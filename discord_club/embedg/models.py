from django.db import models
from datetime import datetime
import pytz

from oauth.models import OauthUser


def _default_timestamp():
    return datetime.now(tz=pytz.utc)


class Embed(models.Model):
    user = models.ForeignKey(OauthUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=_default_timestamp)
    data = models.TextField()

    @property
    def timestamp_str(self):
        return self.timestamp.strftime("%d. %b %Y - %H:%M")

    def __str__(self):
        return str(self.user) + " - " + self.timestamp_str
