#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | Akshay C

import asyncio
import logging
import os
import time
from pathlib import Path
import aria2p
import requests
from tobrot import (
	DOWNLOAD_LOCATION,
	GLEECH_COMMAND,
	GLEECH_UNZIP_COMMAND,
	GLEECH_ZIP_COMMAND,
	LEECH_COMMAND,
	LEECH_UNZIP_COMMAND,
	LEECH_ZIP_COMMAND,
	LOGGER,
	YTDL_COMMAND,
	GPYTDL_COMMAND,
	PYTDL_COMMAND,
)
from tobrot import bot
from tobrot.helper_funcs.admin_check import AdminCheck
from tobrot.helper_funcs.cloneHelper import CloneHelper
from tobrot.helper_funcs.download import download_tg
from tobrot.helper_funcs.download_aria_p_n import (
	aria_start,
	call_apropriate_function,
)
from tobrot.helper_funcs.download_from_link import request_download
from tobrot.helper_funcs.extract_link_from_message import extract_link
from tobrot.helper_funcs.upload_to_tg import upload_to_tg
from tobrot.helper_funcs.youtube_dl_extractor import extract_youtube_dl_formats
from tobrot.helper_funcs.ytplaylist import yt_playlist_downg


async def incoming_purge_message_f(client, message):
	"""/purge command"""
	print(message.client)
	i_m_sefg2 = await message.reply_text("Purging...", quote=True)
	if await AdminCheck(client, message.chat.id, message.from_user.id):
		aria_i_p = await aria_start()
		# Show All Downloads
		downloads = aria_i_p.get_downloads()
		for download in downloads:
			LOGGER.info(download.remove(force=True))
	await i_m_sefg2.delete()


async def incoming_message_f(client, message):
	"""/leech command or /gleech command"""
	user_command = message.command[0]
	g_id = message.from_user.id
	u_men = message.from_user.mention
	credit = await message.reply_text(
		f"<b><i>🛃 Working For 🛃:</i></b> {u_men}", parse_mode="html"
	)
	# get link from the incoming message
	i_m_sefg = await message.reply_text("<code>Processing . . . 🔄</code>", quote=True)
	rep_mess = message.reply_to_message
	is_file = False
	dl_url = ''
	cf_name = ''
	if rep_mess:
		file_name = ''
		if rep_mess.media:
			file = [rep_mess.document, rep_mess.video, rep_mess.audio]
			file_name = [fi for fi in file if fi is not None][0].file_name
		if not rep_mess.media or str(file_name).lower().endswith(".torrent"):
			dl_url, cf_name, _, _ = await extract_link(message.reply_to_message, "LEECH")
			LOGGER.info(dl_url)
			LOGGER.info(cf_name)
		else:
			if user_command == LEECH_COMMAND.lower():
				u_men = message.from_user.mention
				await i_m_sefg.edit(f"<i> Hey {u_men}, \n\n ⚠️ Check and Send a Valid Download Source to Start Me Up !! ⚠️</i>")
				return
			is_file = True
			dl_url = rep_mess
	elif len(message.command) == 2:
		dl_url = message.command[1]
		LOGGER.info(dl_url)

	else:
		await i_m_sefg.edit("<b>⚠️ Opps ⚠️</b>\n\n <b><i>⊠ Reply with Direct/Torrent Link or File⁉️</i></b>")
		return
	if dl_url is not None:

		current_user_id = message.from_user.id
		# create an unique directory
		new_download_location = os.path.join(
			DOWNLOAD_LOCATION, str(current_user_id), str(time.time())
		)
		# create download directory, if not exist
		if not os.path.isdir(new_download_location):
			os.makedirs(new_download_location)
		aria_i_p = ''
		if not is_file:
			await i_m_sefg.edit_text("<code>Extracting Links . . . 🔀</code>")
			# start the aria2c daemon
			aria_i_p = await aria_start()
			# LOGGER.info(aria_i_p)
		
		u_men = message.from_user.mention
		await i_m_sefg.edit_text(f"<b>👤 User : {u_men} \n Your Request Has Been Added To The Status \n Use /status To Check Your Progress</b>")
		# try to download the "link"
		is_zip = False
		is_cloud = False
		is_unzip = False
		bot_unzip = f"{LEECH_UNZIP_COMMAND}@{bot.username}"
		bot_zip = f"{LEECH_ZIP_COMMAND}@{bot.username}"

		if user_command == LEECH_UNZIP_COMMAND.lower() or bot_unzip.lower():
			is_unzip = True
		elif user_command == LEECH_ZIP_COMMAND.lower() or bot_zip.lower():
			is_zip = True

		if user_command == GLEECH_COMMAND.lower():
			is_cloud = True
		if user_command == GLEECH_UNZIP_COMMAND.lower():
			is_cloud = True
			is_unzip = True
		elif user_command == GLEECH_ZIP_COMMAND.lower():
			is_cloud = True
			is_zip = True
		sagtus, err_message = await call_apropriate_function(
			aria_i_p,
			dl_url,
			new_download_location,
			i_m_sefg,
			is_zip,
			cf_name,
			is_cloud,
			is_unzip,
			is_file,
			message,
			client,
		)
		if not sagtus:
			# if FAILED, display the error message
			await i_m_sefg.edit_text(err_message)
	else:
		await i_m_sefg.edit_text(
			f"<b> 🏖Maybe You Didn't Know I am Being Used !!</b> \n\n<b>🌐 API Error</b>: {cf_name}"
		)


