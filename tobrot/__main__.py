#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

import io
import logging
import os
import sys
import traceback

from pyrogram import Client, filters
from pyrogram.handlers import CallbackQueryHandler, MessageHandler

from tobrot import (API_HASH, APP_ID, AUTH_CHANNEL, CANCEL_COMMAND_G,
                    CLEAR_THUMBNAIL, CLONE_COMMAND_G, DOWNLOAD_LOCATION,
                    GET_SIZE_G, GLEECH_COMMAND, LEECH_COMMAND, LOG_COMMAND,
                    PYTDL_COMMAND_G, RENEWME_COMMAND, SAVE_THUMBNAIL,
                    STATUS_COMMAND, TELEGRAM_LEECH_COMMAND_G, TG_BOT_TOKEN,
                    UPLOAD_COMMAND, YTDL_COMMAND)
from tobrot.helper_funcs.download import down_load_media_f
from tobrot.plugins.call_back_button_handler import button
# the logging things
from tobrot.plugins.choose_rclone_config import rclone_command_f
from tobrot.plugins.custom_thumbnail import clear_thumb_nail, save_thumb_nail
from tobrot.plugins.incoming_message_fn import (g_clonee, g_yt_playlist,
                                                incoming_gdrive_message_f,
                                                incoming_message_f,
                                                incoming_purge_message_f,
                                                incoming_youtube_dl_f,
                                                rename_tg_file)
from tobrot.plugins.new_join_fn import help_message_f, new_join_f
from tobrot.plugins.rclone_size import check_size_g, g_clearme
from tobrot.plugins.status_message_fn import (cancel_message_f, exec_message_f,
                                              status_message_f,
                                              upload_document_f,
                                              upload_log_file)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":
    # create download directory, if not exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    #
    app = Client(
        "LeechBot",
        bot_token=TG_BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        workers=343
    )
    #
    incoming_message_handler = MessageHandler(
        incoming_message_f,
        filters=filters.command(
            [f"{LEECH_COMMAND}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_message_handler)
    #
    incoming_gdrive_message_handler = MessageHandler(
        incoming_gdrive_message_f,
        filters=filters.command(
            [f"{GLEECH_COMMAND}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_gdrive_message_handler)
    #
    incoming_telegram_download_handler = MessageHandler(
        down_load_media_f,
        filters=filters.command(
            [f"{TELEGRAM_LEECH_COMMAND_G}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_telegram_download_handler)
    #
    incoming_purge_message_handler = MessageHandler(
        incoming_purge_message_f,
        filters=filters.command(["purge"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_purge_message_handler)
    #
    incoming_clone_handler = MessageHandler(
        g_clonee,
        filters=filters.command(
            [f"{CLONE_COMMAND_G}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_clone_handler)
    #
    incoming_size_checker_handler = MessageHandler(
        check_size_g,
        filters=filters.command(
            [f"{GET_SIZE_G}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_size_checker_handler)
    #
    incoming_g_clear_handler = MessageHandler(
        g_clearme,
        filters=filters.command(
            [f"{RENEWME_COMMAND}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_g_clear_handler)
    #
    incoming_youtube_dl_handler = MessageHandler(
        incoming_youtube_dl_f,
        filters=filters.command(
            [f"{YTDL_COMMAND}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_youtube_dl_handler)
    #
    incoming_youtube_playlist_dl_handler = MessageHandler(
        g_yt_playlist,
        filters=filters.command(
            [f"{PYTDL_COMMAND_G}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_youtube_playlist_dl_handler)
    #
    status_message_handler = MessageHandler(
        status_message_f,
        filters=filters.command(
            [f"{STATUS_COMMAND}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(status_message_handler)
    #
    cancel_message_handler = MessageHandler(
        cancel_message_f,
        filters=filters.command(
            [f"{CANCEL_COMMAND_G}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(cancel_message_handler)
    #
    exec_message_handler = MessageHandler(
        exec_message_f,
        filters=filters.command(["exec"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(exec_message_handler)
    #
    '''
    eval_message_handler = MessageHandler(
        eval_message_f,
        filters=filters.command(["eval"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(eval_message_handler)
    '''
    #
    rename_message_handler = MessageHandler(
        rename_tg_file,
        filters=filters.command(["rename"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(rename_message_handler)
    #
    upload_document_handler = MessageHandler(
        upload_document_f,
        filters=filters.command(
            [f"{UPLOAD_COMMAND}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(upload_document_handler)
    #
    upload_log_handler = MessageHandler(
        upload_log_file,
        filters=filters.command(
            [f"{LOG_COMMAND}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(upload_log_handler)
    #
    help_text_handler = MessageHandler(
        help_message_f,
        filters=filters.command(["help"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(help_text_handler)
    #
    new_join_handler = MessageHandler(
        new_join_f,
        filters=~filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(new_join_handler)
    #
    group_new_join_handler = MessageHandler(
        help_message_f,
        filters=filters.chat(chats=AUTH_CHANNEL) & filters.new_chat_members
    )
    app.add_handler(group_new_join_handler)
    #
    call_back_button_handler = CallbackQueryHandler(
        button
    )
    app.add_handler(call_back_button_handler)
    #
    save_thumb_nail_handler = MessageHandler(
        save_thumb_nail,
        filters=filters.command(
            [f"{SAVE_THUMBNAIL}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(save_thumb_nail_handler)
    #
    clear_thumb_nail_handler = MessageHandler(
        clear_thumb_nail,
        filters=filters.command(
            [f"{CLEAR_THUMBNAIL}"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(clear_thumb_nail_handler)
    #
    rclone_config_handler = MessageHandler(
        rclone_command_f,
        filters=filters.command(["rclone"])
    )
    app.add_handler(rclone_config_handler)
    #
    app.run()
