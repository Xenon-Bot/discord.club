from django.db import models


class OauthUser(models.Model):
    id = models.CharField(max_length=18, primary_key=True)
    name = models.CharField(max_length=32)
    discriminator = models.CharField(max_length=4)
    email = models.EmailField(blank=True)

    access_token = models.CharField(max_length=48)
    refresh_token = models.CharField(max_length=48)

    def __str__(self):
        return "{s.name}#{s.discriminator} ({s.id})".format(s=self)
