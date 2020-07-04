#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) gautamajay52

import subprocess
import os
import asyncio

from tobrot import (
    EDIT_SLEEP_TIME_OUT,
    DESTINATION_FOLDER,
    RCLONE_CONFIG
)



async def check_size_g(client, message):
    #await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    del_it = await message.reply_text("🔊 Checking size...wait!!!")
    subprocess.Popen(('touch', 'rclone.conf'), stdout = subprocess.PIPE)
    with open('rclone.conf', 'a', newline="\n") as fole:
        fole.write("[DRIVE]\n")
        fole.write(f"{RCLONE_CONFIG}")
    destination = f'{DESTINATION_FOLDER}'
    gau_tam = subprocess.Popen(['rclone', 'size', '--config=rclone.conf', 'DRIVE:'f'{destination}'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    gau, tam = gau_tam.communicate()
    print(gau)
    print(tam)
    print(tam.decode("utf-8"))
    gautam = gau.decode("utf-8")
    print(gautam)
    await asyncio.sleep(5)
    await message.reply_text(f"🔊CloudInfo:\n\n{gautam}")
    await del_it.delete()
