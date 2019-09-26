import logging
import sys
import time

import requests

from utils import make_url

logger = logging.getLogger(__name__)


class Bot:
    api_base = "https://api.telegram.org/bot"

    def __init__(self, token: str):
        if not token:
            raise ValueError("specify valid token")
        self.token = token
        self.offset = 0
        self.callbacks = []

    @property
    def base(self):
        return self.api_base + self.token

    def make_url(self, *args, params=None):
        return make_url(self.base, *args, params=params)

    def get_updates(self):
        response = requests.get(self.make_url('getUpdates', params={'offset': self.offset}))
        updates = response.json().get("result", [])
        if updates:  # check if not empty
            self.offset = max(self.offset, *[u['update_id'] + 1 for u in updates])
        return updates

    def delete_message(self, chat_id, message_id):
        url = self.make_url('deleteMessage')
        requests.post(url, params={'message_id': message_id, 'chat_id': chat_id})

    def send_message(self, chat_id: int, text: str, reply_to_msg=None, parse_mode='Markdown'):
        url = self.make_url('sendMessage')
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
        if reply_to_msg:
            params['reply_to_message_id'] = reply_to_msg
        requests.post(url=url, params=params)

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def remove_callback(self, callback):
        self.callbacks.remove(callback)

    def _process(self):
        for update in self.get_updates():
            logger.debug(update)
            for callback in self.callbacks:
                try:
                    callback(self, update)
                except Exception as e:
                    print(e, file=sys.stderr)

    def run_polling(self, interval=5):
        try:
            while True:
                self._process()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info('bye')
