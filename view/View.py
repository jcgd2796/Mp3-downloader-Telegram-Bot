"""view.py
Main file of the bot. Acts as the view to interact with Telegram chats, connects with the controller.
Author:
    Jcgd2796"""
from __future__ import unicode_literals
import re

import telegram.error
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from controller.Controller import Controller


class View:
    controller = None
    TOKEN = None
    updater = None

    def __init__(self, c: Controller, t:str):
        self.controller = c
        self.TOKEN = t
        self.updater = Updater(self.TOKEN, use_context=True)

    def run(self):
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CommandHandler('download', self.download))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.unknown))
        self.updater.start_polling()

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'Hello!\n'
            'Available options: \n'
            '\t /download <url>: Downloads the <url> video as an mp3 and sends it to the chat. Url must have the '
            'following format: \'https://youtu.be/<vid>\'\n '
            '\t /help: Displays available commands'
            'Please remember this bot shouldn\'t be used to break copyright laws')

    def help(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'Available options: \n'
            '\t /download <url>: Downloads the <url> video as an mp3 and sends it to the chat. Url must have the '
            'following format: \'https://youtu.be/<vid>\'\n '
            '\t /help: Displays this help message')

    def unknown(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text)

    def download(self, update: Update, context: CallbackContext):
        try:
            url = update.message.text.split(" ")
            update.message.reply_text("URL received")
            if not re.match("https://youtu.be/", url[1]):
                update.message.reply_text("The URL " + url[1] + "is not valid. Allowed URLs must begin with "
                                                                "\"https://youtu.be/\"")
            else:
                update.message.reply_text("Downloading " + url[1])
                file = self.controller.download(url[1])
                update.message.reply_text("Download finished")
                update.message.reply_audio(audio=open("../downloads/" + file, 'rb'), timeout=300)
                self.controller.delete(file)
        except telegram.error.NetworkError:
            update.message.reply_text("File is too large. Can't send files over 50 MB")
        except Exception as ex:
            update.message.reply_text("An error has occurred, please tell my owner")
            print(ex)
            return
