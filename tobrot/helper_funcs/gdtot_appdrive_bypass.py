import re
import base64
import requests
from urllib.parse import urlparse, parse_qs
from lxml import etree

from tobrot import APPDRIVE_EMAIL, APPDRIVE_PASS, GDTOT_CRYPT, APPDRIVE_SHARED_DRIVE_ID, APPDRIVE_FOLDER_ID

crypt = GDTOT_CRYPT

account = {
    'email': APPDRIVE_EMAIL, 
    'passwd': APPDRIVE_PASS
}

async def gdtot_parse_info(res):
    title = re.findall(">(.*?)<\/h5>", res.text)[0]
    info = re.findall('<td\salign="right">(.*?)<\/td>', res.text)
    parsed_info = {
        'error': True,
        'message': 'Link Invalid.',
        'title': title,
        'size': info[0],
        'date': info[1]
    }
    return parsed_info

# ==========================================

async def gdtot_dl(url):
    client = requests.Session()
    client.cookies.update({ 'crypt': crypt })
    res = client.get(url)

    info = await gdtot_parse_info(res)
    info['src_url'] = url

    res = client.get(f"https://new.gdtot.top/dld?id={url.split('/')[-1]}")
    
    try:
        url = re.findall('URL=(.*?)"', res.text)[0]
    except:
        info['message'] = 'The requested URL could not be retrieved.',
        return info

    params = parse_qs(urlparse(url).query)
    
    if 'msgx' in params:
        info['message'] = params['msgx'][0]
    
    if 'gd' not in params or not params['gd'] or params['gd'][0] == 'false':
        return info
    
    try:
        decoded_id = base64.b64decode(str(params['gd'][0])).decode('utf-8')
        info['gd_id'] = decoded_id
        info['message'] = 'Success.'
        info['error'] = False
    except:
        info['error'] = True
    
    return info

#-------------------------------------------------------------------------------#
#------------------------------------appdrive-----------------------------------#
#-------------------------------------------------------------------------------#

async def account_login(client, url, email, password):
    data = {
        'email': email,
        'password': password
    }
    client.post(f'https://{urlparse(url).netloc}/login', data=data)

async def update_account(client, url, shared_drive_id, folder_id):
    data = {
        'root_drive': shared_drive_id,
        'folder': folder_id
    }
    client.post(f'https://{urlparse(url).netloc}/account', data=data)

async def gen_payload(data, boundary=f'{"-"*6}_'):
    data_string = ''
    for item in data:
        data_string += f'{boundary}\r\n'
        data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
    data_string += f'{boundary}--\r\n'
    return data_string

async def parse_info(data):
    info = re.findall('>(.*?)<\/li>', data)
    info_parsed = {}
    for item in info:
        kv = [s.strip() for s in item.split(':', maxsplit = 1)]
        info_parsed[kv[0].lower()] = kv[1]
    return info_parsed

# ===================================================================

async def appdrive_dl(url):
    try:
        client = requests.Session()
        client.headers.update({
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        })

        await account_login(client, url, account['email'], account['passwd'])
        await update_account(client, url, APPDRIVE_SHARED_DRIVE_ID, APPDRIVE_FOLDER_ID)

        res = client.get(url)
        key = re.findall('"key",\s+"(.*?)"', res.text)[0]

        ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")

        info_parsed = await parse_info(res.text)
        info_parsed['error'] = False
        info_parsed['link_type'] = 'login' # direct/login
    
        headers = {
            "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
        }
    
        data = {
            'type': 1,
            'key': key,
            'action': 'original'
        }
    
        if len(ddl_btn):
            info_parsed['link_type'] = 'direct'
            data['action'] = 'direct'
    
        while data['type'] <= 3:
            try:
                response = client.post(url, data=await gen_payload(data), headers=headers).json()
                break
            except:
                data['type'] += 1
        
        if 'url' in response:
            info_parsed['gdrive_link'] = response['url']
        elif 'error' in response and response['error']:
            info_parsed['error'] = True
            info_parsed['error_message'] = response['message']
        else:
            info_parsed['error'] = True
            info_parsed['error_message'] = 'Something went wrong :('
    
        if info_parsed['error']: return info_parsed
    
        if urlparse(url).netloc == 'driveapp.in' and not info_parsed['error']:
            res = client.get(info_parsed['gdrive_link'])
            drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
            info_parsed['gdrive_link'] = drive_link
        
        info_parsed['src_url'] = url
    except Exception as er:
        info_parsed = {
            'error': True,
            'error_message': er
        }
    
    return info_parsed
