from django.db import models


class Redirect(models.Model):
    path = models.CharField(max_length=50, unique=True)
    permanent = models.BooleanField(default=False)
    target = models.CharField(max_length=250)

    def __str__(self):
        return "%s, %s" % (self.path, self.target)
