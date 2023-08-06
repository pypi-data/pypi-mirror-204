import telepot
from telepot.loop import MessageLoop

bot = telepot.Bot('6093409606:AAGLWUuUDzirhfpCu3mpgO9fZGGuJZBqGHQ')

def all(text):
    try:
        bot.sendMessage(-1001921187107, text)
    except:
        pass