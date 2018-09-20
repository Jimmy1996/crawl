# coding : UTF-8

import re
import csv
import time
import random

import demjson
from bs4 import BeautifulSoup
from src.common.saveToFile import save
from src.common.spider import get_content,get_code

baseUrl = "https://k.autohome.com.cn"
grade = ["/suva01/"]
def getDetail(liList):
    """
    :param liList:  bs4.element.Tag 列表
    :return: 返回提取好的信息列表，信息格式：['2013款 改款经典 1.6L 手动风尚版', '11.29', '--', '4.23', '651']
    """
    carMouths = []
    count = 0
    for i in liList:
        title = i.find('div', class_='emiss-title').find('a').string   #车型标题
        emissPrice = i.find_all('div', class_='emiss-price')
        price = emissPrice[0].find('a').string                          #厂商指导价
        price2 = emissPrice[1].string.replace(" ","").replace("\r\n","")                 #二手车价格
        score =  i.find('div',class_ = 'emiss-fen').find('a')  # 用户评分
        score = re.sub("<.*?>","",str(score))
        participantNum = i.find('div',class_='emiss-ren').find('a').string
        carMouth = [title,price,price2,score,participantNum]
        carMouths.insert(count,carMouth)
        count = count +1
        # print(carMouth)
    return carMouths

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
    out = open('test.csv', 'w', newline='')
    csv_write = csv.writer(out)
    csv_write.writerow(['车系','车型','车款链接','车款名称','厂商指导价','评分','参与评分人数'])
    for m in audiTypeIdList:
        url = baseUrl + "/FrontAPI/GetSpecListBySeriesId?seriesId="+m[2].replace("/","")+"&specState=1"
        content = get_code(url)
        jsonData = demjson.decode(content)
        for i in jsonData:
            thisLink = "https://k.autohome.com.cn/spec/" + str(i['SpecId']) + "/"
            thisRow = [m[0].encode('gbk', 'ignore').decode('gbk'),           #车系
                       m[1].encode('gbk', 'ignore').decode('gbk'),           #车型
                       thisLink.encode('gbk', 'ignore').decode('gbk'),       #车款链接
                       i['SpecName'].encode('gbk', 'ignore').decode('gbk'), #
                       i['MinPrice'].encode('gbk', 'ignore').decode('gbk'),
                       i['Average'].encode('gbk', 'ignore').decode('gbk'),
                       i['EvaluationCount']]
            csv_write.writerow(thisRow)
            print(thisRow)
    out.close()

def getCarAudi(carId):
    """
    :param carId: 汽车id(在汽车之家中的id)
    :return:
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

    rsLi = getCarMsg("https://k.autohome.com.cn/suva01/")
    getDetailData(rsLi)