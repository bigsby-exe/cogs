from datetime import timezone
import discord
from redbot.core import commands, Config, checks, modlog
from redbot.core.utils.chat_formatting import escape, info, error, humanize_list

class salv(commands.Cog):
    """Auto reply to youtube links."""

    guild_conf = {
            "terms": []
            }

    def __init__(self, bot):
        """Initialize cog. Set up config."""
        self.bot = bot
        self.config = Config.get_conf(self, 0xff5269620001)
        self.config.register_guild(**self.guild_conf)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        """Handle on_message"""
        
        if(
            not isinstance(message.channel, discord.TextChannel) or # this is a DM or group DM, discard early
            message.type != discord.MessageType.default or # this is a system message, discard early
            message.author.bot or  # Message author is a bot
            len(message.clean_content) == 0 # nothing to do, exit early
        ): return

        terms = await self.config.guild(message.guild).terms()
        counter = 0
        content = message.content
        term = ''
        last_term = None
        for term in terms:
            if len(term) > 0:
                if len(content) > 0 and term.lower() in content.lower():
                    counter += 1
                    last_term = term

        if counter >= 1 and len(terms) > 0 and len(term) > 0:
            try:
                await message.channel.send("Fucking great video",
                allowed_mentions=discord.AllowedMentions(
                everyone=False, roles=False, users=False))
            except:
                pass

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @checks.mod_or_permissions(manage_guild=True)
    async def salv(self, ctx, *, term):
        """Add term to the Salvatore list."""
        await ctx.invoke(self.add, term=term)

    @salv.command()
    @commands.guild_only()
    @checks.mod_or_permissions(manage_guild=True)
    async def add(self, ctx, *, term):
        """Add term to the Salvatore list."""
        async with self.config.guild(ctx.guild).terms() as terms:
            if not term in terms:
                terms.append(term)
                await ctx.send(info("Term added."))
            else:
                await ctx.send(error("Term was already present on this server."))

    @salv.command(aliases=["rem", "delete", "del"])
    @commands.guild_only()
    @checks.mod_or_permissions(manage_guild=True)
    async def remove(self, ctx, *, term):
        """Remove term from the Salvatore list."""
        async with self.config.guild(ctx.guild).terms() as terms:
            if term in terms:
                terms.remove(term)
                await ctx.send(info("Term removed."))
            else:
                await ctx.send(error("Term was not present on this server."))

    @salv.command()
    @commands.guild_only()
    @checks.mod_or_permissions(manage_guild=True)
    async def list(self, ctx):
        """List terms from the Salvatore list."""
        async with self.config.guild(ctx.guild).terms() as terms:
            if len(terms) == 0:
                await ctx.send(info("No terms set on this server."))
            else:
                ls = humanize_list(["`{}`".format(term) for term in terms])
                await ctx.send(info("Terms on this server:\n{}".format(ls)))

    @salv.command()
    @commands.guild_only()
    @checks.mod_or_permissions(manage_guild=True)
    async def clear(self, ctx):
        """Clear terms from the Salvatore list."""
        await self.config.guild(ctx.guild).terms.set([])
        await ctx.send(info("Terms cleared on this server."))

