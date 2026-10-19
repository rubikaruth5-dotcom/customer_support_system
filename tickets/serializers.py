from rest_framework import serializers
from .models import Ticket
from .ai_helper import predict_ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]
        
    def create(self, validated_data):
        description = validated_data.get("description", "")
        prediction = predict_ticket(description)

        validated_data["category"] = prediction["category"]
        validated_data["priority"] = prediction["priority"]

        return super().create(validated_data)


    
    def validate(self, attrs):
        request = self.context.get("request")

        if not request or not self.instance:
            return attrs

        user = request.user
        profile = getattr(user, "userprofile", None)

        is_agent_or_admin = (
            user.is_staff
            or user.is_superuser
            or (
                profile is not None
                and profile.role in ["agent", "admin"]
            )
        )

        protected_fields = {"category", "priority", "status"}

        if not is_agent_or_admin:
            changed_fields = protected_fields.intersection(attrs.keys())

            if changed_fields:
                raise serializers.ValidationError(
                    "Only support agents and admins can change "
                    "category, priority, or status."
                )

        return attrs
