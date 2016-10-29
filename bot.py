import os
import asyncio
import random
from types import SimpleNamespace

import aiohttp
import telepot
import telepot.aio.api
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space

try:
    import config
except ImportError:
    config = SimpleNamespace()
    config.TOKEN = os.environ['TOKEN']
    config.USE_PROXY = os.environ.get('USE_PROXY', False)
    config.PROXY_URL = os.environ.get('PROXY_URL', 'http://localhost:3128')


if config.USE_PROXY:
    telepot.aio.api._pools = {
        'default': aiohttp.ProxyConnector(proxy=config.PROXY_URL, limit=10)
    }

    telepot.aio.api._onetime_pool_spec = (aiohttp.ProxyConnector, dict(proxy=config.PROXY_URL, force_close=True))


class Patriot(telepot.aio.helper.ChatHandler):
    music = [
        'https://www.youtube.com/watch?v=vtw5u8Mhc_s',
        'https://www.youtube.com/watch?v=Eu2Yq-qUw5Y',
        'https://www.youtube.com/watch?v=L_utPjoRNsI',
        'https://www.youtube.com/watch?v=b7dgQIkkmpQ',
        'https://www.youtube.com/watch?v=37l7P5V1eXU',
        'https://www.youtube.com/watch?v=F023drCD-M4'
    ]

    async def open(self, initial_msg, seed):
        await self.sender.sendMessage('Пришло время подумать о родине, дружок')
        return True

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            await self.sender.sendMessage('Скажи что-нибудь словами')
            return

        await self.sender.sendMessage('похоже, ты не достаточно патриот. вот немного лекарства')
        await self.sender.sendMessage(random.choice(self.music))

    async def on__idle(self, event):
        await self.sender.sendMessage('судя по всему ты не хочешь скрепляться, вызываю гибдд')
        self.close()


bot = telepot.aio.DelegatorBot(config.TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Patriot, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
