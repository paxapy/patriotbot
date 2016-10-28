import sys
import asyncio
import random

import urllib3
import telepot
import telepot.api
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
import telepot.api


proxy_url = "http://proxy.server:3128"

telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager,
                                  dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

"""
patriot bot
"""


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

        self.close()

    async def on__idle(self, event):
        await self.sender.sendMessage('судя по всему ты не хочешь скрепляться, вызываю гибдд')
        self.close()

TOKEN = sys.argv[1]

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Patriot, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
