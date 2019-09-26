import requests

class Bot:
    base:str = "https://api.telegram.org/bot"
    def __init__(self, token : str):
        self.token = token
        self.offset = 0

    def get_updates(self):
        reply = requests.get(self.base + self.token + "/getUpdates?offset=" + str(self.offset))
        messages = dict()
        data = reply.json()["result"]
        for update in data:
            if update["update_id"] >= self.offset:
                self.offset = update["update_id"] + 1
            try:
                if update["message"]["text"].find("/link") != -1:
                    messages[update["update_id"]] = update["message"]
            except:
                continue
        return messages

    def delete_message(self, chat_id, message_id):
        requests.get(self.base + self.token + "/deleteMessage?message_id=" + str(message_id) + "&chat_id=" + str(chat_id))

    def send_message(self, chat_id:int, text:str, reply_to_msg = None):
        if reply_to_msg:
            requests.get(url=(self.base + self.token + "/sendMessage?chat_id=" + str(chat_id)) + "&reply_to_message_id=" + str(reply_to_msg), params={'text' : text})
        else:
            requests.get(url= (self.base + self.token + "/sendMessage?chat_id=" + str(chat_id)), params={'text' : text})
