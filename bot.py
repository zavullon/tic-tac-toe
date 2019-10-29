import logging
from ChatType import ChatType
from DBHelper import DBHelper
from Game import Game
from Field import Field
from SquareValue import SquareValue

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

db = DBHelper()


def start(update, context):
    group_members_amount = context.bot.getChat(update.message.chat_id).get_members_count()
    if group_members_amount <= 3:
        chat_type = ChatType(group_members_amount - 2)
        admins = context.bot.getChat(update.message.chat_id).get_administrators()
        first_player_id = update.message.from_user.id
        second_player_id = 0
        if chat_type == ChatType.PVE:
            second_player_id = -1
        elif chat_type == ChatType.PVP and len(admins) == 2:
            second_player_id = admins[0].user.id if admins[0].user.id != first_player_id else admins[1].user.id
        else:
            update.message.reply_text('in order to play you should make you partner an admin of this chat')
            return
        last_game = db.get_last_game(first_player_id, second_player_id)
        if last_game is None:
            last_game = Game(Field(), first_player_id, second_player_id)
            db.update_last_game(last_game)
        custom_keyboard = last_game.field.toPrint()
        reply_markup = telegram.InlineKeyboardMarkup(custom_keyboard)
        context.bot.send_message(update.message.chat_id, update.message.from_user.username + "'s turn",
                                 reply_markup=reply_markup)
    else:
        update.message.reply_text('you can only play with 1 friend, which can be the bot itself by the way')


def help(update, context):
    update.message.reply_text('/start to start a game with bot'
                              'or add this bot to chat group with you and the person you want to challenge '
                              'and enter /start')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def button(update, context):
    query = update.callback_query
    group_members_amount = context.bot.getChat(query.message.chat_id).get_members_count()
    if group_members_amount <= 3:
        chat_type = ChatType(group_members_amount - 2)
        admins = context.bot.getChat(query.message.chat_id).get_administrators()
        first_player_id = query.from_user.id
        second_player_id = 0
        if chat_type == ChatType.PVE:
            second_player_id = -1
        elif chat_type == ChatType.PVP and len(admins) == 2:
            second_player_id = admins[0].user.id if admins[0].user.id != first_player_id else admins[1].user.id
        else:
            context.bot.send_message(query.message.chat_id, 'in order to play you should make you partner an admin of this chat')
            return
        last_game = db.get_last_game(first_player_id, second_player_id)
        if (SquareValue(last_game.next_move.value) == SquareValue.CIRCLE and query.from_user.id == last_game.circle_id) or (
                SquareValue(last_game.next_move.value == SquareValue.CROSS) and query.from_user.id == last_game.cross_id):
            last_game.move(int(query.data))
            db.update_last_game(last_game)
            custom_keyboard = last_game.field.toPrint()
            reply_markup = telegram.InlineKeyboardMarkup(custom_keyboard)
            context.bot.send_message(query.message.chat_id, query.from_user.username + "'s turn",
                                    reply_markup=reply_markup)
        #context.bot.send_message(query.message.chat_id, str(query.data))


def main():
    updater = Updater("960888759:AAECyatQetOLUPB660SEJfvc8LUdOUffS4A", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
