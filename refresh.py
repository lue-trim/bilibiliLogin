import os, time, requests, re, json
import http.cookiejar, requests.utils

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import binascii
import time

key = RSA.importKey('''\
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDLgd2OAkcGVtoE3ThUREbio0Eg
Uc/prcajMKXvkCKFCWhJYJcLkcM2DKKcSeFpD/j6Boy538YXnR6VhcuUJOhH2x71
nzPjfdTcqMz7djHum0qSZA0AyCBDABUqCrfNgCiJ00Ra7GmRj+YCK1NJEuewlb40
JNrRuoEUXpabUzGB8QIDAQAB
-----END PUBLIC KEY-----''')

def getCorrespondPath(ts):
    '获取刷新地址'
    cipher = PKCS1_OAEP.new(key, SHA256)
    encrypted = cipher.encrypt(f'refresh_{ts}'.encode())
    return binascii.b2a_hex(encrypted).decode()

ts = round(time.time() * 1000)
correspondPath = getCorrespondPath(ts)

def dict2str(data:dict):
    'cookie_dict转换为字符串'
    s = ''
    for i in data.keys():
        s += "{}={};".format(i, data[i])
    return s
    
# header和session
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
    }
session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar()
session.cookies.load(filename='cookies.txt', ignore_discard=True, ignore_expires=True)
cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)

# 检查是否需要更新
print("正在检查是否需要刷新")
response = session.get(
    url='https://passport.bilibili.com/x/passport-login/web/cookie/info', 
    headers=headers, 
    params={'csrf':cookies_dict['bili_jct']}
    )
data = response.json()['data']
if not data['refresh']:
    print("无需刷新")
    os.system('pause')
    quit()

# 获取refresh_csrf
print("正在获取刷新凭证")
response = session.get(
    url="https://www.bilibili.com/correspond/1/{}".format(correspondPath), 
    headers=headers
    )
refresh_csrf = re.search(r'(?<=<div id="1-name">).*?(?=</div>)', response.text).group()

# 获取refresh_token
with open("loginData.json", 'r', encoding='utf-8') as f:
    data = json.load(f)
refresh_token = data['refresh_token']

# 刷新cookies
print("正在获取新cookies")
response = session.post(
    url='https://passport.bilibili.com/x/passport-login/web/cookie/refresh', 
    headers=headers, 
    params={
        'csrf': cookies_dict['bili_jct'], 
        'refresh_csrf': refresh_csrf, 
        'source': 'main_web',
        'refresh_token': refresh_token
        }
    )
js = response.json()
data = js['data']
print("Code: {}, 信息: {}".format(js['code'], js['message']))

# 提取新的登录信息
loginData = data

# 提取新的csrf
cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
csrf = cookies_dict['bili_jct']

# 确认更新
print("正在更新cookies")
response = session.post(
    url='https://passport.bilibili.com/x/passport-login/web/confirm/refresh', 
    headers=headers, 
    params={
        'csrf': csrf, 
        'refresh_token': refresh_token
        }
    )
code = response.json()['code']
if code == 0:
    print("更新成功")
else:
    print(response.json()['message'])

# 保存登录信息
with open("loginData.json", 'w', encoding='utf-8') as f:
    json.dump(loginData, f)

# 保存cookies
session.cookies.save(filename='cookies.txt')

# 打印cookies
#cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
print("新的Cookies:", dict2str(cookies_dict))
os.system('pause')
