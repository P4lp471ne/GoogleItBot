import Bot
import time

token = ""

def compose_link(req:str):
    req = req[req.find("/link") + 5:]
    index = req.find(" -") + 2
    if index == 1:
        param = "g"
        return ("https://lmgtfy.com/?q=" + req.replace(" ", "+") + "&p=1&s=" + param)
    else:
        param = req[index]
        return ("https://lmgtfy.com/?q=" + req[index + 2:].replace(" ", "+") + "&p=1&s=" + param)


if __name__ == "__main__":
    bot = Bot.Bot(token)
    while True:
        time.sleep(5)
        messages = bot.get_updates()
        for i in messages.values():
            print(i["text"])
            if i["chat"]["type"] != "private":
                bot.delete_message(i["chat"]["id"], i["message_id"])
                try:
                    bot.send_message(int(i["chat"]["id"]), compose_link(i["text"]), i["reply_to_message"]["message_id"])
                except KeyError:
                    bot.bot.send_message(int(i["chat"]["id"]), compose_link(i["text"]))
            else:
                bot.send_message(int(i["chat"]["id"]), compose_link(i["text"]))
