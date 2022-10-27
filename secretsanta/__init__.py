from .secretsanta import secretsanta

def setup(bot):
    bot.add_cog(secretsanta(bot))