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

    def is_online(self):
        return (datetime.now(pytz.utc) - self.seen).seconds < 3 * 60
