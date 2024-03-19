# Kaydonbot Discord Bot

KaydonBot is a Discord bot designed to enhance the functionality and interactivity of Discord servers. It integrates features like greeting new members, responding to user prompts using GPT-3.5-turbo, generating images with DALL-E 3, and a wide assortment of general commands, moderation commands, botgames, fortnite commands, and even dev commands. It also includes a rate limit system on moderator commands to prevent abuse. 

> Further info can be found on our website for the bot. Found [here](https://kaydonbot.xyz/)

## Features

- **Welcome Messages**: Sends a custom welcome message to new members in a designated channel.
- **GPT-4 Integration**: Interacts with users by responding to prompts using OpenAI's gpt-3.5-1106-turbo model.
- **DALL-E 3 Image Generation**: Generates images based on user prompts using OpenAI's DALL-E 3.
- **Rate Limit System**: Prevents abuse of moderator commands by limiting their usage to once every 30 seconds per user per server.
- **Birthday Releated**: The bot will @mention any user on their birthday in the designated #birthdays channel. Birthdays can be added to the bday database via commands through the bot

## Utilizing The Bot

### Adding the Bot to Your Server

To add KaydonBot to your Discord server, follow these steps:

1. **Navigate to the Discord Authorization URL**: [Add KaydonBot to Discord](https://kaydonbot.xyz/invite.html)
2. **Select Your Server**: Choose the server where you want to add the bot.
3. **Grant Required Permissions**: Make sure to grant all necessary permissions for the bot to function correctly.

> Note: You need to have the 'Administrator' permission on the server to add the bot. The bot requires 'Administrator' permissions.

### Support Server

If you need assistance or have any questions about Kaydonbot, feel free to join our [support server](https://discord.gg/Ht4tugQPQM).

### Bot Website

You can find more information about the bot on our [website](https://kaydonbot.xyz).

## Working With The Code

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kaydonbob03/Kaydonbot.git
   ```
2. **Navigate to the Bot Directory**:
   ```bash
   cd Kaydonbot
   ```
3. **Install Dependencies**:
   Make sure you have Python 3.x installed and then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   Similarly set the other required API keys
2. **Discord Bot Token**:
   Add your Discord bot token in the bot script or as an environment variable.

### Usage

Run the bot using the following command:
```bash
python kaydonbotv2.py
```

### Contributing

Contributions to Kaydonbot are welcome! Please feel free to submit pull requests or open issues to discuss proposed changes or report bugs.

## License

This code is licensed under the GPL-3.0 License (GNU GENERAL PUBLIC LICENSE). More info can be found in the LICENSE file

## Contact

For any queries or support, please send a message in the #support channel or open as ticket in our [support server](https://discord.gg/Ht4tugQPQM)

---

> Note: This bot uses OpenAI's GPT-3.5-turbo models and DALL-E 3, which are subject to OpenAI's usage policies and limitations.
