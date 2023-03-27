import socket


class TelegramNotification:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send(self, message):
        if self.token is None or self.chat_id is None:
            print("{Local}: " + message)
            return
        send_noti_to_telegram(message, self.token, self.chat_id)


def send_noti_to_telegram(message, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID):
    try:
        import telegram
    except ImportError:
        print(
            "telegram package is not installed. "
            + "please install the package by executing $ pip install python-telegram-bot"
        )
        return
    except Exception as e:
        print("sending message failed", e)
        return

    print(message)

    try:
        token = TELEGRAM_TOKEN
        chat_id = TELEGRAM_CHAT_ID
        bot = telegram.Bot(token=token)
        bot.sendMessage(chat_id=chat_id, text=f"[{socket.gethostname()}]\n{message}")
    except KeyError:
        print("TELEGRAM_TOKEN or TELEGRAM_CHAT_ID is not set")
        pass
    except Exception as e:
        print("Sending message failed: ", e)
        return


# def send_noti_to_teams(message):
#     try:
#         import pymsteams
#     except ImportError:
#         print('pymsteams package is not installed. ' +
#               'please install the package by executing $ pip install pymsteams')
#         return
#     except Exception as e:
#         print('sending message failed', e)
#         return
#
#     try:
#         token = os.environ['TELEGRAM_TOKEN']
#         chat_id = os.environ['TELEGRAM_CHAT_ID']
#         bot = telegram.Bot(token=token)
#         bot.sendMessage(chat_id=chat_id, text=f'[{socket.gethostname()}]\n{message}')
#     except KeyError:
#         print('TELEGRAM_TOKEN or TELEGRAM_CHAT_ID is not set')
#         pass
#     except Exception as e:
#         print('sending message failed', e)
#         return
