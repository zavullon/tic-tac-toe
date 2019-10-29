import logging
from ChatType import ChatType

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    group_members_amount = context.bot.get_chat_members_count(update.message.chat_id)
    if group_members_amount <= 3:
        chat_type = ChatType(group_members_amount - 2)
        update.message.reply_text(chat_type.value)
    else:
        update.message.reply_text('you can only play with 1 friend, which can be the bot itself by the way')


def help(update, context):
    update.message.reply_text('/start to start a game with bot'
                              'or add this bot to chat group with you and the person you want to challenge '
                              'and enter /start')


def move(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater("960888759:AAECyatQetOLUPB660SEJfvc8LUdOUffS4A", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, move))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
