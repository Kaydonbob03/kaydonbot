import os
import discord
import openai
import json
import requests
from discord.ext import commands
from discord import app_commands

# ========================================================================================================================

# --------------------------------------------------INITIALIZATION------------------------------------------------------

# Define your guild ID here (replace with your guild's ID)
MY_GUILD = discord.Object(id=1178205977380671529)  

# Set your OpenAI API key (ensure this is set in your environment variables)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create a bot instance
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=';', intents=intents)


welcome_channels = {}

# Event listener for when the bot is ready
@bot.event
async def on_ready():
    # Sync the command tree
    global welcome_channels
    welcome_channels = await load_welcome_channels()
    await bot.tree.sync(guild=MY_GUILD)  
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

# -------------------------------------------------INITIALIZATION ENDS--------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------MOD-ONLY COMMANDS----------------------------------------------------

# Send welcome message on user join
@bot.event
async def on_member_join(member):
    guild_id = member.guild.id
    channel_id = welcome_channels.get(guild_id)
    channel = member.guild.get_channel(channel_id) if channel_id else discord.utils.get(member.guild.text_channels, name='welcome')
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}!")

# Check if user is admin/mod
def is_admin_or_mod():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.guild_permissions.administrator or \
               any(role.name.lower() in ['admin', 'moderator'] for role in interaction.user.roles)
    return app_commands.check(predicate)
    
def save_welcome_channels():
    with open('welcome_channels.json', 'w') as file:
        json.dump(welcome_channels, file)
        
