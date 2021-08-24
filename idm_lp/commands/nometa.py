import asyncio
import time

from vkbottle.framework.framework.rule import PrivateMessage
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.database import Database
from idm_lp.logger import logger_decorator
from idm_lp.utils import edit_message

user = Blueprint(
    name='nometa_blueprint'
)


def _r(r: list, t: str) -> list:
    for l in r:
        yield l + t


HELLO_TEXTS_PATTERNS = [
    "привет", "ку", "салам",
    "приветствую", "здрасте", "здравствуйте",
    "здарова", "йоу", 'хай',
    'добрый день', 'доброе утро', 'добрый вечер',
    'доброго времени суток', 'шалам', 'cалом алейкум',
    'cалам алейкум', 'салам', 'салом', "приветствую вас", "приветствую",
    "мы разделяем с тобой солнце", "мы разделяем с тобой луну",
    'бонжур', 'привiт', 'hi', 'hello', 'здравствуй', 'приветик', 'хаюшки'
]

HELLO_TEXTS = [
    *HELLO_TEXTS_PATTERNS,
    *_r(HELLO_TEXTS_PATTERNS, '!'),
    *_r(HELLO_TEXTS_PATTERNS, '.'),
]

HELLO_STICKER_IDS = [

]


async def nometa_checker(db: Database, message: Message):
    await asyncio.sleep(db.nometa_delay)
    try:
        msgs = await message.api.messages.get_by_conversation_message_id(
            peer_id=message.peer_id,
            conversation_message_ids=[message.conversation_message_id + 1]
        )
        if msgs.items:
            return
    except:
        pass

    await message.api.messages.send(
        peer_id=message.peer_id,
        message=db.nometa_message,
        attachment=",".join(db.nometa_attachments) if db.nometa_attachments else None,
        random_id=0
    )


@user.on.message_handler(FromMe(False), PrivateMessage(), text=HELLO_TEXTS)
@logger_decorator
async def nometa_message_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    if not db.nometa_enable:
        return
    try:
        msgs = await message.api.messages.get_by_conversation_message_id(
            peer_id=message.peer_id,
            conversation_message_ids=[message.conversation_message_id - 1]
        )
        if msgs.items:
            time_prev = msgs.items[0].date
            if time.time() - time_prev < 60 * 60 * 12:
                return
    except:
        pass

    asyncio.ensure_future(nometa_checker(db, message))


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -nometa")
@logger_decorator
async def activate_nometa_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.nometa_enable = False
    db.save()
    await edit_message(
        message,
        "✅ Режим NoMeta отключен"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +nometa")
@logger_decorator
async def deactivate_nometa_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.nometa_enable = True
    db.save()
    await edit_message(
        message,
        "✅ Режим NoMeta включен"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> nometa сообщение <text>")
@logger_decorator
async def deactivate_nometa_wrapper(message: Message, text: str, **kwargs):
    db = Database.get_current()
    db.nometa_message = text
    db.save()
    await edit_message(
        message,
        "✅ Текст NoMeta обновлен"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> nometa задержка <delay:float>")
@logger_decorator
async def deactivate_nometa_wrapper(message: Message, delay: float, **kwargs):
    db = Database.get_current()
    db.nometa_delay = delay
    db.save()
    await edit_message(
        message,
        "✅ Задержка NoMeta обновлена"
    )
