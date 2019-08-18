from django.db import models
from datetime import datetime
import pytz


class Shard(models.Model):
    _db = "xenon"

    class Meta:
        managed = False
        db_table = "shards"

    id = models.IntegerField(primary_key=True, db_column="_id")
    guilds = models.BigIntegerField()
    users = models.BigIntegerField()
    latency = models.FloatField()
    seen = models.DateTimeField()

    def is_online(self) -> bool:
        return (datetime.now(pytz.utc) - self.seen).seconds < 3 * 60

    def get_latency(self) -> str:
        if self.is_online():
            return str(round(self.latency * 1000, 1))

        else:
            return "offline"


class Template(models.Model):
    _db = "xenon"

    class Meta:
        managed = False
        db_table = "templates"

    name = models.CharField(max_length=2000, primary_key=True, db_column="_id")
    creator = models.BigIntegerField()
    used = models.IntegerField()
    featured = models.BooleanField()
    approved = models.BooleanField()
    original = models.CharField(max_length=16)
    description = models.TextField()


class Backup(models.Model):
    _db = "xenon"

    class Meta:
        managed = False
        db_table = "backups"

    id = models.CharField(max_length=16, primary_key=True, db_column="_id")
    creator = models.BigIntegerField()
    timestamp = models.DateTimeField()


class Interval(models.Model):
    _db = "xenon"

    class Meta:
        managed = False
        db_table = "intervals"

    guild = models.BigIntegerField(primary_key=True, db_column="_id")
    chatlog = models.IntegerField()
    interval = models.IntegerField()
    next = models.DateTimeField()


