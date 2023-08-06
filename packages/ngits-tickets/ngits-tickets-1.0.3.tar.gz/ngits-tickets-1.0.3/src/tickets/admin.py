from django.contrib import admin

from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ("date", "status", "created_by", "email", "description")
    list_filter = ("date", "status")
    search_fields = ("email", "description")


admin.site.register(Ticket, TicketAdmin)