async def incoming_youtube_dl_f(client, message):
	""" /ytdl command """
	current_user_id = message.from_user.id
	u_men = message.from_user.mention
	credit = await message.reply_text(
		f"<b><i>🛃 Working For 🛃:</i></b> {u_men}", parse_mode="html"
	)
	i_m_sefg = await message.reply_text("<code>Prrocessing...🔃</code>", quote=True)
	# LOGGER.info(message)
	# extract link from message
	if message.reply_to_message:
		dl_url, cf_name, yt_dl_user_name, yt_dl_pass_word = await extract_link(
			message.reply_to_message, "YTDL"
		)
		LOGGER.info(dl_url)
		LOGGER.info(cf_name)
	elif len(message.command) == 2:
		dl_url = message.command[1]
		LOGGER.info(dl_url)
		cf_name = None
		yt_dl_user_name = None
		yt_dl_pass_word = None
		cf_name = None
	else:
		await i_m_sefg.edit("<b>⚠️ Opps ⚠️</b>\n\n <b><i>⊠ Reply To YTDL Supported Link.</i></b>")
		return
	if dl_url is not None:
		await i_m_sefg.edit_text("<code>Extracting Links . . . 🔀</code>")
		# create an unique directory
		user_working_dir = os.path.join(DOWNLOAD_LOCATION, str(current_user_id))
		# create download directory, if not exist
		if not os.path.isdir(user_working_dir):
			os.makedirs(user_working_dir)
		# list the formats, and display in button markup formats
		thumb_image, text_message, reply_markup = await extract_youtube_dl_formats(
			dl_url, cf_name, yt_dl_user_name, yt_dl_pass_word, user_working_dir
		)
		if thumb_image is not None:
			req = requests.get(f"{thumb_image}")
			thumb_img = f"{current_user_id}.jpg"
			with open(thumb_img, "wb") as thumb:
				thumb.write(req.content)
			await message.reply_photo(
				# text_message,
				photo=thumb_img,
				quote=True,
				caption=text_message,
				reply_markup=reply_markup,
			)
			await i_m_sefg.delete()
		else:
			await i_m_sefg.edit_text(text=text_message, reply_markup=reply_markup)
	else:
		await i_m_sefg.edit_text(
			"<b> 🏖Maybe You Didn't Know I am Being Used !!</b> \n\n<b>🌐 API Error</b>: {cf_name}"
		)


