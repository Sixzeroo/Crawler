#coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
import os
import codecs


#获取题目中的序号
def get_titleid(title):
    title_id=re.match(r'^.*E(\d{4})$',title)    #防止字符串中的中文符号|的干扰
    if title_id is not None:
        return title_id.group(1)


def get_title_pure(title):
    title_pure=re.match(r'(.*)\（',title)
    title_pure=title_pure.group(1)
    return title_pure

def get_cource(root_url):
    '''
    爬取出指定页面的音频信息
    :param root_url: 页面url
    :return: 音频题目，编号，网址组成的列表
    '''
    base_url="http://www.ximalaya.com"
    res = requests.get(root_url)
    soup = BeautifulSoup(res.content, "lxml")
    cource = soup.find_all("div", class_="album_soundlist ")
    cource_list = cource[0].find_all("li")
    cources = []
    for cource in cource_list:
        cource_ro = cource.find("a", class_="title")
        cource_url = cource_ro.get("href")
        cource_url = base_url + cource_url
        cource_title = cource_ro.text.strip()  # 丢掉空格和换行
        cource_id = get_titleid(cource_title)
        cource_title = get_title_pure(cource_title)
        cource_info = [cource_title, cource_id, cource_url]
        ch = len(cources)
        if (ch > 0):
            if (cources[ch - 1][1] != cource_id):
                cources.append(cource_info)
        else:
            cources.append(cource_info)
    return cources

def get_coure_info(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "lxml")
    out = soup.find("div", class_="rich_intro")   #找对标签 不能只是一部分内容
    if out is None:
        return -1
    else:
        out=out.find("article").text.strip()
        rem = re.match(r'^(.*)想了解', out)  # 去除广告的影响
        if rem is None:
            info=out
        else:
            info = rem.group(1)
        return info


def make_mdfile(cources):
    path=os.getcwd()
    path=path+'\\'+"Info.md"
    with codecs.open(path,'a','utf-8') as f:
        for cource in cources:
            print(cource)
            info=get_coure_info(cource[2])
            if(info!=-1):
                f.writelines(['\n','####',cource[0],'\n'])
                f.write(info)
        f.close()



if __name__ == '__main__':
    root_url = "http://www.ximalaya.com/23508288/album/4541211?page=2"
    cources=get_cource(root_url)
    make_mdfile(cources)