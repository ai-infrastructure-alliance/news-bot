import re
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlunparse

# Regex pattern for matching URLs
regex_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"


class NewsBot:

  def __init__(self, bot, id, linksdb):
    self.bot = bot
    self.chat_id = id
    self.linksdb = linksdb

  def send_info_message(self, message):
    markdown = f"""Hey *{message.from_user.first_name}*! 
Welcome to *AIIA News Bot*.

Throughout the week, you have to *add links* to the database. 
Simply send messages with links in this chat. I also accept comments.

Use */stats* to check the statistics of the bot.
Use */fresh* to get a list of recent links.
Use */help* to get a list of commands.
"""
    self.bot.reply_to(message, markdown, parse_mode="Markdown")
    print(f"[News] Info message is sent to {message.from_user.first_name}.")

  # Use */delete* to delete the link from the database in reply to a message with a link.

  def _parse_rows(self, message, news):
    n = 0
    for item in news:
      n += 1
      url = item.link.replace("*", "\\*").replace("_", "\\_")
      text = f"""*{n}*
*URL*: {url}
*Type*: {item.type}
*Title*: {item.title}"""
      self.bot.send_message(message.chat.id,
                            text,
                            parse_mode="Markdown",
                            disable_web_page_preview=True)
    self.bot.send_message(message.chat.id, "All links are sent.")

  def get_fresh_news(self, message):
    if message.chat.id == self.chat_id:
      framestart = datetime.now() - timedelta(days=7)
      news = self.linksdb.retrieve_from(framestart)
      if news:
        text = f"Here are all links received after {framestart.isoformat()}:"
        self.bot.reply_to(message, text)
        self._parse_rows(message, news)
      else:
        self.bot.reply_to(message, "Sorry, no links found.")
      print(f"[News] A list is sent to {message.from_user.first_name}.")
    else:
      self.bot.reply_to(message,
                        "Sorry, you are not authorized to use the bot.")
      print(f"[News] Unauthorized access from {message.from_user.username}.")

  def delete(self, message):
    if message.chat.id == self.chat_id:
      if message.reply_to_message:
        reply_message = message.reply_to_message
        if reply_message.text:
          text = reply_message.text
          url_match = re.search(regex_pattern, text)
          if url_match:
            url = url_match.group(0)
            link_data = (url, )
            self.linksdb.delete_link(link_data)
            self.bot.reply_to(message, f"Link {url} is deleted.")
          else:
            self.bot.reply_to(message, "Sorry, no link found.")
        else:
          self.bot.reply_to(message, "Sorry, no link found.")
    else:
      self.bot.reply_to(message,
                        "Sorry, you are not authorized to use the bot.")
      print(f"[News] Unauthorized access from {message.from_user.username}.")

  def read_any(self, message):
    if message.chat.id == self.chat_id:
      input_text = message.text
      url_match = re.search(regex_pattern, input_text)
      if url_match:
        url = url_match.group(0)
        pre_text = input_text[:url_match.start()]
        post_text = input_text[url_match.end():]
        comment = (pre_text + " " + post_text).strip()
        url = self.clean_url(url)
        added = self.linksdb.add_link(url, comment,
                                      message.from_user.first_name)
        if added:
          self.bot.reply_to(message,
                            "Thank you, the link is added to the database.")
        else:
          self.bot.reply_to(message, "The link is already in the database.")
      else:
        self.bot.reply_to(message, "Sorry, no URL found in the message.")
      print(f"[News] Link is added by {message.from_user.first_name}.")
    else:
      self.bot.reply_to(message,
                        "Sorry, you are not authorized to use the bot.")
      print(f"[News] Unauthorized access from {message.from_user.username}.")

  def stats(self, message):
    if message.chat.id == self.chat_id:
      news = self.linksdb.get_all()
      text = f"""Current Frame stats:
*Number of news in DB*: {len(news)}
*Number of missing titles:* {len([x for x in news if not x.title])}
*Number of missing summaries:* {len([x for x in news if not x.summary])}
"""
      self.bot.send_message(message.chat.id, text, parse_mode="Markdown")
    else:
      self.bot.reply_to(message,
                        "Sorry, you are not authorized to use the bot.")
      print(f"[News] Unauthorized access from {message.from_user.username}.")

  def clean_url(self, url):
    parsed_url = urlparse(url)
    cleaned_url = parsed_url._replace(query="")
    return urlunparse(cleaned_url)
