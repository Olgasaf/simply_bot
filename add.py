import telebot

from Utils import CryptoConverter, APIException
from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    text = "Привет! Я RedDeerBot-котвертер валют и я могу:  "\
    "\n- Показать список доступных валют через команду /values "\
    "\n- Провести конвертацию валюты при Вашем вводе : <название вашей валюты> <в какую валюту перевести> <количество переводимой валюты>"\
    "\n- Напомнить, что я могу через команду /help ."
    bot.reply_to(message, text)

@bot.message_handler(commands=["help"])
def help(message: telebot.types.Message):
    text = "- Для конвертации введите Ваши данные в следующем формате: \n "\
           " <название вашей валюты> <в какую валюту перевести> <количество переводимой валюты> ."
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Список доступных валют: "
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text"])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException("Извините, слишком много данных.")
        elif len(values) < 3:
            raise APIException("Извините, слишком мало данных.")

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e :
        bot.reply_to(message, f"Внимание, Вы ошиблись\n{e}.")

    except Exception as e :
        bot.reply_to(message, f"Не удалось обработать команду\n{e}.")

    else:
        x = float(amount)
        text = f"Стоимость {amount} {quote} в {base} равна {total_base*x} ."
        bot.send_message(message.chat.id, text)


bot.polling()




