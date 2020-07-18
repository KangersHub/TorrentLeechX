#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

from pyrogram import CallbackQuery
from tobrot.helper_funcs.admin_check import AdminCheck
from tobrot.helper_funcs.download_aria_p_n import aria_start
from tobrot.helper_funcs.youtube_dl_button import youtube_dl_call_back
from tobrot.plugins.status_message_fn import cancel_message_f

async def button(bot, update: CallbackQuery):
	cb_data = update.data
	g = await AdminCheck(bot, update.message.chat.id, update.from_user.id)
	print(g)
	if (update.from_user.id == update.message.reply_to_message.from_user.id) or g:
		print(cb_data)
		if cb_data.startswith("cancel"):
			if len(cb_data) > 1:
				i_m_s_e_g = await update.message.reply_text("checking..?", quote=True)
				aria_i_p = await aria_start()
				g_id = cb_data.split()[-1]
				LOGGER.info(g_id)
				try:
					downloads = aria_i_p.get_download(g_id)
					LOGGER.info(downloads)
					LOGGER.info(downloads.remove(force=True))
					await i_m_s_e_g.edit_text(f"Leech Cancelled by <a href='tg://user?id={update.from_user.id}'>{update.from_user.first_name}</a>")
				except Exception as e:
					await i_m_s_e_g.edit_text("<i>FAILED</i>\n\n" + str(e) + "\n#error")
			else:
				await update.message.delete()
	
		elif "|" in cb_data:
			await youtube_dl_call_back(bot, update)
