import os
import telebot
from googletrans import LANGUAGES, Translator

# Substitua 'YOUR_BOT_TOKEN' pelo token do seu bot
BOT_TOKEN = '6879949232:AAF_Uq8CaNKVoR6sdqYI03cAeXfA78BqO04'
bot = telebot.TeleBot(BOT_TOKEN)

translator = Translator()
user_messages = {}

def language_list():
    languages = {v: k for k, v in LANGUAGES.items()}
    return '\n'.join([f"*{k.capitalize()}* - `{v.upper()}`" for k, v in languages.items()])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Envie-me uma mensagem e eu vou traduzi-la para você.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id in user_messages:
        # Traduz a mensagem para o idioma escolhido
        dest_lang = text.lower()
        if dest_lang not in LANGUAGES:
            bot.reply_to(message, "Desculpe, eu não reconheço esse código de idioma. Por favor, tente novamente.")
            return
        src_text = user_messages[chat_id]
        translated_text = translator.translate(src_text, dest=dest_lang).text
        bot.reply_to(message, translated_text)
        del user_messages[chat_id]
    else:
        # Armazena a mensagem do usuário e pede o idioma de destino
        user_messages[chat_id] = text
        bot.reply_to(message, "Para qual idioma você gostaria de traduzir? Aqui estão as opções:\n\n" + language_list(), parse_mode='Markdown')

bot.polling()
