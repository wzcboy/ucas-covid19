"""
author: Les1ie
mail: me@les1ie.com
license: CC BY-NC-SA 3.0
"""

import pytz
import requests
from datetime import datetime


s = requests.Session()
header = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 \
        Chrome/78.0.3904.62 XWEB/2693 MMWEBSDK/201201 Mobile Safari/537.36 MMWEBID/1300 \
        MicroMessenger/7.0.22.1820 WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
    }
s.headers.update(header)

user = ""    # sep账号
passwd = ""   # sep密码
api_key = ""  # server酱的api，填了可以微信通知打卡结>果，不填没影响


def login(s: requests.Session, username, password):
    # r = s.get(
    #     "https://app.ucas.ac.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.ucas.ac.cn%2Fsite%2FapplicationSquare%2Findex%3Fsid%3D2")
    # print(r.text)
    payload = {
        "username": username,
        "password": password
    }
    r = s.post("https://app.ucas.ac.cn/uc/wap/login/check", data=payload)

    # print(r.text)
    if r.json().get('m') != "操作成功":
        print(r.text)
        print("登录失败")
        exit(1)


def get_daily(s: requests.Session):
    daily = s.get("https://app.ucas.ac.cn/ucasncov/api/default/daily?xgh=0&app_id=ucas")
    # info = s.get("https://app.ucas.ac.cn/ncov/api/default/index?xgh=0&app_id=ucas")
    j = daily.json()
    print(j)
    d = j.get('d', None)
    if d:

        return daily.json()['d']
    else:
        print("获取昨日信息失败")
        exit(1)


def get_zrhsjc():
    day_in_year = datetime.now(tz=pytz.timezone("Asia/Shanghai")).timetuple().tm_yday
    # 三天做一次核酸检测，可以修改mod3的余数，来正确同步核酸时间
    if day_in_year % 3 == 1:
        return "1"
    else:
        return "2"


def submit(s: requests.Session, old: dict):
    new_daily = {
        'date': datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d"),
        'realname': old['realname'],
        'number': old['number'],
        'jzdz': old['jzdz'],
        'zrzsdd': old['zrzsdd'],
        'sfzx': old['sfzx'],
        'dqszdd': old['dqszdd'],
        'geo_api_infot': old['geo_api_infot'],
        'szgj': old['szgj'],
        'szgj_select_info': old['szgj_select_info'],
        'geo_api_info': old['old_city'],
        'dqsfzzgfxdq': old['dqsfzzgfxdq'],
        'zgfxljs': old['zgfxljs'],
        'tw': old['tw'],
        'sffrzz': old['sffrzz'],
        'dqqk1': old['dqqk1'],
        'dqqk1qt': old['dqqk1qt'],
        'dqqk2': old['dqqk2'],
        'dqqk2qt': old['dqqk2qt'],
        'sfjshsjc': get_zrhsjc(),
        'dyzymjzqk': old['dyzymjzqk'],
        'dyzwjzyy': old['dyzwjzyy'],
        'dyzjzsj': old['dyzjzsj'],
        'dezymjzqk': old['dezymjzqk'],
        'dezwjzyy': old['dezwjzyy'],
        'dezjzsj': old['dezjzsj'],
        'dszymjzqk': old['dszymjzqk'],
        'dszwjzyy': old['dszwjzyy'],
        'dszjzsj': old['dszjzsj'],
        'gtshryjkzk': old['gtshryjkzk'],
        'extinfo': old['extinfo'],
        'app_id': 'ucas'}

    r = s.post("https://app.ucas.ac.cn/ucasncov/api/default/save", data=new_daily)
    print("提交信息:", new_daily)
    # print(r.text)
    result = r.json()
    if result.get('m') == "操作成功":
        print("打卡成功")
        if api_key:
            message(api_key, result.get('m'), new_daily)
    else:
        print("打卡失败，错误信息: ", r.json().get("m"))
        if api_key:
            message(api_key, result.get('m'), new_daily)


def message(key, title, body):
    """
    微信通知打卡结果
    """
    msg_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(key, title, body)
    requests.get(msg_url)


if __name__ == "__main__":
    print(datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S %Z"))
    login(s, user, passwd)
    yesterday = get_daily(s)
    print(yesterday)
    submit(s, yesterday)