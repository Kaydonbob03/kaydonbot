# Kaydonbot Discord Bot

KaydonBot is a Discord bot designed to enhance the functionality and interactivity of Discord servers. It integrates features like greeting new members, responding to user prompts using GPT-4-turbo, and generating images with DALL-E 3. It also has a wide assortment of moderation commands and botgames!

## Features

- **Welcome Messages**: Sends a custom welcome message to new members in a designated channel.
- **GPT-4 Integration**: Interacts with users by responding to prompts using OpenAI's gpt-4-1106-preview model.
- **DALL-E 3 Image Generation**: Generates images based on user prompts using OpenAI's DALL-E 3.

## Utilizing The Bot

### Adding the Bot to Your Server

To add KaydonBot to your Discord server, follow these steps:

1. **Navigate to the Discord Authorization URL**: [Add KaydonBot to Discord](https://discord.com/api/oauth2/authorize?client_id=1181143854959837184&permissions=8&scope=bot+applications.commands)
2. **Select Your Server**: Choose the server where you want to add the bot.
3. **Grant Required Permissions**: Make sure to grant all necessary permissions for the bot to function correctly.

> Note: You need to have the 'Administrator' permission on the server to add the bot. The bot requires 'Administrator' permissions.

### Support Server

If you need assistance or have any questions about KaydonBotV2, feel free to join my server! It was originally just my server for content creation, but I am going to include my development stuff there as well until my bot or any development stuff gets bug enough to require its own server. The channels for development things can be accessed without requiring to verify subscription to my youtube channel and stuff :). You can join here: [Kaydonbob03 Server](https://discord.com/invite/qbVJ6G2)

## Working With The Code

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kaydonbob03/KaydonBotV2.git
   ```
2. **Navigate to the Bot Directory**:
   ```bash
   cd KaydonBotV2
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
2. **Discord Bot Token**:
   Add your Discord bot token in the bot script or as an environment variable.

### Usage

Run the bot using the following command:
```bash
python kaydonbotv2.py
```

### Contributing

Contributions to KaydonBot are welcome! Please feel free to submit pull requests or open issues to discuss proposed changes or report bugs.

## License

The License can be found in the LICENSE file

## Contact

For any queries or support, please contact [Kayden Cormier](MAILTO:Kaydonbob03@gmail.com).

---

> Note: This bot uses OpenAI's GPT-4 models and DALL-E 3, which are subject to OpenAI's usage policies and limitations.
