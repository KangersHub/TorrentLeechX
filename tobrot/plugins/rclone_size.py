#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) gautamajay52
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
import subprocess
import os
import asyncio

from tobrot import (
    EDIT_SLEEP_TIME_OUT,
    DESTINATION_FOLDER,
    RCLONE_CONFIG
)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def check_size_g(client, message):
    #await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    del_it = await message.reply_text("🔊 Checking size...wait!!!")
    if not os.path.exists('rclone.conf'):
        with open('rclone.conf', 'w+', newline="\n", encoding = 'utf-8') as fole:
            #fole.write("[DRIVE]")
            fole.write(f"{RCLONE_CONFIG}")
    destination = f'{DESTINATION_FOLDER}'
    cmd = ['rclone', 'size', '--config=./rclone.conf', 'DRIVE:'f'{destination}']
    gau_tam = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    gau, tam = await gau_tam.communicate()
    LOGGER.info(gau)
    LOGGER.info(tam)
    LOGGER.info(tam.decode("utf-8"))
    gautam = gau.decode("utf-8")
    LOGGER.info(gautam)
    await asyncio.sleep(5)
    await message.reply_text(f"🔊CloudInfo:\n\n{gautam}")
    await del_it.delete()

#gautamajay52

async def g_clearme(client, message):
    inline_keyboard = []
    ikeyboard = []
    ikeyboard.append(InlineKeyboardButton("Yes 🚫", callback_data=("fuckingdo").encode("UTF-8")))
    ikeyboard.append(InlineKeyboardButton("No 🤗", callback_data=("fuckoff").encode("UTF-8")))
    inline_keyboard.append(ikeyboard)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await message.reply_text("Are you sure? 🚫 This will delete all your downloads locally 🚫", reply_markup=reply_markup, quote=True)
