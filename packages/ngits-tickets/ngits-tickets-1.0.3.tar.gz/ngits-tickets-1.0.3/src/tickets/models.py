from django.contrib.auth import get_user_model
from django.db import models

from .consts import Status

User = get_user_model()

EMAIL_MAX_LENGTH = 256
TYPE_MAX_LENGTH = 30


class Ticket(models.Model):
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=8, choices=Status.choices, default=Status.NEW
    )
    type = models.CharField(max_length=TYPE_MAX_LENGTH)

    def __str__(self):
        return "{}, {}, {}".format(self.email, self.date, self.description)
