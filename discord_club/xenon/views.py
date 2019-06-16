from django.shortcuts import render

from .models import Shard


def index(request):
    shards = list(Shard.objects.all())
    guilds = sum([shard.guilds for shard in shards])
    users = sum([shard.users for shard in shards])
    context = {
        "shards": Shard.objects.all(),
        "guilds": guilds,
        "guild_steps": guilds // 500,
        "users": users,
        "user_steps": users // 500
    }
    return render(request, 'xenon/index.html', context)
