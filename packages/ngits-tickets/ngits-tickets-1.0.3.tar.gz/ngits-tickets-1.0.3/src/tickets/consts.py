from django.db.models import TextChoices


class Status(TextChoices):
    NEW = "new"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DONE = "done"


class Type(TextChoices):
    CRASH = "crash"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    LOG = "log"
