from django.db import models


class Supporter(models.Model):
    name = models.CharField(max_length=50)
    patreon_name = models.CharField(max_length=100)
    avatar = models.URLField()

    instagram = models.URLField(blank=True)
    discord = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    twitch = models.URLField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    author_id = models.CharField(max_length=18)
    text = models.TextField()

    def __str__(self):
        return self.text


class Service(models.Model):
    name = models.CharField(max_length=50)
    view = models.CharField(max_length=50, blank=True)

    display_front = models.BooleanField(default=False)
    image_name = models.CharField(max_length=100, blank=True)
    bullet_points = models.TextField()

    def __str__(self):
        return self.name


class Link(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    url = models.URLField()

    def __str__(self):
        return self.name
