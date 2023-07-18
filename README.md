# AIIA News Telegram Bot

This is a very simple Telegram Bot which help collecting links for a newsletter.

You can use the Newsletter Assistant without it, directly adding links to an AirTable base, 
but this bot makes it easier to add links from Telegram.

## How to use it

### Setup the Telegram Bot

1. Create a Telegram Bot using the [BotFather](https://core.telegram.org/bots#6-botfather)
2. Add the bot to a Telegram group where you and your colleges will send links to it;
as bot is reading all messages, you'll have to create a dedicated group for it. 
    - To allow a bot to read all messages, use BotFather command `/setprivacy` and set it to `Disabled`.
    - To allow a bot to be added in a group, use BotFather command `/setjoingroups` and set it to `Enabled`.
    - After you add a bot in a group, you can use `/setjoingroups` again to set it to `Disabled` again.
3. When the bot is in the group, run `/start` command in the group to get the chat id.

### Setup the AirTable base

Unfortunately, AirTable doesn't provide an API to create a base, so you'll have to do it manually.

1. Create a new [AirTable](https://airtable.com/) base
2. Create an AirTable table `Weekly newsletter` in that base with the following fields:
    - `URL` (Primary, URL)
    - `Type` (Single select: 'post', 'paper', 'project', 'youtube', 'twitter', 'reddit')
    - `Title` (Single line text)
    - `Summary` (Long text)
    - `Comment` (Long text)
3. If you prefer to call your table differently, change the name in the `news_bot_runner.py` file.

### Setup the project

1. If you plan to test it locally, create a `.env` file with the following content:
```
BOT_TOKEN_NEWS=<the bot token, you get it on bot creation>
NEWS_CHAT_ID=<the id of the chat you'll use your bot in>
AIRTABLE_API_KEY=<API key in Airtable>
BASE_ID=<Base ID in Airtable; to get it, click Help | API Documentation in your base>
```

2. The project is desinged to be deployed on Heroku. Add the corresponding environment variables to your Heroku app.
