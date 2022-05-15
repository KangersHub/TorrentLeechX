import os
import re
import time
import datetime
import shutil
import asyncio
import logging
import requests
import subprocess

from pathlib import Path
from hurry.filesize import size
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import urllib.parse as ur

from tobrot.helper_funcs import media_info, download_tg
from tobrot import (
    DESTINATION_FOLDER,
    DOWNLOAD_LOCATION,
    INDEX_LINK,
    LOGGER,
    RCLONE_CONFIG,
    AUTH_CHANNEL
)

async def mannual_gd_upload(client, message):
    '''Upload a local file to gdrive manually'''
    g_id = message.from_user.id
    start_time = time.time()
    if g_id not in AUTH_CHANNEL:
        await message.reply_text("You're not allowed to use this command!", quote = True)
        return
    process_msg = await message.reply_text("`Processing...⏳`", parse_mode = "markdown", quote = True) 
    if not len(message.text) > 6 :
        await process_msg.delete()
        await message.reply_text("**‼️You didn't give path to a file‼️😡**\n`Aborting...`", parse_mode = 'markdown', quote = True)
        return
    path_to_file = str(message.text.split('upgd ', 1)[1])
    if not os.path.exists(path_to_file):
        await process_msg.delete()
        await message.reply_text("**‼️Given file path doesn't exist‼️😡\nGive a valid path to file!**\n`Aborting...`", parse_mode = 'markdown', quote = True)
        return
    await process_msg.edit("Found a valid path to file...\n`Now Uploading to ☁️Cloud!!!`", parse_mode = 'markdown')
    if not os.path.exists("rclone.conf"):
        with open("rclone.conf", "w+", newline="\n", encoding="utf-8") as fole:
            fole.write(f"{RCLONE_CONFIG}")
    if os.path.exists("rclone.conf"):
        with open("rclone.conf", "r+") as file:
            con = file.read()
            gUP = re.findall("\[(.*)\]", con)[0]
            LOGGER.info(gUP)
    destination = f"{DESTINATION_FOLDER}"
    path_to_file = str(Path(path_to_file).resolve())
    LOGGER.info(path_to_file)
    if os.path.isfile(path_to_file):
        g_au = [
            "rclone",
            "copy",
            "--config=rclone.conf",
            f"{path_to_file}",
            f"{gUP}:{destination}",
            "-v",
        ]
        LOGGER.info(g_au)
        tmp = await asyncio.create_subprocess_exec(
            *g_au, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        pro, cess = await tmp.communicate()
        LOGGER.info(pro.decode("utf-8"))
        LOGGER.info(cess.decode("utf-8"))
        gk_file = re.escape(os.path.basename(path_to_file))
        LOGGER.info(gk_file)
        with open("filter.txt", "w+", encoding="utf-8") as filter:
            print(f"+ {gk_file}\n- *", file=filter)

        t_a_m = [
            "rclone",
            "lsf",
            "--config=rclone.conf",
            "-F",
            "i",
            "--filter-from=filter.txt",
            "--files-only",
            f"{gUP}:{destination}",
        ]
        gau_tam = await asyncio.create_subprocess_exec(
            *t_a_m, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        # os.remove("filter.txt")
        gau, tam = await gau_tam.communicate()
        gautam = gau.decode().strip()
        LOGGER.info(gau.decode())
        LOGGER.info(tam.decode())
        # os.remove("filter.txt")
        gauti = f"https://drive.google.com/file/d/{gautam}/view?usp=drivesdk"
        gjay = size(os.path.getsize(path_to_file))
        button = []
        button.append(
            [InlineKeyboardButton(text="☁️ CloudUrl ☁️", url=f"{gauti}")]
        )
        if INDEX_LINK:
            indexurl = f"{INDEX_LINK}/{os.path.basename(path_to_file)}"
            tam_link = requests.utils.requote_uri(indexurl)
            LOGGER.info(tam_link)
            button.append(
                [
                    InlineKeyboardButton(
                        text="ℹ️ IndexUrl ℹ️", url=f"{tam_link}"
                    )
                ]
            )
        button_markup = InlineKeyboardMarkup(button)
        time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
        await asyncio.sleep(2)
        await message.reply_text(
            f"🤖: Uploaded successfully `{os.path.basename(path_to_file)}` <a href='tg://user?id={g_id}'>🤒</a>\n📀 Size: {gjay}\n<i>Time taken: {time_taken}</i>",
            reply_markup=button_markup,
            quote = True
        )
        await process_msg.delete()
    else:
        tt = os.path.join(destination, os.path.basename(path_to_file))
        LOGGER.info(tt)
        t_am = [
            "rclone",
            "copy",
            "--config=rclone.conf",
            f"{path_to_file}",
            f"{gUP}:{tt}",
            "-v",
        ]
        LOGGER.info(t_am)
        tmp = await asyncio.create_subprocess_exec(
            *t_am, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        pro, cess = await tmp.communicate()
        LOGGER.info(pro.decode("utf-8"))
        LOGGER.info(cess.decode("utf-8"))
        g_file = re.escape(os.path.basename(path_to_file))
        LOGGER.info(g_file)
        with open("filter1.txt", "w+", encoding="utf-8") as filter1:
            print(f"+ {g_file}/\n- *", file=filter1)

        g_a_u = [
            "rclone",
            "lsf",
            "--config=rclone.conf",
            "-F",
            "i",
            "--filter-from=filter1.txt",
            "--dirs-only",
            f"{gUP}:{destination}",
        ]
        gau_tam = await asyncio.create_subprocess_exec(
            *g_a_u, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        # os.remove("filter1.txt")
        gau, tam = await gau_tam.communicate()
        gautam = gau.decode("utf-8")
        LOGGER.info(gautam)
        LOGGER.info(tam.decode("utf-8"))
        # os.remove("filter1.txt")
        gautii = f"https://drive.google.com/folderview?id={gautam}"
        gjay = size(getFolderSize(path_to_file))
        LOGGER.info(gjay)
        button = []
        button.append(
            [InlineKeyboardButton(text="☁️ CloudUrl ☁️", url=f"{gautii}")]
        )
        if INDEX_LINK:
            indexurl = f"{INDEX_LINK}/{os.path.basename(path_to_file)}/"
            tam_link = requests.utils.requote_uri(indexurl)
            LOGGER.info(tam_link)
            button.append(
                [
                    InlineKeyboardButton(
                        text="ℹ️ IndexUrl ℹ️", url=f"{tam_link}"
                    )
                ]
            )
        button_markup = InlineKeyboardMarkup(button)
        time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
        await asyncio.sleep(2)
        await message.reply_text(
            f"🤖: Uploaded successfully `{os.path.basename(path_to_file)}` <a href='tg://user?id={g_id}'>🤒</a>\n📀 Size: {gjay}\n<i>Time taken: {time_taken}</i>",
            reply_markup=button_markup,
            quote = True
        )
        shutil.rmtree(path_to_file)
        await process_msg.delete()
        return



async def link_mediainfo_fn(bot, msg):
    '''get mediainfo from direct/index links'''
    if len(msg.command) == 1:
        await msg.reply("You didn't provide a link for mediainfo!!!", quote = True)
        return
    file_link = msg.text.replace('/mediainfo ', '').strip(' ')
    if file_link.endswith('/'):
        await msg.reply("Send direct download links only!!!", quote = True)
        return
    pr = await msg.reply("`Processing...`", quote = True)
    minfo = media_info(file_link)
    if not minfo:
        await pr.edit("There was some error while getting mediainfo.")
        return
    mitxt = f"[{ur.unquote(file_link.split('/')[-1])}]({minfo})"
    await pr.edit(mitxt)
    return
    
async def dl_to_local_fn(client, message):
    '''Download a tg file to bot's local storage'''
    usr_id = message.from_user.id
    if not message.reply_to_message:
        await message.reply("<b>⚠️ Oops ⚠️</b>\n\n <b><i>⊠ Reply with Telegram Media (File / Video)⁉️</b>", quote=True)
        return
    if len(message.command) > 1:
        new_name = (
            str(Path().resolve()) + "/" +
            message.text.split(" ", maxsplit=1)[1].strip()
        )
    else:
        new_name = None
        await message.reply_text(
            "⚠️You didn't give a name, file will be downloaded with original name!", quote=True
        )
    file, mess_age = await download_tg(client, message)
    try:
        if new_name != None:
            os.rename(file, new_name)
            final_name = new_name
        else:
            final_name = file
    except Exception as g_g:
        LOGGER.error(g_g)
        await message.reply_text("g_g")
    try:
        message_to_send = f"<b>Your File</b>\n<code>{final_name}</code>\n<b>has been downloaded!</b>"
        mention_req_user = (f"<a href='tg://user?id={usr_id}'><i>🙈</i></a>")
        message_to_send = mention_req_user + message_to_send
        await message.reply_text(text=message_to_send, quote=True, disable_web_page_preview=True)
    except Exception as pe:
        LOGGER.info(pe)
