from rest_framework.routers import DefaultRouter
from .views import TicketViewSet,predict_ticket_api,dashboard_summary
from django.urls import path

router = DefaultRouter()
router.register("tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("dashboard/summary/", dashboard_summary, name="dashboard-summary"),
    path("predict/", predict_ticket_api, name="predict-ticket"),
] + router.urls