from datetime import timezone
from email import message
import discord
from redbot.core import commands, Config, checks, modlog
from redbot.core.utils.chat_formatting import escape, info, error, humanize_list

class secretsanta(commands.Cog):
    """Auto reply to youtube links."""

    guild_conf = {
            "ssusers": []
            }

    def __init__(self, bot):
        """Initialize cog. Set up config."""
        self.bot = bot
        self.config = Config.get_conf(self, 0xFF526998EE54)
        self.config.register_guild(**self.guild_conf)
        
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def secretsanta(self, ctx, *, term):
        """Add term to the Salvatore list."""
        await ctx.invoke(self.add, term=term)

    @secretsanta.command()
    @commands.guild_only()
    async def join(self, ctx):
        user = str(ctx.author.display_name)
        """Add term to the secretsantaatore list."""
        async with self.config.guild(ctx.guild).ssusers() as ssusers:
            if not user in ssusers:
                ssusers.append(user)
                await ctx.send(info("You have been added to Secret Santa 2022."))
            else:
                await ctx.send(error("You are already in  Secret Santa 2022."))

    @secretsanta.command()
    @commands.guild_only()
    async def list(self, ctx):
        """List ssusers from the secretsantaatore list."""
        async with self.config.guild(ctx.guild).ssusers() as ssusers:
            if len(ssusers) == 0:
                await ctx.send(info("No ssusers set on this server."))
            else:
                ls = humanize_list(["`{}`".format(term) for term in ssusers])
                await ctx.send(info("ssusers on this server:\n{}".format(ls)))

    @secretsanta.command()
    @commands.guild_only()
    @checks.mod_or_permissions(manage_guild=True)
    async def clear(self, ctx):
        """Clear ssusers from the secretsantaatore list."""
        await self.config.guild(ctx.guild).ssusers.set([])
        await ctx.send(info("ssusers cleared on this server."))

