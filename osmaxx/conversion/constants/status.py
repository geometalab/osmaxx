from enum import Enum
from django.utils.translation import gettext_lazy as _

RECEIVED = "received"
QUEUED = "queued"
FINISHED = "finished"
FAILED = "failed"
STARTED = "started"
DEFERRED = "deferred"

CHOICES = (
    (RECEIVED, _("received")),
    (QUEUED, _("queued")),
    (FINISHED, _("finished")),
    (FAILED, _("failed")),
    (STARTED, _("started")),
    (DEFERRED, _("deferred")),
)

FINAL_STATUSES = [FINISHED, FAILED]
