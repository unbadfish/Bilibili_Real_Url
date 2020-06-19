# -*- coding: UTF-8 -*-

import requests
import json

"""
author:unbadfish
usage: get the real url of bilibili's live room
date:2020/06/18
run:only one time
I suggest you to run this program in the IDLE, not in the cmd mode, because the url is VERY long
====================================================================================================
本项目受到了 https://github.com/wbt5/real-url 的启发,使用了其使用的API接口
this subject is inspired by https://github.com/wbt5/real-url ,as I use the API "wbt5" also used
====================================================================================================
Copyright 2020 unbadfish

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

cookies: dict = {}
"""
go to http://curl.trillworks.com/ to get your OWN cookies
But, after all, this program can run without this cookies
"""


def get_status(room_id: str):
    """获取直播间状态
    输入:room_id<<str"""
    full_url: str = 'http://api.live.bilibili.com/room/v1/Room/room_init?id=' + room_id
    # print(full_url)
    response = requests.get(url=full_url, cookies=cookies)
    doc: dict = json.loads(response.text)
    # print(doc)
    msg: str = doc.get('msg')
    # print(msg)
    if doc.get('data'):
        live_state = True
    else:
        live_state = None
    """
    网上有人说data->live_status的值表示直播状态:0->no;1->yes
    但是我看了一下430号(即78787号)直播间
    2020/06/14 15:25该人并未直播,live_status的值为2,疑惑...
    所以就只能这么凑合着办了,求大神指点
    """
    # print(live_state)
    return live_state, msg


"""
原作者说>>PC网页和手机APP端的qn=1是最高画质;qn取值0~4<<
但是我一个一个试了试发现好像长宽和比特率都一样
qn有0-4五种值,每个页面还提供了几个不同的链接.心累QAQ.有人想改就自己改吧...
"""


def get_flv(room_id: str):
    """获取直播flv类型源的链接
    输入的room_id<<str
    返回(url, message)或(None, message)<<tuple"""
    qn: str = str(1)  # qn值
    full_url: str = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomPlayInfo?room_id={}&play_url=1&mask=1&qn={}&platform=web'.format(room_id, qn)
    # print(full_url)
    response = requests.get(url=full_url, cookies=cookies)
    doc: dict = json.loads(response.text)
    # print(doc)
    msg: str = doc.get('message')
    try:
        flv_url: str = doc.get('data').get('play_url').get('durl')[0].get('url')
        # [0]表示第一个链接,[1]表示第二个...以此类推
    except:
        return None, msg
    else:
        return flv_url, msg


def get_m3u8(room_id: str):
    """获取直播的m3u8类型源的链接
    输入room_id<<str
    返回(url, message)或(None, message)<<tuple"""
    qn: str = str(1)  # qn值
    full_url: str = 'https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl?cid={}&platform=h5&otype=json&quality={}'.format(room_id, qn)
    # print(full_url)
    response = requests.get(url=full_url, cookies=cookies)
    doc: dict = json.loads(response.text)
    # print(doc)
    msg: str = doc.get('message')
    try:
        m3u8_url: str = doc.get('data').get('durl')[0].get('url')
        # [0]表示第一个链接,[1]表示第二个...以此类推
    except:
        return None, msg
    else:
        return m3u8_url, msg


print("""Copyright 2020 unbadfish

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.""")

print('输入直播房间号')
user_input: str = str(input())
"""====debug mode====
user_input: str = str(0)
# """
if user_input.isdigit():  # is int
    room_status: tuple = get_status(user_input)
    # print(room_status)
    if room_status[0]:  # room data is found
        print('直播间已找到')
        room_flv: tuple = get_flv(user_input)
        room_m3u8: tuple = get_m3u8(user_input)
        if room_flv[0]:
            print('flv url found.')
            print(room_flv[0])
        else:
            print('flv url NOT found.Error message:' + room_flv[1])
        print('\n')
        if room_m3u8[0]:
            print('m3u8 url found.')
            print(room_m3u8[0])
        else:
            print('m3u8 url NOT found.Error message:' + room_m3u8[1])
        if (room_flv[0] is not None and room_m3u8[0] is None) or (room_flv[0] is None and room_m3u8[0] is not None):
            print('如果只找到一种链接的话可能是主播未开播或者是其他不明原因,望大神指点【超大声】')
    else:
        print('未找到直播间.Error message:' + room_status[1])
else:
    print('请输入纯数字，如\"666\",\"2233\"')
input('程序结束，按回车键退出\n')