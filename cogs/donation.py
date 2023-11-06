import asyncio
import datetime
import os

import discord
import stripe
from discord import app_commands
from discord.ext import commands

from util.databasefunctions import create_pool, get
from util.sqlitefunctions import create_db, getconfig

stripe.api_key = os.getenv('stripesecret')


def find_prodid(input_list, name):
    try:
        for a in input_list:
            if a[name]:
                return a[name]
    except KeyError:  # If name not found in dictionaries, return name param (product id most likely)
        return name


class donationcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="donate", description="Command used to donate to the community")
    async def donate(self, interaction: discord.Interaction):
        try:
            itemlist = []
            for item in stripe.Product.list():
                if item.active:
                    iteminfo = {item.name: item.id}  # Item information stored here
                    itemlist.append(iteminfo)

            prod = find_prodid(itemlist, "donation")
            item = stripe.Product.retrieve(prod)
            price = stripe.Price.list(product=item).data[0]
            print(price)
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price.id,
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'https://discord.com/channels/{interaction.guild.id}/{interaction.channel.id}',
                cancel_url=f'https://discord.com/channels/{interaction.guild.id}/{interaction.channel.id}',
            )

            embed = discord.Embed(title=self.bot.user.name,
                                  color=0x00ff00)
            embed.add_field(name="Donation Link", value=f"[Donation Link]({session.url})")

            await interaction.response.send_message(embed=embed, ephemeral=True)

            while session.payment_status != "paid":
                await asyncio.sleep(1)
                session = stripe.checkout.Session.retrieve(session.id)

            pool = await create_pool()
            data = await get(pool,
                             f"""SELECT supporterroleid FROM {self.bot.user.name.replace(" ", "_")} WHERE serverid={interaction.guild.id}""")
            role = discord.utils.get(interaction.guild.roles, id=data)

            if role:
                if role not in interaction.user.roles:
                    await interaction.user.add_roles(role)
                    embed = discord.Embed(title=self.bot.user.name,
                                          description=f"Thank you for donating {interaction.user.mention}! You "
                                                      f"have been given the role {role.mention}!",
                                          color=0x00ff00)
                else:
                    embed = discord.Embed(title=self.bot.user.name,
                                          description=f"Thank you for donating {interaction.user.mention}!",
                                          color=0x00ff00)
            else:
                embed = discord.Embed(title=self.bot.user.name,
                                      description=f"Thank you for donating {interaction.user.mention}!",
                                      color=0x00ff00)

            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            print(e)

    @donate.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(donationcmd(bot))