# playlist
async def g_yt_playlist(client, message):
	""" /pytdl command """
	user_command = message.command[0]
	usr_id = message.from_user.id
	is_cloud = False
	url = None
	if message.reply_to_message:
		url = message.reply_to_message.text
		if user_command == GPYTDL_COMMAND.lower():
			is_cloud = True
	elif len(message.command) == 2:
		url = message.command[1]
		if user_command == GPYTDL_COMMAND.lower():
			is_cloud = True
	else:
		await message.reply_text("<b> Reply with Youtube Playlist link</b>", quote=True)
		return
	if "youtube.com/playlist" in url:
		u_men = message.from_user.mention
		i_m_sefg = await message.reply_text(
			f"<b>Ok Fine 🐈 {u_men} Bro!!:\n Your Request has been ADDED</b>\n\n <code> Please wait until Upload</code>",
			parse_mode="html",
		)
		await yt_playlist_downg(message, i_m_sefg, client, is_cloud)

	else:
		await message.reply_text("<b>YouTube playlist link only 🙄</b>", quote=True)

 #


async def g_clonee(client, message):
	""" /gclone command """
	g_id = message.from_user.id
	if message.reply_to_message is not None:
		LOGGER.info(message.reply_to_message.text)
		gclone = CloneHelper(message)
		gclone.config()
		a, h = gclone.get_id()
		LOGGER.info(a)
		LOGGER.info(h)
		await gclone.gcl()
		await gclone.link_gen_size()
	else:
		await message.reply_text(
			"You should reply to a message, which format should be [ID of Gdrive file/folder Name of the file/folder]\nOr read Github for detailled information"
		)


async def rename_tg_file(client, message):
	usr_id = message.from_user.id
	if not message.reply_to_message:
		await message.reply("<b>⚠️ Oops ⚠️</b>\n\n <b><i>⊠ Reply with Telegram Media (File / Video)⁉️</b>", quote=True)
		return
	if len(message.command) > 1:
		new_name = (
			str(Path().resolve()) + "/" +
			message.text.split(" ", maxsplit=1)[1].strip()
		)
		file, mess_age = await download_tg(client, message)
		try:
			if file:
				os.rename(file, new_name)
			else:
				return
		except Exception as g_g:
			LOGGER.error(g_g)
			await message.reply_text("g_g")
		response = {}
		final_response = await upload_to_tg(
			mess_age, new_name, usr_id, response, client
		)
		LOGGER.info(final_response)
		if not final_response:
			return
		try:
			message_to_send = ""
			for key_f_res_se in final_response:
				local_file_name = key_f_res_se
				message_id = final_response[key_f_res_se]
				channel_id = str(message.chat.id)[4:]
				private_link = f"https://t.me/c/{channel_id}/{message_id}"
				message_to_send += "👉 <a href='"
				message_to_send += private_link
				message_to_send += "'>"
				message_to_send += local_file_name
				message_to_send += "</a>"
				message_to_send += "\n"
			if message_to_send != "":
				mention_req_user = (
					f"<a href='tg://user?id={usr_id}'><i>🗃 Your Uploaded Files !!</i></a>\n\n"
				)
				message_to_send = mention_req_user + message_to_send
				message_to_send = message_to_send + "\n\n" + "<b>#uploads</b>"
			else:
				message_to_send = "<i>FAILED</i> to upload files. 😞😞"
			await message.reply_text(
				text=message_to_send, quote=True, disable_web_page_preview=True
			)
		except Exception as pe:
			LOGGER.info(pe)

	else:
		await message.reply_text(
			"<b>⚠️ Oops ⚠️</b>\n\n⚡Provide Name with extension.\n\n➩<b>Example</b>: <code> /rename Sample.mkv</code>", quote=True
		)
