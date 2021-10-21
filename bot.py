'''MIT License

Copyright (c) 2021 Kittu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''


from telethon import TelegramClient
from telethon import events
import os
import logging
from telethon.tl.types import ChannelParticipantsAdmins


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Basics
APP_ID = os.environ.get("APP_ID", default=None)
API_HASH = os.environ.get("API_HASH", default=None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", default=None)


bot = TelegramClient("MentionBot", APP_ID, API_HASH)
start = bot.start(bot_token=BOT_TOKEN) 



@bot.on(events.NewMessage(pattern="^/start"))
async def _(event):
    await event.reply('''Hey, I'm Mention Bot. I'll tag your group members and will notify them.\n\nMade by @Autichrist''')
@bot.on(events.NewMessage(pattern="^/mention ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "Users : "
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()



print ("Successfully Started")
start.run_until_disconnected()