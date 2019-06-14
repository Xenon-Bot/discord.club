from django.db import models


class Shard(models.Model):
    _db = "xenon"

    class Meta:
        managed = False
        db_table = "shards"

    _id = models.IntegerField(primary_key=True)
    guilds = models.BigIntegerField()
    users = models.BigIntegerField()
    latency = models.FloatField()
    seen = models.DateTimeField()
