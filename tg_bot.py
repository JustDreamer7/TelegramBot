# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press Ctrl+F8 to toggle the breakpoint.
import geopy
import telebot
import requests
import datetime
import time
import sqlalchemy
from config.launch_db import connect_to_db
from config.structure_db import Users, Messages
from config.local_settings import binance_api_key, binance_secret_key, telegram_key, mapquest_api
from binance_exchange_rate import ExchangeRate

bot = telebot.TeleBot(telegram_key)
chg_rate = ExchangeRate(binance_api_key, binance_secret_key)
# test_bot = TelegramClient('bot', 17091113, '03e6bcd5c30d2d1536772bfad2bd363d').start(bot_token=telegram_key)

response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
unparsed_content = response.json()

geolocator = geopy.Nominatim(user_agent=mapquest_api)


def get_keyboard():
    main_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_rate = telebot.types.KeyboardButton("💰 Курс валют")
    item_crypto_rate = telebot.types.KeyboardButton("💰 Курс криптовалюты")
    item_geopos = telebot.types.KeyboardButton("Где я?", request_location=True)
    main_markup.add(item_rate)
    main_markup.add(item_crypto_rate)
    main_markup.add(item_geopos)
    return main_markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    db_session = connect_to_db()
    bot.send_message(message.chat.id, "Приветствую, делайте со мной, что хотите", reply_markup=get_keyboard())
    try:
        reg_date = time.localtime(message.date)
        new_record = Users(user_id=message.chat.id, user_name=message.chat.username,
                           registration_date=datetime.datetime(reg_date.tm_year, reg_date.tm_mon, reg_date.tm_mday,
                                                               reg_date.tm_hour, reg_date.tm_min, reg_date.tm_sec))
        db_session.add(new_record)
        db_session.commit()
        print('Copied')
    except sqlalchemy.exc.IntegrityError:
        db_session.rollback()
        print('Ошибка')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(message)
    db_session = connect_to_db()
    try:
        reg_date = time.localtime(message.date)
        new_record = Messages(message_id=message.message_id,
                              message_text=message.text, sender=message.chat.username,
                              sending_time=datetime.datetime(reg_date.tm_year, reg_date.tm_mon, reg_date.tm_mday,
                                                             reg_date.tm_hour, reg_date.tm_min, reg_date.tm_sec),
                              has_location=bool(message.location), has_contact=bool(message.contact))
        db_session.add(new_record)
        db_session.commit()
        print('Copied')
    except sqlalchemy.exc.IntegrityError:
        db_session.rollback()
        print('Ошибка')
    if message.text.strip() == '💰 Курс валют':
        bitcoin_rate, btc_pricechanging_list = chg_rate.exchange_rate_btc()
        bot.send_message(message.chat.id,
                         f"BitCoin - {round(bitcoin_rate, 2)}, 12ч.({round(btc_pricechanging_list[0], 2)}), " +
                         f"1ч.({round(btc_pricechanging_list[1], 2)})\n" +
                         f'USD - {round(unparsed_content["Valute"]["USD"]["Value"], 2)}\n' +
                         f'EUR - {round(unparsed_content["Valute"]["EUR"]["Value"], 2)}\n' +
                         f'CNY - {round(unparsed_content["Valute"]["CNY"]["Value"], 2)}\n')
    elif message.text.strip() == '💰 Курс криптовалюты':
        # t1 = time.time()
        crypto_rate = chg_rate.run(chg_rate.exchange_rate_my_crypto_coins)
        crypto_pricechanging_list = chg_rate.run(chg_rate.historical_values)
        bot.send_message(message.chat.id,
                         f'ETH - {round(crypto_rate["ETHUSDT"], 3)}, 12ч.({round(crypto_pricechanging_list["ETHUSDT"][0], 3)}), ' +
                         f'1ч.({round(crypto_pricechanging_list["ETHUSDT"][1], 3)})\n' +
                         f'EGLD - {round(crypto_rate["EGLDUSDT"], 3)}, 12ч.({round(crypto_pricechanging_list["EGLDUSDT"][0], 3)}), ' +
                         f'1ч.({round(crypto_pricechanging_list["EGLDUSDT"][1], 3)})\n' +
                         f'XRP - {round(crypto_rate["XRPUSDT"], 3)}, 12ч.({round(crypto_pricechanging_list["XRPUSDT"][0], 3)}), ' +
                         f'1ч.({round(crypto_pricechanging_list["XRPUSDT"][1], 3)})\n' +
                         f'AVAX - {round(crypto_rate["AVAXUSDT"], 3)}, 12ч.({round(crypto_pricechanging_list["AVAXUSDT"][0], 3)}), ' +
                         f'1ч.({round(crypto_pricechanging_list["AVAXUSDT"][1], 3)})\n' +
                         f'SOL - {round(crypto_rate["SOLUSDT"], 3)}, 12ч.({round(crypto_pricechanging_list["SOLUSDT"][0], 3)}), ' +
                         f'1ч.({round(crypto_pricechanging_list["SOLUSDT"][1], 3)})\n' +
                         f'FTT - {round(crypto_rate["FTTUSDT"], 3)}, 12ч.({round(crypto_pricechanging_list["FTTUSDT"][0], 3)}), ' +
                         f'1ч.({round(crypto_pricechanging_list["FTTUSDT"][1], 3)})\n' +
                         f'WAVES - {round(crypto_rate["WAVESUSDT"], 3)}, 12ч.({round(crypto_pricechanging_list["WAVESUSDT"][0], 3)}), ' +
                         f'1ч.({round(crypto_pricechanging_list["WAVESUSDT"][1], 3)})\n' +
                         f'DOGE - {round(crypto_rate["DOGEUSDT"], 4)}, 12ч.({round(crypto_pricechanging_list["DOGEUSDT"][0], 4)}), ' +
                         f'1ч.({round(crypto_pricechanging_list["DOGEUSDT"][1], 4)})\n' +
                         f'ADA - {round(crypto_rate["ADAUSDT"], 3)}, 12ч.({round(crypto_pricechanging_list["ADAUSDT"][0], 3)}), ' +
                         f'1ч.({round(crypto_pricechanging_list["ADAUSDT"][1], 3)})\n' +
                         f'DOCK - {round(crypto_rate["DOCKUSDT"], 4)}, 12ч.({round(crypto_pricechanging_list["DOCKUSDT"][0], 4)}), ' +
                         f'1ч.({round(crypto_pricechanging_list["DOCKUSDT"][1], 4)})\n' +
                         f'ALICE - {round(crypto_rate["ALICEUSDT"], 3)}, 12ч.({round(crypto_pricechanging_list["ALICEUSDT"][0], 3)}), ' +
                         f'1ч.({round(crypto_pricechanging_list["ALICEUSDT"][1], 3)})\n')
        # print(time.time() - t1)
    elif message.text.strip() == 'Отправить геопозицию пользователю':
        msg = bot.reply_to(message, "Введите username пользователя")
        bot.register_next_step_handler(msg, save_ans)
        # updates = bot.get_updates()
        # print(updates)
    elif message.text.strip() == 'Вернутся к предыдущему меню':
        bot.send_message(message.chat.id, "Хорошо, но вы всегда можете передумать", reply_markup=get_keyboard())


