from controller.Controller import Controller
from view.View import View


def main():
    file = open("token.txt", "+r")
    TOKEN = file.readline()
    control = Controller()
    view = View(control, str(TOKEN).split()[0])
    view.run()

main()
