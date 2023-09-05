import telebot
from config import keys, TOKEN
from classes import ConversionException, CashConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f'Здравствуйте {message.chat.first_name}.\n' \
           'Вас приветствует бот для конвертации валют.\n' \
           'Информация об актуальныйх ценах взята с сайта - \n' \
           'https://cryptocompare.com\n' \
           'Чтобы получить подробную инструкцию введите команду -\n "/help"'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы сконвертировать одну валюту в другую,\n' \
           'необходимо ввести запрос в формате:\n' \
           '"Наименование валюты" <пробел> \n' \
           '"Валюта в которую необходимо перевести" <пробел> \n' \
           '"Количество переводимой валюты". ' \
           'Одной строкой, маленькими буквами.\n' \
           'Чтобы узнать список доступных валют введите команду -\n"/values"'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException('Параметров должно быть 3!\n'
                                      'Валюта из которой конвертируем => в которую переводим => количество.')

        quote, base, amount = values

        total_base = CashConverter.convert(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        summ = float(total_base) * float(amount)

        text = f'Цена {amount} {quote} в {base} - {summ}.'
        bot.send_message(message.chat.id, text)

bot.polling()