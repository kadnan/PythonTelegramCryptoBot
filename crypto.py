# import datetime
from datetime import datetime

from config import TOKEN
from telegram.ext import Updater, CommandHandler
from yf import get_ticker_info

USAGE = '/ticker <SYMBOL>: For example: /ticker BTC or /ticker ETH'


def start(update, context):
    print('Calling Start Command')
    update.message.reply_text(USAGE)


def ticker_command(update, context):
    symbol = ''

    print('Calling Price Command')

    if len(context.args) == 1:
        symbol = context.args[0]
        result = get_ticker_info(symbol)

    if len(result) > 0:
        result = result[0]
        graph_up = u'\U0001F4C8'
        graph_down = u'\U0001F4C9'
        trend = ''
        percent_change = float(round(result['regularMarketChangePercent']))

        if percent_change > 0:
            trend = graph_up
        else:
            trend = graph_down

        quote_url = 'https://finance.yahoo.com/quote/{}-USD'.format(symbol)

        msg = '<strong><a href="{}">{}-USD:- {:,}</a>{}</strong>'.format(quote_url,
                                                                         symbol, result['regularMarketPrice'], trend)
        msg += '\n<strong>Open:</strong> {:,}'.format(result['regularMarketOpen'])
        msg += '\n<strong>High:</strong> {:,}'.format(result['regularMarketDayHigh'])
        msg += '\n<strong>Low:</strong> {:,}'.format(result['regularMarketDayLow'])
        msg += '\n<strong>Close:</strong> {:,}'.format(result['regularMarketPreviousClose'])
        msg += '\n<strong>Volume:</strong> {:,}'.format(result['regularMarketVolume'])
        msg += '\n<strong>Percentage Change:</strong> {}%'.format(percent_change)
        msg += '\n<strong>Time:</strong> {}'.format(datetime.fromtimestamp(result['regularMarketTime']))
        msg += '\n\n <i>Powered by Yahoo Finance!</i>'
        update.message.reply_text(msg, parse_mode='html', disable_web_page_preview=True)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ticker", ticker_command))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
