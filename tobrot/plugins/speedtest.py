from speedtest import Speedtest
import logging
from tobrot.helper_funcs.display_progress import humanbytes

torlog = logging.getLogger(__name__)

async def get_speed(self, message):
    imspd = await message.reply("`Running Speed Test...`")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    string_speed = f'''
<code>🌐 Server :</code>
╠ <b>Name:</b> <code>{result['server']['name']}</code>
╠ <b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
╠ <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
╚ <b>ISP:</b> <code>{result['client']['isp']}</code>

<code>🧭 SpeedTest Results :</code>
╠ <b>Upload:</b> <code>{humanbytes(result['upload'] / 8)}</code>
╠ <b>Download:</b>  <code>{humanbytes(result['download'] / 8)}</code>
╠ <b>Ping:</b> <code>{result['ping']} ms</code>
╚ <b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
'''
    await imspd.delete()
    await message.reply(string_speed, parse_mode="HTML")
    torlog.info(f'Server Speed result:-\nDL: {humanbytes(result["download"] / 8)}/s UL: {humanbytes(result["upload"] / 8)}/s')

