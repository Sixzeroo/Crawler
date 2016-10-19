#coding=utf8

import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

url="https://unsplash.com/"


def get_dir():
    base_dir=os.getcwd()
    if(not os.path.isdir("imgs")):
        os.makedirs("imgs")
    base_dir=os.path.join(base_dir,"imgs")
    return base_dir

def get_imgurl():
    try:
        response=requests.get(url=url)
    except:
        print("提交请求失败，请重试。",url)
    soup=BeautifulSoup(response.content,"html5lib")
    test=soup.find_all("div",class_="y5w1y")
    imgurl=[]
    for i in test:
        imgurl_son=i.contents[1].get("href")
        #print(imgurl_son[1:])
        imgurl_son=url+imgurl_son[1:]
        print(imgurl_son)
        imgurl.append(imgurl_son)
    return imgurl

def get_img(imgurl):
    for item in imgurl:
           try:
                response=requests.get(url=item,stream=True)
           except:
                print("图片网址："+item+"get失败，进入下一张图片")
                continue
           img=response.content
           print(img)



if __name__ == '__main__':
    startime=datetime.now()
    base_dir=get_dir()
    imgurl=get_imgurl()
    get_img(imgurl)
    print(base_dir)
    endtiem=datetime.now()
    print("耗时：",(endtiem-startime).seconds,"秒")