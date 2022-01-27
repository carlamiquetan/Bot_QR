from fileinput import filename
from lib2to3.pgen2.pgen import generate_grammar
from lib2to3.pytree import generate_matches
from socket import timeout
from sre_constants import CH_LOCALE
from tokenize import generate_tokens
import qrcode
import os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from telegram import ChatAction

INPUT_TEXT = 0
def start(update, context):
    
    update.message.reply_text("Hola bienvenido, que deseas hacer? \n\n Usa /qr para generar un codigo qr")

def qr_commandhandler(update, context):
 update.message.reply_text("Enviame un texto para transformarlo en un código qr")
 return INPUT_TEXT


def generate_qr(text):
    filename = text + ".jpg"
    img = qrcode.make(text)
    img.save(filename)
    return filename


def send_qr(filename, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    chat.send_photo(
        photo = open(filename, 'rb')
    )
    
    os.unlink(filename)


def input_text(update,contex):
    text=update.message.text

    filename = generate_qr(text)
    chat = update.message.chat
    send_qr(filename,chat)
    return ConversationHandler.END

if __name__ == '__main__':

    updater = Updater(token='', use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(ConversationHandler(
    
    entry_points=[
        CommandHandler("qr",qr_commandhandler)
    ],
    states={
        INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
    },
    fallbacks = []
    
    ))
   
    updater.start_polling()

    updater.idle()
