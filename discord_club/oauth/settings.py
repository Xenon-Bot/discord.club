from os import environ as env

CLIENT_ID = 465946982339444746
CLIENT_SECRET = env.get("CLIENT_SECRET")
SCOPES = ["identify"]
REDIRECT_URI = "https://discord.club/oauth/callback/"
