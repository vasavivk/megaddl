import telebot
import re
from mega_info_api import get_mega_info

bot = telebot.TeleBot('6450639403:AAFgYcw01RDsEH-A2kRM4Q_Th0-RXqtJUVQ')

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, "Hello! Send me a MEGA file link and I'll provide Name,Direct Link,Size")

@bot.message_handler(func=lambda message: True)
def check_link(message):
  text = message.text
  if ("http" and "mega" in text) and ("folder" not in text):
    url = text.split()[0]
    try:
        name, dl, size = get_mega_info(url)
        response = f"*Name:* `{name}`\n*Size:* `{size}`\n*Ditect Link:* ```{dl}```"
        bot.reply_to(message, response, parse_mode="Markdown")
    except Exception as e:
        response = f"An error occurred while processing the URL: {str(e)}"
        bot.reply_to(message, response)
  else:
    bot.reply_to(message, "Enter Correct Mega.nz file url format")


bot.polling()
