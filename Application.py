import logging
import os
from pprint import pformat

from bot import Bot
from utils import make_url

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
logger = logging.getLogger(__name__)


def compose_link(text: str):
    url = make_url('https://lmgtfy.com', params={'q': text})
    return url


def get_command(update: dict):
    msg = update['message']
    entities = msg.get('entities', [])
    for ent in entities:
        if ent['type'] == 'bot_command':
            s = ent['offset']
            e = ent['offset'] + ent['length']
            cmd = msg['text'][s:e]
            text = msg['text'][e + 1:]
            if '@' in cmd:  # check if command contains bot mention
                return cmd.split('@')[0], text
            return cmd, text
    return None, msg.get('text')


def process_link(bot: Bot, update: dict):
    logger.debug('- ' * 10 + 'process_link')
    logger.debug(pformat(update))
    cmd, text = get_command(update)
    logger.debug(f'cmd: {cmd!r}, text: {text!r}')
    if cmd != '/link' or not text:
        logger.debug("invalid message")
        return
    msg = update['message']
    chat_id = msg["chat"]["id"]
    if msg['chat']['type'] == 'private':
        reply_msg_id = None
    else:
        reply_msg_id = msg["message_id"]

    google_link = compose_link(text)
    logger.debug(f"google_link {google_link}")
    sent_text = f"[let me google it for you]({google_link})"
    bot.send_message(chat_id, sent_text, reply_msg_id)


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)8s %(name)20s:%(lineno)-3d > %(message)s",
    )
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    bot = Bot(TOKEN)
    bot.add_callback(process_link)
    logger.info("running bot in polling mode")
    bot.run_polling(interval=2)


if __name__ == "__main__":
    main()
