"""view.py
Main file of the bot. Acts as the view to interact with Telegram chats, connects with the controller.
Author:
    Jcgd2796"""
import os
import telegram.error
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters
from controller.Controller import Controller

logger = logging.getLogger('MP3Downloader')
class View:
    def __init__(self, c: Controller, t: str):
        self.controller = c
        self.TOKEN = t
        self.application = ApplicationBuilder().token(self.TOKEN).build()

    def run(self):
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('download', self.download))
        self.application.add_handler(CommandHandler('help', self.help))
        self.application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.unknown))
        self.application.run_polling()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            'Hello!\n'
            'Available options: \n'
            '\t /download <url>: Downloads the <url> video as an mp3 and sends it to the chat. Url must have the '
            'following format: \'https://youtu.be/<vid>\'\n '
            '\t /help: Displays available commands\n'
            'Please remember this bot shouldn\'t be used to break copyright laws')

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            'Available options: \n'
            '\t /download <url>: Downloads the <url> video as an mp3 and sends it to the chat. Url must have the '
            'following format: \'https://youtu.be/<vid>\'\n '
            '\t /help: Displays this help message')

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            f"Sorry '{update.message.text}' is not a valid command")

    async def download(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            file = None
            url = update.message.text.split(" ")[1]
            await update.message.reply_text("URL received")
            if not url.startswith("https://youtu.be/"):
                await update.message.reply_text("The URL " + url + " is not valid. Allowed URLs must begin with \"https://youtu.be/\"")
            else:
                await update.message.reply_text("Downloading " + url)
                file = self.controller.download(url)
                await update.message.reply_text("Download finished")
                with open(os.path.join(os.path.dirname(__file__), '..', 'downloads', file), 'rb') as audio_file:
                    await update.message.reply_audio(audio=audio_file)
        except telegram.error.NetworkError:
            await update.message.reply_text("File is too large. Can't send files over 50 MB")
        except Exception as ex:
            await update.message.reply_text("An error has occurred, please tell my owner")
            logger.exception(traceback.format_exc())
            return
        finally:
            if (file != None):
                self.controller.delete(file)
            
