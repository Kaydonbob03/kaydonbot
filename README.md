# Kaydonbotv2 Discord Bot

KaydonBotV2 is a Discord bot designed to enhance the functionality and interactivity of Discord servers. It integrates features like greeting new members, responding to user prompts using GPT-3.5, and generating images with DALL-E 3.

## Features

- **Welcome Messages**: Sends a custom welcome message to new members in a designated channel.
- **GPT-3.5 Integration**: Interacts with users by responding to prompts using OpenAI's GPT-3.5 model.
- **DALL-E 3 Image Generation**: Generates images based on user prompts using OpenAI's DALL-E 3.

## Installation

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

## Configuration

1. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
2. **Discord Bot Token**:
   Add your Discord bot token in the bot script or as an environment variable.

## Usage

Run the bot using the following command:
```bash
python kaydonbotv2.py
```

## Contributing

Contributions to KaydonBotV2 are welcome! Please feel free to submit pull requests or open issues to discuss proposed changes or report bugs.

## License

[MIT License](LICENSE)

## Contact

For any queries or support, please contact [Your Contact Information].

---

> Note: This bot uses OpenAI's GPT-3.5 and DALL-E 3, which are subject to OpenAI's usage policies and limitations.