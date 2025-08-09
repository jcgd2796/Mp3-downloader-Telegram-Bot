from controller.Controller import Controller
from view.View import View
import logging
logger = logging.getLogger('MP3Downloader')



def main():
    logging.basicConfig(filename='MP3Downloader.log')
    file = open("token.txt", "+r")
    TOKEN = file.readline()
    control = Controller()
    view = View(control, str(TOKEN).split()[0])
    view.run()

main()
