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

import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

APP_ID = int(os.environ.get("APP_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
yone = TelegramClient('client', APP_ID, API_HASH)
RUn = yone.start(bot_token=BOT_TOKEN)



@yone.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**Hey, I'm Yone Mention Bot**, I can Tag almost all members in group or channel \nHit Command - **/help** for more information\n\n",
                    buttons=(
                      [Button.url('Support', 'https://t.me/league_of_bots'),
                      Button.url('Developer', 'https://github.com/Noob-kittu')]
                    ),
                    link_preview=False
                   )


                   
@yone.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Help Menu of Yone Mention Bot**\n\nCommand: /Mention\nYou can use this command with text what you want to Tag others.\n`Example: /mention how are you buddy?`\nYou can you this command as a reply to any message. Bot will tag users to that replied messsage."
  await event.reply(helptext,
                    buttons=(
                      [Button.url('Support', 'https://t.me/league_of_bots'),
                      Button.url('Developer', 'https://github.com/Noob-kittu')]
                    ),
                    link_preview=False
                   )
  
@yone.on(events.NewMessage(pattern="^/mention ?(.*)"))
async def mentionall(event):
  if event.is_private:
    return await event.respond("This command can be use in groups and channels!")
  
  admins = []
  async for admin in yone.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("Only admins can mention all!")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("I can't mention members for older messages! (messages which are sent before I'm added to group)")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Give me one argument!")
  else:
    return await event.respond("Reply to a message or give me some text to mention others!")
  
  if mode == "text_on_cmd":
    usrnum = 0
    usrtxt = ""
    async for usr in yone.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await yone.send_message(event.chat_id, f"{msg} \n\n{usrtxt}")
        await asyncio.sleep(1)
        usrnum = 0
        usrtxt = ""
        
  if mode == "text_on_reply":
    usrnum = 0
    usrtxt = ""
    async for usr in yone.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await yone.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(1)
        usrnum = 0
        usrtxt = ""
        

print ("Successfully Started")
RUn.run_until_disconnected()