"""ThumbNail utilities, © @AnyDLBot"""


import os

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from tobrot import DOWNLOAD_LOCATION


async def save_thumb_nail(client, message):
	thumbnail_location = os.path.join(DOWNLOAD_LOCATION, "thumbnails")
	thumb_image_path = os.path.join(
		thumbnail_location, str(message.from_user.id) + ".jpg"
	)
	ismgs = await message.reply_text("<code>Processing . . . 🔄</code>")
	if message.reply_to_message is not None:
		if not os.path.isdir(thumbnail_location):
			os.makedirs(thumbnail_location)
		download_location = thumbnail_location + "/"
		downloaded_file_name = await client.download_media(
			message=message.reply_to_message, file_name=download_location
		)
		# https://stackoverflow.com/a/21669827/4723940
		Image.open(downloaded_file_name).convert("RGB").save(thumb_image_path)
		# Moved to upload_to_tg file
		os.remove(downloaded_file_name)
		await ismgs.edit(
			"<b>⚡<i>Custom Thumbnail 🖼 Saved for Next Uploads</i>⚡</b>\n\n"
			+ "<b><i>✅Your Photo is Set, Ready to Go ...👨‍🦯</i></b>."
		)
	else:
		await ismgs.edit("<b><i>⛔Sorry⛔</i></b>\n\n" + "<b>❌ Reply with Image to Save Your Custom Thumbnail.❌</b>")

async def clear_thumb_nail(client, message):
	thumbnail_location = os.path.join(DOWNLOAD_LOCATION, "thumbnails")
	thumb_image_path = os.path.join(
		thumbnail_location, str(message.from_user.id) + ".jpg"
	)
	ismgs = await message.reply_text("<code>Processing . . . 🔄</code>")
	if os.path.exists(thumb_image_path):
		os.remove(thumb_image_path)
		await ismgs.edit("<b><i>✅Success✅</i></b>\n\n" + "<b>🖼Custom Thumbnail Cleared Successfully As Per Your Request.</b>")
	else:
		await ismgs.edit("<b><i>⛔Sorry⛔</i></b>\n\n" + "<b>❌Nothing to Clear For You❌</b>")
