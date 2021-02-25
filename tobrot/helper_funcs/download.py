#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) gautamajay52 | Shrimadhav U K

import asyncio
import logging
import math
import os
import re
import subprocess
import time
from datetime import datetime

from pyrogram import Client, filters
from tobrot import DOWNLOAD_LOCATION
from tobrot.helper_funcs.create_compressed_archive import (unrar_me, untar_me,
                                                           unzip_me)
from tobrot.helper_funcs.display_progress_g import progress_for_pyrogram_g
# the logging things
from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
#


async def down_load_media_f(client, message):
    user_id = message.from_user.id
    LOGGER.info(user_id)
    mess_age = await message.reply_text("...", quote=True)
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    if message.reply_to_message is not None:
        start_t = datetime.now()
        download_location = "/app/"
        c_time = time.time()
        try:
            the_real_download_location = await client.download_media(
                message=message.reply_to_message,
                file_name=download_location,
                progress=progress_for_pyrogram_g,
                progress_args=(
                    "trying to download", mess_age, c_time
                )
            )
        except Exception as g_e:
            LOGGER.info(g_e)
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        LOGGER.info(the_real_download_location)
        await asyncio.sleep(10)
        await mess_age.edit_text(f"Downloaded to <code>{the_real_download_location}</code> in <u>{ms}</u> seconds")
        the_real_download_location_g = os.path.basename(
            the_real_download_location)
        LOGGER.info(the_real_download_location_g)
        if len(message.command) > 1:
            if message.command[1].lower() == "unzip":
                file_upload = await unzip_me(the_real_download_location_g)
                if file_upload is not None:
                    g_response = await upload_to_gdrive(file_upload, mess_age, message, user_id)
                    LOGGER.info(g_response)

            elif message.command[1].lower() == "unrar":
                file_uploade = await unrar_me(the_real_download_location_g)
                if file_uploade is not None:
                    gk_response = await upload_to_gdrive(file_uploade, mess_age, message, user_id)
                    LOGGER.info(gk_response)

            elif message.command[1].lower() == "untar":
                file_uploadg = await untar_me(the_real_download_location_g)
                if file_uploadg is not None:
                    gau_response = await upload_to_gdrive(file_uploadg, mess_age, message, user_id)
                    LOGGER.info(gau_response)
        else:
            gaut_response = await upload_to_gdrive(the_real_download_location_g, mess_age, message, user_id)
            LOGGER.info(gaut_response)
    else:
        await mess_age.edit_text("Reply to a Telegram Media, to upload to the Cloud Drive.")


async def download_tg(client, message):
    user_id = message.from_user.id
    LOGGER.info(user_id)
    mess_age = await message.reply_text("...", quote=True)
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    if message.reply_to_message is not None:
        start_t = datetime.now()
        download_location = "/app/"
        c_time = time.time()
        try:
            the_real_download_location = await client.download_media(
                message=message.reply_to_message,
                file_name=download_location,
                progress=progress_for_pyrogram_g,
                progress_args=(
                    "trying to download", mess_age, c_time
                )
            )
        except Exception as g_e:
            LOGGER.info(g_e)
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        LOGGER.info(the_real_download_location)
        await asyncio.sleep(5)
        await mess_age.edit_text(f"Downloaded to <code>{the_real_download_location}</code> in <u>{ms}</u> seconds")
    return the_real_download_location
