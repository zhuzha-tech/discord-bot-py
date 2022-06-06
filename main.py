import discord
from discord.ext import commands, tasks
from discord.commands import Option
import logging
from typing import List
import validators

import sys
print(sys.version_info)
print(sys.version_info >= (3, 10))
#logging.basicConfig(level=logging.INFO)

# import random
import os
import boto3
import botocore
import time
# from replit import db
from keep_alive import keep_alive
from datetime import datetime, timedelta

INSTANCE_ID = os.environ.get("INSTANCE_ID", "")
REGION_NAME = os.environ.get("REGION_NAME", "")

TOKEN = os.environ.get("DISCORD_TOKEN", "")
GUILD_ID = os.environ.get("GUILD_ID", "")
ACCESS_KEY = os.environ.get("ACCESS_KEY", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")

ec2_client = boto3.client(
  'ec2',
  region_name=REGION_NAME,
  aws_access_key_id=ACCESS_KEY,
  aws_secret_access_key=SECRET_KEY
)


def pl(number, singular, plural=None):
    if plural == None:
        plural = singular + 's'
    return "{} {}".format(number, singular if number == 1 else plural)


def embed_maker(field_names: List[str], action: str == "Action",
                values: List[str], thumbnail: str == None,
                is_footer: bool == False, footer: str == None,
                color: int == 0x000000):

    embedVar = discord.Embed(title=action.capitalize(), color=color)

    for i in range(len(field_names)):
        embedVar.add_field(name=field_names[i], value=values[i], inline=True)

    if thumbnail is not None:
        if validators.url(thumbnail):
            embedVar.set_thumbnail(url=thumbnail)

    if is_footer:
        embedVar.set_footer(text=footer)

    return embedVar


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("$"))
        #change_time.start()


bot = Bot()


@bot.event
async def on_ready():
    change_time.start()
    logging.info(f"We have logged in as {bot.user}")


@bot.slash_command(guild_ids=[GUILD_ID])
async def joined(ctx,
                 member: discord.Member = None
                 ):  # Passing a default value makes the argument optional
    user = member or ctx.author
    await ctx.respond(
        f"{user.name} joined at {discord.utils.format_dt(user.joined_at)}")


@bot.slash_command(guild_ids=[GUILD_ID], description='Hello, gamers or nerd')
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author}!")


@bot.user_command(guild_ids=[GUILD_ID]
                  )  # create a user command for the supplied guilds
async def mention(ctx,
                  member: discord.Member):  # user commands return the member
    await ctx.respond(f"{ctx.author.name} just mentioned {member.mention}!")


# user commands and message commands can have spaces in their names
@bot.message_command(name="Show ID",
                     guild_ids=[GUILD_ID])  # creates a global message command
async def show_id(
        ctx, message: discord.Message):  # message commands return the message
    await ctx.respond(
        f"{ctx.author.name}, here's the message id: {message.id}!")


@bot.slash_command(guild_ids=[GUILD_ID],
                   description='Interact with game server')
@commands.cooldown(1, 5, commands.BucketType.user
                   )  # the command can only be used once in 5 seconds
async def server(
        ctx: discord.ApplicationContext,
        game: Option(
            str,
            "Pick a game server",
            autocomplete=discord.utils.basic_autocomplete(["valheim", "csgo"]),
        ),  # Demonstrates passing a callback to discord.utils.basic_autocomplete
        action:
    Option(
        str,
        "Pick a action for server",
        autocomplete=discord.utils.basic_autocomplete(
            ["start", "stop", "status"]),
    ),  # Demonstrates passing a static iterable discord.utils.basic_autocomplete
):
    # check that instance exists
    # check the instance status
    # act based on instance status
    thumb_url = "https://images.squarespace-cdn.com/content/v1/5e203941ee6ea226e307532c/1587479704115-BAUOTYM8A1PARFTPNOS2/favicon.ico"

    if action == "start":
        try:
            response = ec2_client.start_instances(InstanceIds=[INSTANCE_ID])
        except botocore.exceptions.ClientError as e:
            await ctx.respond(f"{e}")
        else:
            response_root_field = "StartingInstances"
            response_state_field = "CurrentState"

            instance_id = response[response_root_field][0]['InstanceId']
            instance_state = response[response_root_field][0][
                response_state_field]['Name']

            await ctx.respond(
                embed=embed_maker(["Instance", action.capitalize()], action,
                                  [instance_id, instance_state], thumb_url,
                                  True, "discord-bot (c)", 0x18ec5f))

    elif action == "stop":
        try:
            response = ec2_client.stop_instances(InstanceIds=[INSTANCE_ID])
        except botocore.exceptions.ClientError as e:
            await ctx.respond(f"{e}")
        else:
            response_root_field = "StoppingInstances"
            response_state_field = "CurrentState"
            instance_id = response[response_root_field][0]['InstanceId']
            instance_state = response[response_root_field][0][
                response_state_field]['Name']

            await ctx.respond(
                embed=embed_maker(["Instance", action.capitalize()], action,
                                  [instance_id, instance_state], thumb_url,
                                  True, "discord-bot (c)", 0x18ec5f))

    elif action == "status":
        try:
            response = ec2_client.describe_instance_status(
                InstanceIds=[INSTANCE_ID], IncludeAllInstances=True)
        except botocore.exceptions.ClientError as e:
            await ctx.respond(f"{e}")
        else:
            response_root_field = "InstanceStatuses"
            response_state_field = "InstanceState"
            instance_id = response[response_root_field][0]['InstanceId']
            instance_state = response[response_root_field][0][
                response_state_field]['Name']

            await ctx.respond(
                embed=embed_maker(["Instance", action.capitalize()], action,
                                  [instance_id, instance_state], thumb_url,
                                  True, "discord-bot (c)", 0x18ec5f))

            # embedVar = discord.Embed(title=action.capitalize(), color=0x18ec5f)
            # embedVar.add_field(name="Instance", value=instance_id, inline=True)
            # embedVar.add_field(name="Status", value=instance_state, inline=True)
            # embedVar.set_thumbnail(url="https://images.squarespace-cdn.com/content/v1/5e203941ee6ea226e307532c/1587479704115-BAUOTYM8A1PARFTPNOS2/favicon.ico")
            # embedVar.set_footer(text="discord-bot (c)")
            # await ctx.respond(embed=embedVar)


