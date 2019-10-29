import logging
from ChatType import ChatType
from DBHelper import DBHelper
from Game import Game
from Field import Field

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

db = DBHelper()


def start(update, context):
    group_members_amount = context.bot.get_chat_members_count(update.message.chat_id)
    if group_members_amount <= 3:
        chat_type = ChatType(group_members_amount - 2)
        admin_id = context.bot.getChat(update.message.chat_id).get_administrators()[0].user.id
        if chat_type.value == ChatType.PVE:
            second_player_id = -1
            last_game = db.get_last_game(admin_id, -1)
            if last_game is None:
                last_game = Game(Field(), admin_id, second_player_id)
                db.update_last_game(last_game)
            custom_keyboard = last_game.field.toPrint()
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            context.bot.send_message(update.message.chat_id, 'test', reply_markup=reply_markup)
        else:
            pass
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
