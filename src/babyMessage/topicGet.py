# coding : UTF-8

import csv
import random
import time
import socket
import http.client
import requests
import re

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
            rep.encoding = 'utf-8'                                      #设置编码方式
            html_text = rep.text.replace("\n", "")                      #rep.text为网页源码，这里为匹配方便，我将 换行符 先替换掉了
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
def get_content(url,regex):
    """
    :param url: 网址链接
    :param regex: 正则表达式
    :return: 返回所匹配的内容列表
    """
    htmltext = get_code(url)
    pattern = re.compile(regex)
    resultList = re.findall(pattern,htmltext)
    return resultList

if __name__ == '__main__':
    baseURL = "https://www.baby-kingdom.com/"
    basePageUrl = "https://www.baby-kingdom.com/forum.php?mod=forumdisplay&fid=21&page="

    topicRegexNew =  "\"new\">.*?<a href=\"(.*?)\".*?</style>(.*?)</font>"   #匹配类名为new的帖子主题
    topicRegexLock = "\"lock\">.*?<a href=\"(.*?)\".*?</style>(.*?)</font>"  #匹配类名为lock的帖子主题
    topicReRegex = "class=\"t_fsz\">.*?postmessage.*?>(.*?)</div>"            #用于匹配帖子回复

    out = open('test.csv', 'w', newline='')
    csv_write = csv.writer(out)
    csv_write.writerow(['帖子主题','回复'])

    for count in range(1,2):
        thisUrl = basePageUrl + str(count)        #拼接页面网址 count为页数
        print(str(count) + "  " + thisUrl)
        if(count<=1): this_url_list = get_content(thisUrl,topicRegexNew)              #this_url_list 为匹配到的帖子链接列表
        else: this_url_list = get_content(thisUrl,topicRegexLock)
        for i in this_url_list:
            url = baseURL + i[0]               #拼接帖子页面的网址 i[0]为匹配到的
            url = url.replace("amp;", "")     #去掉抓取到的链接中的多余部分
            print(url + " " + i[1])
            answer = get_content(url,topicReRegex)   #匹配到的 帖子回复的列表
            for m in answer:
                thisLine = re.sub("<.*?>", "", m)
                thisLine = re.sub("rexsetsite.*?(\"pb_forumbox_rect_pos4\")","",thisLine)
                thisLine = re.sub("document.write.*?;","",thisLine)
                thisLine = re.sub("回覆.*?的帖子", "", thisLine)
                thisLine = re.sub(" 本帖.*?編輯 ","",thisLine)
                thisArr = thisLine.split(" ")
                if(len(thisArr) ==5) :
                    thisLine = thisArr[len(thisArr)-1]
                    if(thisLine == "..."): thisLine = thisArr[len(thisArr)-2]
                print(i[1] + "    " + thisLine)
                if(len(thisLine)>=3):
                    oneRow = [i[1].encode('gbk', 'ignore').decode('gbk'),thisLine.encode('gbk', 'ignore').decode('gbk')]
                    csv_write.writerow(oneRow)
                continue
            continue
        continue