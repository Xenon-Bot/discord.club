from django.shortcuts import render

from .models import Shard


def index(request):
    shards = list(Shard.objects.all())
    context = {
        "shards": Shard.objects.all(),
        "guilds": sum([shard.guilds for shard in shards]),
        "users": sum([shard.users for shard in shards])
    }
    return render(request, 'xenon/index.html', context)
