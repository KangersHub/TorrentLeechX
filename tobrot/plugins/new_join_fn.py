#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import logging

import pyrogram
from tobrot import AUTH_CHANNEL, LOGGER


async def new_join_f(client, message):
    chat_type = message.chat.type
    if chat_type != "private":
        await message.reply_text(f"Current CHAT ID: <code>{message.chat.id}</code>")
        # leave chat
        await client.leave_chat(chat_id=message.chat.id, delete=True)
    # delete all other messages, except for AUTH_CHANNEL
    await message.delete(revoke=True)


async def help_message_f(client, message):
    # await message.reply_text("no one gonna help you 🤣🤣🤣🤣", quote=True)
    # channel_id = str(AUTH_CHANNEL)[4:]
    # message_id = 99
    # display the /help

    await message.reply_text(
        """Join this group for help-- @XcodersHub\n\n And also don't forget to star/fork this repo: <a href="https://github.com/AmirulAndalib/TorrentLeechX">TorrentLeechX</a> 
 
 here is a list of available cmds: 👇

 ytdl - This command should be used as reply to a supported link

 pytdl - This command will download videos from youtube playlist link and will upload to telegram.

 gytdl - This will download and upload to your cloud.

 gpytdl - This download youtube playlist and upload to your cloud.

 leech - leech any torrent/magnet/direct-download link to Telegram

 leechzip - leech any torrent/magnet/direct-download link to Telegram and Upload It as .tar.gz acrhive...

 gleech - leech any torrent/magnet/direct-download link to cloud

 gleechzip - leech any torrent/magnet/direct-download link to Cloud and Upload It as .tar.gz acrhive...

 leechunzip - This will unarchive file and upload to telegram.

 gleechunzip - This will unarchive file and upload to cloud.

 tleech - This will mirror the telegram files to ur respective cloud .

 tleechunzip - This will unarchive telegram file and upload to cloud.

 getsize - This will give you total size of your destination folder in cloud.

 rename - rename the file

 toggledoc - choose whether the file shall be uploaded as doc or not

 togglevid - choose whether the file shall be uploaded as streamable or not	 

 help - send help 

 renewme - clear all downloads (admin only)⚠️

 log - This will send you a txt file of the logs.(admin only)⚠️
 
 rclone - This will change your drive config on fly.(First one will be default)--(admin only)⚠️
 """,
        disable_web_page_preview=False,
    )
