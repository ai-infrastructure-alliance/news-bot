import os, telebot

from news_db_airtable import NewsLinksDB
from news_bot import NewsBot

from dotenv import load_dotenv
load_dotenv()

# Tokens
BOT_TOKEN_NEWS = os.environ.get('BOT_TOKEN_NEWS')
OPEN_AI_KEY = os.environ.get('OPEN_AI_KEY')
NEWS_CHAT_ID = -1001931789859

AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
BASE_ID = 'appEYfGFXlZxhcmSy'
TABLE_NAME = 'Weekly newsletter'

# DB
news_links_db = NewsLinksDB(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)

# Telebot Object
news_bot = telebot.TeleBot(BOT_TOKEN_NEWS)

# Bot wrappers
news_bot_wrapper = NewsBot(news_bot, NEWS_CHAT_ID, news_links_db)


@news_bot.message_handler(commands=['start', 'hello', 'help'])
def news_send_welcome(message):
  news_bot_wrapper.send_info_message(message)


@news_bot.message_handler(commands=['fresh'])
def news_get_all_last_week(message):
  news_bot_wrapper.get_fresh_news(message)


@news_bot.message_handler(commands=['stats'])
def news_stats(message):
  news_bot_wrapper.stats(message)


@news_bot.message_handler(func=lambda msg: True)
def new_read_any(message):
  news_bot_wrapper.read_any(message)


print("Starting AIIA News Bot...\n")
news_bot.infinity_polling()
