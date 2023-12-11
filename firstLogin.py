import qrcode_terminal
import os, time, requests, json
import http.cookiejar, requests.utils

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
    print("正在获取登录二维码")
    response = session.get('https://passport.bilibili.com/x/passport-login/web/qrcode/generate', headers=headers)
    data = response.json()['data']
    #print("Code: {}, 信息: {}".format(data['code'], data['message']))
    qrcode_key = data['qrcode_key']

    # 生成二维码
    qrcode_terminal.draw(data['url'])
    input("扫描后请回车确认")

    # 查询扫码状态
    response = session.get(
        url='https://passport.bilibili.com/x/passport-login/web/qrcode/poll', 
        params={'qrcode_key': qrcode_key},
        headers=headers
        )
    data = response.json()['data']
    
    if data['code'] == 0:
        break
    else:
        print("Code: {}, 信息: {}".format(data['code'], data['message']))
        time.sleep(5)
        continue

# 保存登录信息
with open("loginData.json", 'w', encoding='utf-8') as f:
    json.dump(data, f)

# 保存cookies
session.cookies.save(filename='cookies.txt')
print('登录成功')

# 打印cookies
cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
print("Cookies:", dict2str(cookies_dict))
os.system('pause')
#print(f"登录成功, 有效期至{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + int(loginData['expires_in'])))}")