async def load_welcome_channels():
    try:
        with open('welcome_channels.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        fallback_channels = {}
        for guild in bot.guilds:
            welcome_channel = discord.utils.get(guild.text_channels, name='welcome')
            if welcome_channel:
                fallback_channels[guild.id] = welcome_channel.id
        return fallback_channels
        
# Define a slash command for 'welcomeconfig'
@bot.tree.command(name="welcomeconfig", description="Configure the welcome channel", guild=MY_GUILD)
@is_admin_or_mod()
async def welcomeconfig(interaction: discord.Interaction, channel: discord.TextChannel):
    try:
        # Defer the response to give more time for processing
        await interaction.response.defer()

        guild_id = interaction.guild_id
        welcome_channels[guild_id] = channel.id
        save_welcome_channels() 

        # Send the follow-up message after processing
        await interaction.followup.send(f"Welcome channel set to {channel.mention}")
    except Exception as e:
        await interaction.followup.send(f"Failed to set welcome channel: {e}")

# Define a slash command for 'msgclear'
@bot.tree.command(name="msgclear", description="Clear a specified number of messages in a channel", guild=MY_GUILD)
@is_admin_or_mod()
async def msgclear(interaction: discord.Interaction, channel: discord.TextChannel, number: int):
    try:
        await interaction.response.defer()

        if number < 1 or number > 100:
            await interaction.followup.send("Please specify a number between 1 and 100.")
            return

        messages = [message async for message in channel.history(limit=number)]
        if not messages:
            await interaction.followup.send("No messages to delete.")
            return

        deleted_count = 0
        for message in messages:
            if (discord.utils.utcnow() - message.created_at).days < 14:
                await message.delete()
                deleted_count += 1

        confirmation_message = await interaction.followup.send(f"Cleared {deleted_count} messages in {channel.mention}.")
        await asyncio.sleep(5)  # Wait for 5 seconds
        await confirmation_message.delete()
    except Exception as e:
        await interaction.followup.send(f"Failed to clear messages: {e}")


@bot.tree.command(name="warn", description="Warn a member", guild=MY_GUILD)
@is_admin_or_mod()
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    try:
        await interaction.response.defer()
        # Send a DM to the member with the warning
        await member.send(f"You have been warned for: {reason}")
        await interaction.followup.send(f"{member.mention} has been warned for: {reason}")
    except Exception as e:
        await interaction.followup.send(f"Failed to warn member: {e}")

@bot.tree.command(name="kick", description="Kick a member from the server", guild=MY_GUILD)
@is_admin_or_mod()
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    try:
        await interaction.response.defer()
        await member.kick(reason=reason)
        await interaction.followup.send(f"{member.mention} has been kicked for: {reason}")
    except Exception as e:
        await interaction.followup.send(f"Failed to kick member: {e}")

@bot.tree.command(name="ban", description="Ban a member from the server", guild=MY_GUILD)
@is_admin_or_mod()
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    try:
        await interaction.response.defer()
        await member.ban(reason=reason)
        await interaction.followup.send(f"{member.mention} has been banned for: {reason}")
    except Exception as e:
        await interaction.followup.send(f"Failed to ban member: {e}")

import asyncio

@bot.tree.command(name="mute", description="Mute a member", guild=MY_GUILD)
@is_admin_or_mod()
async def mute(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided"):
    try:
        await interaction.response.defer()
        muted_role = discord.utils.get(member.guild.roles, name="Muted")
        if not muted_role:
            await interaction.followup.send("Muted role not found.")
            return

        await member.add_roles(muted_role, reason=reason)
        await interaction.followup.send(f"{member.mention} has been muted for {duration} minutes. Reason: {reason}")

        await asyncio.sleep(duration * 60)  # Convert minutes to seconds
        if muted_role in member.roles:
            await member.remove_roles(muted_role, reason="Mute duration expired")
            await interaction.followup.send(f"{member.mention} has been unmuted.")
    except Exception as e:
        await interaction.followup.send(f"Failed to mute member: {e}")

@bot.tree.command(name="unmute", description="Unmute a member", guild=MY_GUILD)
@is_admin_or_mod()
async def unmute(interaction: discord.Interaction, member: discord.Member):
    try:
        await interaction.response.defer()
        muted_role = discord.utils.get(member.guild.roles, name="Muted")
        if not muted_role:
            await interaction.followup.send("Muted role not found.")
            return

        if muted_role in member.roles:
            await member.remove_roles(muted_role, reason="Manually unmuted")
            await interaction.followup.send(f"{member.mention} has been unmuted.")
        else:
            await interaction.followup.send(f"{member.mention} is not muted.")
    except Exception as e:
        await interaction.followup.send(f"Failed to unmute member: {e}")


@bot.tree.command(name="lock", description="Lock a channel", guild=MY_GUILD)
@is_admin_or_mod()
async def lock(interaction: discord.Interaction, channel: discord.TextChannel):
    try:
        await interaction.response.defer()
        await channel.set_permissions(channel.guild.default_role, send_messages=False)
        await interaction.followup.send(f"{channel.mention} has been locked.")
    except Exception as e:
        await interaction.followup.send(f"Failed to lock the channel: {e}")

@bot.tree.command(name="unlock", description="Unlock a channel", guild=MY_GUILD)
@is_admin_or_mod()
async def unlock(interaction: discord.Interaction, channel: discord.TextChannel):
    try:
        await interaction.response.defer()
        await channel.set_permissions(channel.guild.default_role, send_messages=True)
        await interaction.followup.send(f"{channel.mention} has been unlocked.")
    except Exception as e:
        await interaction.followup.send(f"Failed to unlock the channel: {e}")


@bot.tree.command(name="slowmode", description="Set slowmode in a channel", guild=MY_GUILD)
@is_admin_or_mod()
async def slowmode(interaction: discord.Interaction, channel: discord.TextChannel, seconds: int):
    try:
        await interaction.response.defer()
        await channel.edit(slowmode_delay=seconds)
        await interaction.followup.send(f"Slowmode set to {seconds} seconds in {channel.mention}.")
    except Exception as e:
        await interaction.followup.send(f"Failed to set slowmode: {e}")


@bot.tree.command(name="purgeuser", description="Clear messages by a specific user", guild=MY_GUILD)
@is_admin_or_mod()
async def purgeuser(interaction: discord.Interaction, channel: discord.TextChannel, member: discord.Member, number: int):
    try:
        await interaction.response.defer()
        deleted_count = 0
        async for message in channel.history(limit=200):
            if message.author == member and deleted_count < number:
                await message.delete()
                deleted_count += 1
            if deleted_count >= number:
                break
        await interaction.followup.send(f"Cleared {deleted_count} messages from {member.mention} in {channel.mention}.")
    except Exception as e:
        await interaction.followup.send(f"Failed to clear messages: {e}")


@bot.tree.command(name="announce", description="Send an announcement", guild=MY_GUILD)
@is_admin_or_mod()
async def announce(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    try:
        await interaction.response.defer()
        await channel.send(message)
        await interaction.followup.send(f"Announcement sent in {channel.mention}.")
    except Exception as e:
        await interaction.followup.send(f"Failed to send announcement: {e}")


@bot.tree.command(name="addrole", description="Add a role to a member", guild=MY_GUILD)
@is_admin_or_mod()
async def addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    try:
        await interaction.response.defer()
        if role in member.roles:
            await interaction.followup.send(f"{member.mention} already has the {role.name} role.")
            return

        await member.add_roles(role)
        await interaction.followup.send(f"Added {role.name} role to {member.mention}.")
    except Exception as e:
        await interaction.followup.send(f"Failed to add role: {e}")


@bot.tree.command(name="removerole", description="Remove a role from a member", guild=MY_GUILD)
@is_admin_or_mod()
async def removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    try:
        await interaction.response.defer()
        if role not in member.roles:
            await interaction.followup.send(f"{member.mention} does not have the {role.name} role.")
            return

        await member.remove_roles(role)
        await interaction.followup.send(f"Removed {role.name} role from {member.mention}.")
    except Exception as e:
        await interaction.followup.send(f"Failed to remove role: {e}")




# -------------------------------------------------MOD-ONLY COMMANDS ENDS----------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------COMMANDS LIST------------------------------------------------------------


# Define a slash command for 'commands'
@bot.tree.command(name="commands", description="Get a list off all commands", guild=MY_GUILD)
async def commands(interaction: discord.Interaction):
    # Defer the initial response
    await interaction.response.defer()

    # Send a follow-up message with the embed
    message = await interaction.followup.send(embed=get_general_commands_embed())

    # Add reactions to the follow-up message
    await message.add_reaction("⬅️")
    await message.add_reaction("➡️")

def get_general_commands_embed():
    embed = discord.Embed(
        title="KaydonbotV2 General Commands",
        description="Commands available for all users.",
        color=discord.Color.gold()
    )
    embed.add_field(name="/commands", value="Displays list of all commands", inline=False)
    embed.add_field(name="/hello", value="Bot will say hello", inline=False)
    embed.add_field(name="/chat [prompt]", value="Sends a prompt to the GPT API and returns a response", inline=False)
    embed.add_field(name="/image [prompt]", value="Uses DALL-E 3 to generate an image based on your prompt", inline=False)
    embed.set_footer(text="Page 1/2")
    return embed

def get_mod_commands_embed():
    embed = discord.Embed(
        title="KaydonbotV2 Moderator Commands",
        description="Commands available for moderators and administrators.",
        color=discord.Color.green()
    )
    # Add fields for each moderator command
    embed.add_field(name="/welcomeconfig", value="Configure the welcome message channel", inline=False)
    embed.add_field(name="/msgclear [channel] [number]", value="Clear a specified number of messages in a channel", inline=False)
    embed.add_field(name="/mute [member] [duration] [reason]", value="Mute a member", inline=False)
    embed.add_field(name="/unmute [member]", value="Unmute a member", inline=False)
    embed.add_field(name="/lock [channel]", value="Lock a channel", inline=False)
    embed.add_field(name="/unlock [channel]", value="Unlock a channel", inline=False)
    embed.add_field(name="/slowmode [channel] [seconds]", value="Set slowmode in a channel", inline=False)
    embed.add_field(name="/purgeuser [channel] [member] [number]", value="Clear messages by a specific user", inline=False)
    embed.add_field(name="/announce [channel] [message]", value="Send an announcement", inline=False)
    embed.add_field(name="/addrole [member] [role]", value="Add a role to a member", inline=False)
    embed.add_field(name="/removerole [member] [role]", value="Remove a role from a member", inline=False)
    embed.set_footer(text="Page 2/2")
    return embed


@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is on the commands message and is from a non-bot user
    if user != bot.user and reaction.message.author == bot.user:
        embeds = [get_general_commands_embed(), get_mod_commands_embed()]
        current_page = int(reaction.message.embeds[0].footer.text.split('/')[0][-1]) - 1

        if reaction.emoji == "➡️":
            next_page = (current_page + 1) % len(embeds)
            await reaction.message.edit(embed=embeds[next_page])
        elif reaction.emoji == "⬅️":
            next_page = (current_page - 1) % len(embeds)
            await reaction.message.edit(embed=embeds[next_page])

        await reaction.remove(user)

# --------------------------------------------------COMMANDS LIST ENDS-------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------OPENAI COMMANDS---------------------------------------------------------


# Define a slash command for 'chat'
@bot.tree.command(name="chat", description="Get a response from GPT", guild=MY_GUILD)
async def chat(interaction: discord.Interaction, prompt: str):
    # Prepare the chat messages for the API call
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    # Call OpenAI Chat Completions API with the prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Send the response back to Discord
    await interaction.response.send_message(response['choices'][0]['message']['content'])

# Function to call DALL-E 3 API
async def generate_dalle_image(prompt: str):
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

# Define a slash command for 'image'
@bot.tree.command(name="image", description="Generate an image using DALL-E 3", guild=MY_GUILD)
async def image(interaction: discord.Interaction, prompt: str):
    # Defer the response to give more time for processing
    await interaction.response.defer()

    image_url = await generate_dalle_image(prompt)
    if image_url:
        await interaction.followup.send(image_url)
    else:
        await interaction.followup.send("Sorry, I couldn't generate an image.")

# ------------------------------------------------OPENAI COMMANDS ENDS-----------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------GENERAL COMMANDS--------------------------------------------------------

# Define a slash command for 'hello'
@bot.tree.command(name="hello", description="This is just a simple hello command.", guild=MY_GUILD)  
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello! How are you today?")









# ------------------------------------------------OPENAI COMMANDS ENDS-----------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------BOT TOKEN BELOW---------------------------------------------------------



# Run the bot with your token
bot.run('MTE4MTE0Mzg1NDk1OTgzNzE4NA.GvyQxQ.7AXQUI2YtMC8lKPbXsJigwSQqV-penF1ACUXzY') 

# --------------------------------------------------BOT TOKEN ENDS--------------------------------------------------------

# ========================================================================================================================




# =======================================================================================================================================
# =========================================================={NO GUILD ID BLOCK}==========================================================
# =======================================================================================================================================


# # Set your OpenAI API key (ensure this is set in your environment variables)
# openai.api_key = os.getenv('OPENAI_API_KEY')

# # Create a bot instance
# intents = discord.Intents.default()
# intents.members = True
# bot = commands.Bot(command_prefix='!', intents=intents)

# welcome_channels = {}

# # Event listener for when the bot is ready
# @bot.event
# async def on_ready():
#     # Sync the command tree globally
#     await bot.tree.sync()  
#     print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
#     print('------')

# @bot.event
# async def on_member_join(member):
#     guild_id = member.guild.id
#     if guild_id in welcome_channels:
#         channel = member.guild.get_channel(welcome_channels[guild_id])
#         if channel:
#             await channel.send(f"Welcome to the server, {member.mention}!")

# def is_admin_or_mod():
#     async def predicate(ctx):
#         return ctx.author.guild_permissions.administrator or \
#                any(role.name.lower() in ['admin', 'moderator'] for role in ctx.author.roles)
#     return app_commands.check(predicate)

# @bot.tree.command(name="config", description="Configure the welcome channel")
# @is_admin_or_mod()
# async def config(interaction: discord.Interaction, channel: discord.TextChannel):
#     guild_id = interaction.guild_id
#     welcome_channels[guild_id] = channel.id
#     await interaction.response.send_message(f"Welcome channel set to {channel.mention}")

# @bot.tree.command(name="commands", description="Get a list off all commands")
# async def commands(interaction: discord.Interaction):
#     await interaction.response.send_message("""Hello! Welcome to KaydonbotV2! Here is my current commands:
#         /commands - Displays list of all commands
#         /hello - Bot will say hello
#         /chat prompt: str - This command will send whatever prompt you would like to ask the gpt api and it will return a response
#         /image prompt: str - This command will take your prompt and use DALL-E 3 image generator to generate an image 
#         /config - This Command is for moderators and admins to configure the welcome message channel                          
#     """)

# @bot.tree.command(name="hello", description="This is just a simple hello command.")
# async def hello(interaction: discord.Interaction):
#     await interaction.response.send_message("Hello! How are you today?")

# @bot.tree.command(name="chat", description="Get a response from GPT")
# async def gpt(interaction: discord.Interaction, prompt: str):
#     # ... [rest of your gpt command]

# # ... [rest of your dalle command and other functions]

# # Run the bot with your token
# bot.run('MTE4MTE0Mzg1NDk1OTgzNzE4NA.GvyQxQ.7AXQUI2YtMC8lKPbXsJigwSQqV-penF1ACUXzY')
