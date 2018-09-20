# coding : UTF-8

import csv
import random
import time
import socket
import http.client
import requests
import re
from bs4 import BeautifulSoup

# 获取网页源代码（去掉换行符）
def get_code(url , data = None):
    """
    :param url:所要获取的网页链接
    :param data:为空
    :return: 返回网页源码（去掉换行符的）
    """
    header={ #浏览器配置
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }

    timeout = random.choice(range(90, 190))

    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)    #用request请求网址，rep为响应
            # rep.encoding = 'utf-8'                                      #设置编码方式
            rep.encoding = 'gb2312'
            html_text = rep.text                   #rep.text为网页源码，这里为匹配方便，我将 换行符 先替换掉了
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))

    if(html_text): return html_text
    else:
        print(url +" 无法获取源码 ")
        return url +" 无法获取源码 "

#正则匹配内容
def get_content(url):
    """
    :param url: 网址链接
    :param regex: 正则表达式
    :return: 返回所匹配的内容列表
    """
    htmltext = get_code(url)
    if(htmltext.__contains__(" 无法获取源码 ")):
        print(htmltext)
        return " 无法获取源码 "
    else:
        bs = BeautifulSoup(htmltext, "html.parser")  # 创建BeautifulSoup对象
        body = bs.body  # 获取body部分
        data = body.find('div', {'id': 'maodian'})  # 找到id为7d的div
        li = data.find_all('li',class_='specrow')
        if(li): return li
        else: return "正则表达式可能有误，无法匹配到内容"