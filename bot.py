import telebot
from app import *

bot = telebot.TeleBot("<token>", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message("<chat_id>", """
/priceDop   : check price DOPPLE
/priceTwin  : check price TWIN
/reward     : check reward from diamon hand
    """)

@bot.message_handler(commands='priceDop')
def send_welcome(message):
    bot.send_message("<chat_id>", "dop price => " + dopPrice)

@bot.message_handler(commands='priceTwin')
def send_welcome(message):
    bot.send_message("<chat_id>", "twin price => " + twinPrice)

@bot.message_handler(commands='reward')
def send_welcome(message):
    bot.send_message("<chat_id>", "reward => " + dopReward + " DOP")

bot.polling()