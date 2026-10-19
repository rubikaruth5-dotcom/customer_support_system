from django.contrib import admin
from .models import Ticket, UserProfile


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "priority",
        "status",
        "created_by",
        "created_at",
    )
    list_filter = ("category", "priority", "status")
    search_fields = ("title", "description")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)