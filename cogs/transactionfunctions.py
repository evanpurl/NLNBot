import discord
from discord import app_commands
from discord.ext import commands

from util.databasefunctions import create_pool, get


# Needs "manage role" perms
# ticket-username


class transactionbuttonpanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Finalize Transaction", style=discord.ButtonStyle.green,
                       custom_id="transaction:close")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.channel.delete()
        except Exception as e:
            print(e)


class transactioncmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="transaction", description="Command used to start a transaction with a player.")
    async def transaction(self, interaction: discord.Interaction, member: discord.Member):
        try:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
                member: discord.PermissionOverwrite(read_messages=True)}

            pool = await create_pool()
            data = await get(pool,
                             f"""SELECT transactioncategoryid FROM {self.bot.user.name.replace(" ", "_")} WHERE serverid={member.guild.id}""")

            transactioncat = discord.utils.get(interaction.guild.categories, id=int(data))
            if transactioncat:
                transactionchan = await interaction.guild.create_text_channel(
                    f"transaction-{interaction.user.name}-{member.name}", category=transactioncat,
                    overwrites=overwrites)
            else:
                transactionchan = await interaction.guild.create_text_channel(
                    f"transaction-{interaction.user.name}-{member.name}",
                    overwrites=overwrites)
            await interaction.response.send_message(content=f"Transaction started: {transactionchan.mention}!",
                                                    ephemeral=True)
            await transactionchan.send(
                content=f"{interaction.user.mention} started a transaction with {member.mention}")
            await transactionchan.send(view=transactionbuttonpanel())

        except Exception as e:
            print(e)

    @transaction.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(transactioncmd(bot))
    bot.add_view(transactionbuttonpanel())