def save_ans(message):
    db_session = connect_to_db()
    save_user = db_session.query(Users).filter_by(user_name=message.text).one()
    save_message_id = db_session.query(Messages).filter_by(sender=message.chat.username, has_location=True).order_by(
        sqlalchemy.desc(Messages.sending_time)).limit(1).scalar()
    print(save_message_id.message_id)
    print(save_user.user_id)
    bot.forward_message(save_user.user_id, message.chat.id, save_message_id.message_id)


@bot.message_handler(content_types=["location"])
def geopos(message):
    db_session = connect_to_db()
    bot.send_message(message.chat.id, geolocator.reverse(f"{message.location.latitude}, {message.location.longitude}"))
    try:
        reg_date = time.localtime(message.date)
        new_record = Messages(message_id=message.message_id,
                              message_text=message.text, sender=message.chat.username,
                              sending_time=datetime.datetime(reg_date.tm_year, reg_date.tm_mon, reg_date.tm_mday,
                                                             reg_date.tm_hour, reg_date.tm_min, reg_date.tm_sec),
                              has_location=bool(message.location), has_contact=bool(message.contact))
        db_session.add(new_record)
        db_session.commit()
        print('Copied')
    except sqlalchemy.exc.IntegrityError:
        db_session.rollback()
        print('Ошибка')
    print(message.message_id)
    markup_geo = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_geo = telebot.types.KeyboardButton("Отправить геопозицию пользователю")
    item_go_back = telebot.types.KeyboardButton("Вернутся к предыдущему меню")
    markup_geo.add(item_geo)
    markup_geo.add(item_go_back)
    bot.send_message(message.chat.id, "Xотите ли отправить ее кому-то?", reply_markup=markup_geo)


bot.polling(non_stop=True)
# class TgBot:
#     def __init__(self, bot, test):
#         self.bot = bot
#         self.test = test
#
#     bot = telebot.TeleBot(telegram_key)
#     test = ExchangeRate(binance_api_key, binance_secret_key)
#     @bot.message_handler(commands=['start'])
#     def send_welcome(self, message, bot):
#         markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
#         item1 = telebot.types.KeyboardButton("Курс валют")
#         item2 = telebot.types.KeyboardButton("В разработке")
#         markup.add(item1)
#         markup.add(item2)
#         bot.send_message(message.chat.id, "Приветствую, делайте со мной, что хотите", reply_markup=markup)
#
#     @bot.message_handler(content_types=["text"])
#     def handle_text(self, message, bot, test):
#         print(message)
#         if message.text.strip() == 'Курс валют':
#             answer = test.exchange_rate()
#             bot.send_message(message.chat.id, answer)
#
#
# test = TgBot(telebot.TeleBot(telegram_key),ExchangeRate(binance_api_key, binance_secret_key))
# print(type(test.bot))
# print(test.bot)
# test.bot.polling(none_stop=True)
