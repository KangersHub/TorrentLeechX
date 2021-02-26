# This is code to switch which rclone config section to use. This setting affects the entire bot(And at this time, the cloneHelper only support gdrive, so you should only choose to use gdrive config section)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) xiaoqi-beta | gautamajay52

import configparser  # buildin package
import logging
import os
import re

import pyrogram.types as pyrogram
from pyrogram.types import CallbackQuery
# the logging things
from tobrot import OWNER_ID

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)


config = configparser.ConfigParser()


# def multi_rclone_init():
#     if not os.path.exists('rclone_bak.conf'):  # backup rclone.conf file
#         with open('rclone_bak.conf', 'w+', newline="\n", encoding='utf-8') as fole:
#             with open('rclone.conf', 'r') as f:
#                 fole.write(f.read())
#         LOGGER.info("rclone.conf backuped to rclone_bak.conf!")


async def rclone_command_f(client, message):
    """/rclone command"""
    LOGGER.info(
        f"rclone command from chatid:{message.chat.id}, userid:{message.from_user.id}")
    if message.from_user.id == OWNER_ID and message.chat.type == "private":
        config.read('rclone_bak.conf')
        sections = list(config.sections())
        inline_keyboard = []
        for section in sections:
            ikeyboard = [
                pyrogram.InlineKeyboardButton(
                    section,
                    callback_data=(f'rclone_{section}').encode("UTF-8")
                )
            ]
            inline_keyboard.append(ikeyboard)
        config.read('rclone.conf')
        section = config.sections()[0]
        msg_text = f"""Default section of rclone config is: **{section}**\n\n
There are {len(sections)} sections in your rclone.conf file, 
please choose which section you want to use:"""
        ikeyboard = [
            pyrogram.InlineKeyboardButton(
                "‼️ Cancel ‼️",
                callback_data=(f'rcloneCancel').encode("UTF-8")
            )
        ]
        inline_keyboard.append(ikeyboard)
        reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
        await message.reply_text(text=msg_text, reply_markup=reply_markup)
    else:
        await message.reply_text("You have no permission!")
        LOGGER.warning(
            f"uid={message.from_user.id} have no permission to edit rclone config!")


async def rclone_button_callback(bot, update: CallbackQuery):
    """rclone button callback"""
    if update.data == "rcloneCancel":
        config.read('rclone.conf')
        section = config.sections()[0]
        await update.message.edit_text(f"Opration canceled! \n\nThe default section of rclone config is: **{section}**")
        LOGGER.info(
            f"Opration canceled! The default section of rclone config is: {section}")
    else:
        section = update.data.split("_", maxsplit=1)[1]
        with open('rclone.conf', 'w', newline="\n", encoding='utf-8') as f:
            config.read('rclone_bak.conf')
            temp = configparser.ConfigParser()
            temp[section] = config[section]
            temp.write(f)
        await update.message.edit_text(f"Default rclone config changed to **{section}**")
        LOGGER.info(f"Default rclone config changed to {section}")