@bot.slash_command(guild_ids=[GUILD_ID],
                   description='Remainig time till BF Sunday')
async def when_bf(ctx: discord.ApplicationContext):

    wanted_day = 'sunday'
    wanted_time = 19

    list = [['monday', 0], ['tuesday', 1], ['wednesday', 2], ['thursday', 3],
            ['friday', 4], ['saturday', 5], ['sunday', 6]]

    for i in list:
        if wanted_day == i[0]:
            number_wanted_day = i[1]

    # number_today delivers the actual day
    number_today = datetime.today().weekday()

    # today delivers the current date
    today = datetime.now()

    # delta_days describes how many days are left until the wanted day
    delta_days = number_wanted_day - number_today

    # time_now delivers the actual time
    time_now = time.gmtime()

    if wanted_time > time_now[3]:
        delta_hours = wanted_time - time_now[3] - 1
        delta_mins = 59 - time_now[4]

    else:
        delta_days = delta_days - 1
        delta_hours = 23 - time_now[3] + wanted_time
        delta_mins = 59 - time_now[4]

    # day delivers date of the event
    day = timedelta(days=number_wanted_day) + (today -
                                               timedelta(days=today.weekday()))

    date_differ_secs = delta_days * 86400 + delta_hours * 3600 + delta_mins * 60

    output_date = str(
        datetime(day.year, day.month, day.day, wanted_time).strftime(
            "%A, %B %d, %H:%M") + 'Z')

    output_time_remains = str(
        f"{pl(delta_days, 'day')}, {pl(delta_hours, 'hour')}, {pl(delta_mins, 'minute')}."
    )

    thumb_url = "https://drive.google.com/file/d/1b9rUBgpnMGr_ti8_341wC5J21tLGC3Lp/view?usp=sharing"

    # Messages users how much time left till Sunday
    if delta_days < 0:
        day = timedelta(days=number_wanted_day) + (
            today - timedelta(days=today.weekday())) + timedelta(days=7)

        output_time_remains = str(
            f"{pl(delta_days, 'day')}, {pl(delta_hours, 'hour')}, {pl(delta_mins, 'minute')}."
        )

    elif delta_days == 0 and delta_hours == 0:
        output_time_remains = str(f"{pl(delta_mins, 'minute')}.")

    elif delta_days == 0:
        output_time_remains = str(
            f"{pl(delta_hours, 'hour')}, {pl(delta_mins, 'minute')}.")

    elif delta_hours == 0:
        output_time_remains = str(
            f"{pl(delta_days, 'day')}, {pl(delta_mins, 'minute')}.")

    elif delta_mins == 0:
        output_time_remains = str(
            f"{pl(delta_days, 'day')}, {pl(delta_hours, 'hour')}.")

    else:
        output_time_remains = str(
            f"{pl(delta_days, 'day')}, {pl(delta_hours, 'hour')}, {pl(delta_mins, 'minute')}."
        )

    await ctx.respond(embed=embed_maker(
        ["Remaining", "Date"], "Reminder", [output_time_remains, output_date],
        thumb_url, True, "discord-bot (c)", 0x18ec5f))


@tasks.loop(seconds=5)  # task runs every 60 seconds
async def change_time():
    time = 1

    # print("time = ", time)


# error handler
@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown.")
    else:
        raise error  # raise other errors so they aren't ignored


@bot.user_command(name="Say Hello")
async def hi(ctx, user):
    await ctx.respond(f"{ctx.author.mention} says hello to {user.name}!")


# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label="Red",
                                 description="Your favourite colour is red",
                                 emoji="🟥"),
            discord.SelectOption(label="Green",
                                 description="Your favourite colour is green",
                                 emoji="🟩"),
            discord.SelectOption(label="Blue",
                                 description="Your favourite colour is blue",
                                 emoji="🟦"),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(
            placeholder="Choose your favourite colour...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(
            f"Your favourite colour is {self.values[0]}")


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())


@bot.command()
async def colour(ctx):
    """Sends a message with our dropdown containing colours"""

    # Create the view containing our dropdown
    view = DropdownView()

    # Sending a message containing our view
    await ctx.send("Pick your favourite colour:", view=view)


from urllib.parse import quote_plus


# Define a simple View that gives us a google link button.
# We take in `query` as the query that the command author requests for
class Google(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        # we need to quote the query string to make a valid url. Discord will raise an error if it isn't valid.
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"

        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(discord.ui.Button(label="Click Here", url=url))


@bot.command()
async def google(ctx: commands.Context, *, query: str):
    """Returns a google link for a query"""
    await ctx.send(f"Google Result for: `{query}`", view=Google(query))


keep_alive()
bot.run(TOKEN)

# keep_alive()
# client = MyClient()
# client.run(TOKEN)
