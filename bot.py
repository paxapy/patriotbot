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
    def choice_content(self):
        types = ['videos', 'images']
        with open('{}.txt'.format(random.choice(types)), 'r') as f:
            link = random.choice(f.readlines())
        return link

    async def open(self, initial_msg, seed):
        await self.sender.sendMessage('Пришло время подумать о родине, дружок')
        return True

    async def on_chat_message(self, msg):

        await self.sender.sendMessage('похоже, ты не достаточно патриот. вот немного лекарства: \n {}'.format(
            self.choice_content()
        ))
        await self.sender.send

    async def on__idle(self, event):
        await self.sender.sendMessage('судя по всему ты не хочешь скрепляться, вызываю гибдд')
        self.close()


bot = telepot.aio.DelegatorBot(config.TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Patriot, timeout=100),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
