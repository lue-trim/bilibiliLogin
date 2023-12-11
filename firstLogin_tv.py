import qrcode_terminal
import os, time, requests, json, urllib, hashlib
import http.cookiejar, requests.utils, time

def sign(params, appkey='4409e2ce8ffd12b8', appsec='59b43e04ad6965f34319062b478f83dd'):
    '为请求参数进行 api 签名'
    params.update({'appkey': appkey})
    params = dict(sorted(params.items())) # 重排序参数 key
    query = urllib.parse.urlencode(params) # 序列化参数
    sign = hashlib.md5((query+appsec).encode()).hexdigest() # 计算 api 签名
    params.update({'sign':sign})
    return params

def dict2str(data:dict):
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

#session.cookies.load(filename='cookies.txt', ignore_discard=True, ignore_expires=True)

# 扫码登录
while True:
    # 获取二维码及其密钥
    ts = round(time.time() * 1000)
    response = session.post(
        'https://passport.snm0516.aisee.tv/x/passport-tv-login/qrcode/auth_code', 
        headers=headers,
        params={'appkey': '4409e2ce8ffd12b8', 'local_id': 0, 'ts': 0, 'sign': 'e134154ed6add881d28fbdf68653cd9c'}
        )
    loginInfo = response.json()
    print("状态：", loginInfo['code'], loginInfo['message'])
    auth_code = loginInfo['data']['auth_code']

    # 生成二维码
    qrcode_terminal.draw(loginInfo['data']['url'])
    input("扫描后请回车确认")

    # 查询扫码状态
    ts = round(time.time() * 1000)
    response = session.post(
        url='https://passport.snm0516.aisee.tv/x/passport-tv-login/qrcode/poll', 
        params={'appkey': '4409e2ce8ffd12b8', 'auth_code': auth_code, 'ts': 0, 'local_id': 0, 'sign': '87de3d0fee7c3f4facd244537238914e'},
        headers=headers
        )
    pollInfo = response.json()
    print("状态：", pollInfo['code'], pollInfo['message'])
    loginData = pollInfo['data']
    
    if loginData['code'] == 0:
        break
        
    else:
        print(loginData['message'])
        continue

# 保存token
with open("tokens.json", 'w', encoding='utf-8') as f:
    json.dump(loginData, f)

# 保存cookies
session.cookies.save(filename='cookies.txt')
print('登录成功')

# 打印cookies
cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
print("Cookies:", dict2str(cookies_dict))

#print(f"登录成功, 有效期至{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + int(loginData['expires_in'])))}")

