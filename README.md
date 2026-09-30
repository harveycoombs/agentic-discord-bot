<p align="center"><img src="https://www.agenti.bot/images/icon.png?v=2" width="105" /></p>

# AgentiBot &middot; [agenti.bot]([https://www.agenti.bot/](https://www.agenti.bot/))

AgentiBot is an agentic AI Discord bot.

## Purpose
AgentiBot can manage just about any aspect of your server. From moderation to server customisation, AgentiBot makes the perfect moderator or administrator. As for how to use AgentiBot, simply ask it to do something (examples: `Give me the Green role`, `Create a channel called gaming and make it private to the gaming role`), and it will oblige.

## Setup
If you wish to run AgentiBot yourself, follow the instructions below.

> Note: Python 3.12 is the recommended Python version for running AgentiBot

### 1. Create a .env file in the root of the repository
Follow the structure provided below, with your own credentials.
```
TOKEN=
APPLICATION_ID=
EMBED_COLOR=

SUPABASE_URL=
SUPABASE_KEY=
```

### 2. Create & enter a virtual environment
Run the command `python3 -m venv .venv` and then either `source .venv/bin/activate` for Mac & Linux, or `.venv/Scripts/activate` for Windows.

### 3. Install dependencies
Once inside the virtual environment, run the command `pip install -r requirements.txt`.

### 4. Running AgentiBot
Once you have completed the above, run `python src/agentibot.py` from the project root to start.

Thank you for using AgentiBot! Please consider donating by [clicking here](https://buymeacoffee.com/harveycoombs).

&ndash; [Harvey Coombs](https://www.harveycoombs.com/)
