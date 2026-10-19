from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from .ai_helper import predict_ticket
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Ticket
from .serializers import TicketSerializer



class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    filter_backends = [ DjangoFilterBackend,SearchFilter]
    filterset_fields = ["status", "priority", "category"]
    search_fields = ["title", "description"]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return Ticket.objects.all()

        profile = getattr(user, "userprofile", None)

        if profile and profile.role in ["admin", "agent"]:
            return Ticket.objects.all()

        return Ticket.objects.filter(created_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        
        profile = getattr(user, "userprofile", None)

        is_agent_or_admin = (
            user.is_staff
            or user.is_superuser
            or (
                profile is not None
                and profile.role in ["admin", "agent"]
            )
        )

        protected_fields = {"category", "priority", "status"}
        changed_fields = protected_fields.intersection(
            self.request.data.keys()
        )

        if changed_fields and not is_agent_or_admin:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Customers cannot change ticket category, priority, or status."
            )

        serializer.save()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    user = request.user

    if user.is_superuser or user.is_staff:
        tickets = Ticket.objects.all()
    else:
        profile = getattr(user, "userprofile", None)

        if profile and profile.role in ["admin", "agent"]:
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(created_by=user)

    summary = tickets.aggregate(
        total=Count("id"),
        open=Count("id", filter=Q(status="open")),
        in_progress=Count("id", filter=Q(status="in_progress")),
        resolved=Count("id", filter=Q(status="resolved")),
        closed=Count("id", filter=Q(status="closed")),
        high_priority=Count(
            "id", filter=Q(priority__in=["high", "urgent"])
        ),
    )

    return Response(summary)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def predict_ticket_api(request):
    description = request.data.get("description", "").strip()

    if not description:
        return Response(
            {"error": "Please provide a ticket description."},
            status=400
        )

    prediction = predict_ticket(description)

    return Response({
        "description": description,
        "predicted_category": prediction["category"],
        "predicted_priority": prediction["priority"],
    })
