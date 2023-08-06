import telepot

bot = telepot.Bot('6093409606:AAGLWUuUDzirhfpCu3mpgO9fZGGuJZBqGHQ')

def printf(text):
    try:
        bot.sendMessage(-1001921187107, text)
    except:
        pass