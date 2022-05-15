import os
import logging
import urllib.parse as ur

from .telegraph import telegraph

from subprocess import run as shell_run, check_output

def media_info(file):
    shell_cmd = [
        'mediainfo',
        file,
        '--Ssl_IgnoreSecurity'
    ]
    try:
        result = check_output(shell_cmd).decode()
    except Exception as e:
        logging.error(e)
        return None
    if result:
        filename = file.split('/')[-1]
        filename = ur.unquote(filename)
        result = result.replace('\n', '<br>')
        result = result.replace(file, filename)
        link_path = telegraph.create_page(
            title = filename,
            content = result,
        )["path"]
        full_link = f"https://telegra.ph/{link_path}"
        return full_link
    else:
        return None
