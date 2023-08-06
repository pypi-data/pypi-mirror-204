from rest_framework import mixins, permissions, viewsets

from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
