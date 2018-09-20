# coding : UTF-8

import re
import csv
import time
import random

import demjson
from bs4 import BeautifulSoup
from src.common.spider import get_code

baseUrl = "https://k.autohome.com.cn"
grade = ['/suva01/','/suva1/','/suvb1/','/suvc1/','/suvd1/','/a001/','/a01/','/a1/','/b1/','/c1/','/d1/','/mpv1/','/s1/','/p1/','/mb1/']

out = open('carPrice.csv', 'w', newline='')
csv_write = csv.writer(out)
csv_write.writerow(['车系', '车型', '车款链接', '车款名称', '厂商指导价', '评分', '参与评分人数'])

def getCarMsg(url):
    """
    :param url: 某个热门车型的链接网址
    :return:返回该型包含的 车系-车型-id 列表
    """
    htmlText = get_code(url)
    bs = BeautifulSoup(htmlText, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body  # 获取body部分
    ul = body.find('ul',class_ ='list-cont')
    li = ul.find_all('li')
    rsList = []
    count = 0
    for i in li:
        carMsg = i.find('div',class_='cont-name')
        id = carMsg.find('a').get('href')
        name = carMsg.find('a').string
        audi = getCarAudi(id)
        print([audi,name,id])
        rsList.insert(count,[audi,name,id])   #将name,id放入列表中
    return rsList

def getDetailData(audiTypeIdList):
    for m in audiTypeIdList:
        url = baseUrl + "/FrontAPI/GetSpecListBySeriesId?seriesId="+m[2].replace("/","")+"&specState=1"   #拼接url字符串,
        content = get_code(url)    #content为json格式的数据，格式为列表
        jsonData = demjson.decode(content)   #解码成python的列表
        for i in jsonData:
            thisLink = "https://k.autohome.com.cn/spec/" + str(i['SpecId']) + "/"
            thisRow = [m[0].encode('gbk', 'ignore').decode('gbk'),           #车系
                       m[1].encode('gbk', 'ignore').decode('gbk'),           #车型
                       thisLink.encode('gbk', 'ignore').decode('gbk'),       #车款链接
                       i['SpecName'].encode('gbk', 'ignore').decode('gbk'), #
                       i['MinPrice'].encode('gbk', 'ignore').decode('gbk'),
                       i['Average'].encode('gbk', 'ignore').decode('gbk'),
                       i['EvaluationCount']]
            csv_write.writerow(thisRow)  #将该行数据写入csv中
            print(thisRow)


def getCarAudi(carId):
    """
    通过该车型id获取，该车型对应的车系
    :param carId: 汽车id(在汽车之家中的id)
    :return: 车系（一个字符串）
    """
    url = "https://www.autohome.com.cn" + carId         #拼接该车型所在页面的网址
    htmlText = get_code(url)    #get页面源代码
    bs = BeautifulSoup(htmlText, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body  # 获取body部分
    carAudiType = body.find('div',class_='athm-sub-nav__car__name').find('a')  #车系以及车型
    audiType = re.sub("<.*?>","",str(carAudiType))
    audi = audiType.split("-")[0]                                  #提取车系
    return audi


if __name__ == '__main__':
    for j in grade:
        thisGradeUrl = baseUrl + j
        rsLi = getCarMsg("https://k.autohome.com.cn/suva01/")
        getDetailData(rsLi)
    out.close()