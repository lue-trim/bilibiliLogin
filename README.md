# bilibiliLogin
扫码登录哔哩哔哩Web端并获取cookies

## 安装
### 免安装（Windows Only）
- 直接在release页或者dist文件夹里下载`loginFirst.exe`、`refresh.exe`即可
### Conda
- 环境需求写在`bili_login.yaml`里

## 使用
1. 首次使用运行`loginFirst.py`或`dist/loginFirst.exe`
命令行将输出二维码，扫码后会将登录信息保存至cookies.txt、loginData.json，并将新Cookies输出到屏幕
2. (更新于2023年12月11日)Cookies大约一周后会失效，若需要刷新Cookies可运行`refresh.py`或`dist/refresh.exe`，无需重新扫码
执行更新命令后将同时废除原来的Cookies，并将新Cookies输出到屏幕

## API来源
[SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)

注：loginFirst_tv.py尚施工中，无法工作
