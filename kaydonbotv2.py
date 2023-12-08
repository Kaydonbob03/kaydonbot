import os
import discord
import openai
import requests
from discord.ext import commands
from discord import app_commands

# Define your guild ID here (replace with your guild's ID)
MY_GUILD = discord.Object(id=1178205977380671529)  

# Set your OpenAI API key (ensure this is set in your environment variables)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create a bot instance
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Event listener for when the bot is ready
@bot.event
async def on_ready():
    # Sync the command tree
    await bot.tree.sync(guild=MY_GUILD)  
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

# Define a slash command for 'commands'
@bot.tree.command(name="commands", description="Get a list off all commands", guild=MY_GUILD)  
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("""Hello! Welcome to KaydonbotV2! Here is my current commands:
        /commands - Displays list of all commands
        /hello - Bot will say hello
        /chat prompt: str - This command will send whatever prompt you would like to ask the gpt api and it will return a response
        /image prompt: str - This command will take your prompt and use DALL-E 3 image generator to generate an image                           
    """)

# Define a slash command for 'hello'
@bot.tree.command(name="hello", description="This is just a simple hello command.", guild=MY_GUILD)  
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello! How are you today?")


# Define a slash command for 'chat'
@bot.tree.command(name="chat", description="Get a response from GPT", guild=MY_GUILD)
async def gpt(interaction: discord.Interaction, prompt: str):
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
async def dalle(interaction: discord.Interaction, prompt: str):
    # Defer the response to give more time for processing
    await interaction.response.defer()

    image_url = await generate_dalle_image(prompt)
    if image_url:
        await interaction.followup.send(image_url)
    else:
        await interaction.followup.send("Sorry, I couldn't generate an image.")



# Run the bot with your token
bot.run('MTE4MTE0Mzg1NDk1OTgzNzE4NA.GvyQxQ.7AXQUI2YtMC8lKPbXsJigwSQqV-penF1ACUXzY')  

# -------------------------------------------------------NO GUILD ID BLOCK-------------------------------------------------------------

# # Set your OpenAI API key (ensure this is set in your environment variables)
# openai.api_key = os.getenv('OPENAI_API_KEY')

# # Create a bot instance
# intents = discord.Intents.default()
# bot = commands.Bot(command_prefix='!', intents=intents)

# # Event listener for when the bot is ready
# @bot.event
# async def on_ready():
#     # Sync the command tree globally
#     await bot.tree.sync()  # This will register commands globally
#     print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
#     print('------')

# # Define a global slash command for 'help'
# @bot.tree.command(name="help", description="Get a list off all commands")  
# async def help_command(interaction: discord.Interaction):
#     await interaction.response.send_message("""Hello! Welcome to KaydonbotV2! Here are my current commands:
#         /help - Displays list of all commands
#         /hello - Bot will say hello
#         /gpt prompt: str - This command will send whatever prompt you would like to ask the gpt api and it will return a response
#         /dalle prompt: str - This command will take your prompt and use DALL-E 3 image generator to generate an image                           
#     """)

# # Define a global slash command for 'hello'
# @bot.tree.command(name="hello", description="This is just a simple hello command.")  
# async def hello_command(interaction: discord.Interaction):
#     await interaction.response.send_message("Hello! How are you today?")

# # Define a global slash command for 'gpt'
# @bot.tree.command(name="gpt", description="Get a response from GPT")
# async def gpt_command(interaction: discord.Interaction, prompt: str):
#     # Prepare the chat messages for the API call
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": prompt}
#     ]

#     # Call OpenAI Chat Completions API with the prompt
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages
#     )

#     # Send the response back to Discord
#     await interaction.response.send_message(response['choices'][0]['message']['content'])

# # Function to call DALL-E 3 API
# async def generate_dalle_image(prompt: str):
#     try:
#         response = openai.Image.create(
#             model="dall-e-3",
#             prompt=prompt,
#             size="1024x1024",
#             quality="standard",
#             n=1,
#         )
#         image_url = response['data'][0]['url']
#         return image_url
#     except Exception as e:
#         print(f"Error generating image: {e}")
#         return None

# # Define a global slash command for 'dalle'
# @bot.tree.command(name="dalle", description="Generate an image using DALL-E 3")
# async def dalle_command(interaction: discord.Interaction, prompt: str):
#     # Defer the response to give more time for processing
#     await interaction.response.defer()

#     image_url = await generate_dalle_image(prompt)
#     if image_url:
#         await interaction.followup.send(image_url)
#     else:
#         await interaction.followup.send("Sorry, I couldn't generate an image.")

# # Run the bot with your token
# bot.run('MTE4MTE0Mzg1NDk1OTgzNzE4NA.GvyQxQ.7AXQUI2YtMC8lKPbXsJigwSQqV-penF1ACUXzY')
