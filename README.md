# Agentic Discord Bot

An agentic AI Discord bot.

## Purpose
This bot can manage just about any aspect of your server, from moderation to server customisation. As for how to use it, simply ask it to do something (examples: `Give me the Green role`, `Create a channel called gaming and make it private to the gaming role`), and it will oblige.

## Setup
If you wish to run this bot yourself, follow the instructions below.

> Note: Python 3.12 is the recommended Python version

### 1. Create a .env file in the root of the repository
Follow the structure provided below, with your own credentials.
```
TOKEN=
APPLICATION_ID=
EMBED_COLOR=

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
XAI_API_KEY=
```

### 2. Create & enter a virtual environment
Run the command `python3 -m venv .venv` and then either `source .venv/bin/activate` for Mac & Linux, or `.venv/Scripts/activate` for Windows.

### 3. Install dependencies
Once inside the virtual environment, run the command `pip install -r requirements.txt`.

### 4. Running the bot
Once you have completed the above, run `python src/bot.py` from the project root to start.

Thank you for using my bot! Please consider donating by [clicking here](https://buymeacoffee.com/harveycoombs).

&ndash; [Harvey Coombs](https://www.harveycoombs.com/)
