from django.db import models

from oauth.models import OauthUser


class Invite(models.Model):
    user = models.ForeignKey(OauthUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=32)

    def __str__(self):
        return self.name
