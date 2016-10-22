from datetime import datetime
import requests
import os
import sqlite3
from bs4 import BeautifulSoup
import re



def creatsqlit():
        con=sqlite3.connect("course_category.db")
        cur=con.cursor()
        cur.execute("CREATE TABLE coursedata(id integer primary KEY ,name char ,category varchar,category_son varchar,category_grson varchar,aim_url varchar,desc_text varchar,lean_num integer,time varchar,dgrees varchar)")
        con.commit()  #在创建的连接对象上提交

def initsqlit():
        con=sqlite3.connect("course_category.db")
        cur=con.cursor()
        cur.execute("DROP TABLE coursedata")
        cur.execute("CREATE TABLE coursedata(id integer primary KEY ,name char ,category varchar,category_son varchar,category_grson varchar,aim_url varchar,desc_text varchar,lean_num integer,time varchar,dgrees varchar)")
        con.commit()
'''
def get_pagenum():
    ba_url="http://www.jikexueyuan.com/course/android"
    r=requests.get(url=ba_url)
    r=r.content
    soup=BeautifulSoup(r.content,"html5lib")
    pagetotal=soup.find("div",id="page-nav")
    print(soup)
    print(pagetotal.contents)
    '''

def addtosqlite(course_info):
        name=course_info["name"]
        category=course_info["category"]
        category_son=course_info["category_son"]
        category_grson=course_info["category_grson"]
        aim_url=course_info["aim_url"]
        desc_text=course_info["desc_text"]
        lean_num=course_info["lean_num"]
        time=course_info["time"]
        dgrees=course_info["dgrees"]

        con=sqlite3.connect("course_category.db")
        cur=con.cursor()
        #数据表中插入数据要输入字段的名字
        sql="INSERT INTO coursedata (name,category,category_son,category_grson,aim_url,desc_text,lean_num,time,dgrees) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(name,category,category_son,category_grson,aim_url,desc_text,lean_num,time,dgrees)
        cur.execute(sql)
        print("插入数据成功！")
        con.commit()

#在分类页面爬取信息
def main_spider(href,text):
    r=requests.get(url=href)
    soup=BeautifulSoup(r.content,"html5lib")
    lesson_list=soup.find_all("div",class_="lesson-infor")
    for i in lesson_list:
        if(i.contents[1].text):
            name=i.contents[1].text
            aim_url=i.find("a").get("href")
            desc_text=i.contents[3].text
            desc_text=desc_text[4:-3]
            lean_peo=i.find("em",class_="learn-number").text
            lean_num=re.match(r'(\d*)',lean_peo)   #使用goup方法返回匹配内容
            lean_num=lean_num.group()
            time=i.find("dd",class_="mar-b8").contents[1].text
            dgrees=i.find("dd",class_="zhongji").find("em").text
            course_info={"name":name,
                         "category":text[0],
                         "category_son":text[1],
                         "category_grson":text[2],
                         "aim_url":aim_url,
                        "desc_text":desc_text,
                        "lean_num":lean_num,"time":time,
                        "dgrees":dgrees}
            print(course_info)
            addtosqlite(course_info)

#获取分类信息
def get_cate():
    url="http://www.jikexueyuan.com/course/"
    r=requests.get(url=url)
    soup=BeautifulSoup(r.content,"html5lib")
    cont1=soup.find("ul",class_="aside-cList") #一级分类容器
    #print(type(cont1))
    #print(cont1)
    for item in cont1:
        text1=item.find("a")
        if(text1!=-1):
            text1=text1.text
            #print(text1)  #一级分类
            cont2=item.find_all("dl")  #二级分类容器
            for item2 in cont2:
                text2=item2.find("dt").text
                #print("--",text2)  #二级分类
                cont3=item2.find("dd")
                cont3=cont3.find_all("a")  #三级分类容器
                for item3 in cont3:
                    text3=item3.text  #三级分类
                    href=item3.get("href")
                    #print("----",text3,href)
                    text=[text1,text2,text3]
                    main_spider(href,text)  #调用页面爬取


if __name__ == '__main__':
    starttime=datetime.now()
    #creatsqlit()
    initsqlit()
    get_cate()
    #get_pagenum()
    endtime=datetime.now()
    print("耗时：",(endtime-starttime).seconds,"秒")