from discord.ext import commands as cmd
import discord


class Help(cmd.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @cmd.command()
    async def help(self, ctx):
        embed = discord.Embed(
            url="https://discord.club",
            description="The best way to generate embeds and improve the look of your discord server"
                        "\n\n\n"
                        "__Commands__\n\n"
                        "**>webhook [#channel]** *Get a valid webhook URL for a channel*\n\n"
                        "**>json <message-id-or-url>** *Get the json code for an existing message*\n\n"
                        "**>edit <message-id-or-url>** *Get an existing message directly into the editor*\n\n"
                        "**>format <text>** *Format the given text as the API format (emojis & mentions)*"
                        "\n\n\n"
                        "[Website](https://discord.club)"
                        " | [Support Discord](https://discord.club/discord)"
                        " | [Invite](https://discord.club/invite)"
        )
        embed.set_author(name="Discord.Club", url="https://discord.club")
        await ctx.send(embed=embed)


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
