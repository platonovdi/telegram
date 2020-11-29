from bs4 import BeautifulSoup
import requests
import bs4
import re
import telebot


bot = telebot.TeleBot(
    '1409772665:AAEN51HJfieV1HEZfPtb5idLx8e6FDW78dc', parse_mode=None)
URL = ['https://www.rbc.ru/crypto/currency/btcusd',
       'https://quote.rbc.ru/ticker/59111']
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}


@bot.message_handler(commands=['help'])
def send_welcome(message):
    # bot.reply_to(message, "Howdy, how are you doing?")
    # bot.send_message(message.chat.id, 'Hello')
    bot.send_message(message.chat.id, '/help\n/btc\n/usd')


@bot.message_handler(commands=['usd'])
def usd(message):
    full_page = requests.get(URL[1], headers=HEADERS)
    page = full_page.text.encode('utf-8')
    soup = bs4.BeautifulSoup(page, 'html.parser')
    rub = soup.find(
        'div', {'class': 'chart__info__row js-ticker', 'data-currency': "₽"}
    )
    pattern = re.compile(r'\d\d,\d\d\d')
    rub_final = re.findall(pattern, str(rub.text.encode('utf-8')))
    # print(float(rub_final[0].replace(',', '.')))
    one_usd_to_rub = float(rub_final[0].replace(',', '.'))
    bot.send_message(
        message.chat.id, f'1$ ➙ {one_usd_to_rub}₽')


@ bot.message_handler(commands=['btc'])
def btc(message):
    full_page = requests.get(URL[0], headers=HEADERS)
    soup = bs4.BeautifulSoup(full_page.text, 'html.parser')
    usd = soup.find_all(
        'div', {'class': 'chart__subtitle js-chart-value'}, limit=1
    )
    pattern = re.compile(r'\d\d \d\d\d')
    usd = re.findall(pattern, str(usd[0]))
    usd = int(str(usd[0]).replace(' ', ''))
    bot.send_message(message.chat.id, f'1 BTC ➙ {usd}$')


# print(btc)
bot.polling()
