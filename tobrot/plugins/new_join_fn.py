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
        """<b>Hello This is TorrentleechX an instance of <a href="https://github.com/XcodersHub/TorrentLeechX">This Repo</a>.\nTry the repo for yourself and dont forget to put a STAR and fork.</b>\n\n<i>here is a list of CMDS available for the bot.👇\n\ngclone - This command is used to clone gdrive files or folder using gclone.\n\nytdl - This command should be used as reply to a supported link.\n\npytdl - This command will download videos from youtube playlist link and will upload to telegram.\n\ngytdl - This will download and upload to your cloud.\n\ngpytdl - This download youtube playlist and upload to your cloud.\n\nleech - leech any torrent/magnet/direct-download link to Telegram.\n\nleechzip - leech any torrent/magnet/direct-download link to Telegram and Upload It as .tar.gz acrhive...\n\ngleech - leech any torrent/magnet/direct-download link to cloud.\n\ngleechzip - leech any torrent/magnet/direct-download link to Cloud and Upload It as .tar.gz acrhive...\n\nleechunzip - This will unarchive file and upload to telegram.\n\ngleechunzip - This will unarchive file and upload to cloud.\n\ntleech - This will mirror the telegram files to ur respective cloud.\n\ntleechunzip - This will unarchive telegram file and upload to cloud.\n\nsavethumbnail - To Add Thumbnail To File.\n\nclearthumbnail - To Remove Previously Added Thumbnail.\n\nstatus - show status of current downloads and stuff.\n\ngetsize - This will give you total size of your destination folder in cloud.\n\nrename - you can do rename to files.\n\ntoggledoc - choose whether the file shall be uploaded as doc or not.\n\ntogglevid - choose whether the file shall be uploaded as streamable or not.\n\nhelp - send help.\n\nrenewme - clear all downloads.(admin only)⚠️\n\nlog - This will send you a txt file of the logs.(admin only)⚠️\n\nrclone - This will change your drive config on fly.(First one will be default)--(admin only)⚠️</i>""",
        disable_web_page_preview=True,
    )
