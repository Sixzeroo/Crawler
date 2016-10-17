#coding=utf8
from bs4 import BeautifulSoup
import requests
import re
import sqlite3
from datetime import datetime

Maxpagenum=94

#创建记录数据库
def creatsqlit():
        con=sqlite3.connect("course.db")
        cur=con.cursor()
        cur.execute("CREATE TABLE coursedata(id integer primary KEY ,name char UNIQUE ,aim_url varchar,desc_text varchar,lean_num integer,time varchar,dgrees varchar)")
        con.commit()  #在创建的连接对象上提交

def initsqlit():
        con=sqlite3.connect("course.db")
        cur=con.cursor()
        cur.execute("DROP TABLE coursedata")
        cur.execute("CREATE TABLE coursedata(id integer primary KEY ,name char UNIQUE ,aim_url varchar,desc_text varchar,lean_num integer,time varchar,dgrees varchar)")
        con.commit()

#将数据插入到数据
def addtosqlite(course_info):
        name=course_info["name"]
        aim_url=course_info["aim_url"]
        desc_text=course_info["desc_text"]
        lean_num=course_info["lean_num"]
        time=course_info["time"]
        dgrees=course_info["dgrees"]

        con=sqlite3.connect("course.db")
        cur=con.cursor()
        #数据表中插入数据要输入字段的名字
        sql="INSERT INTO coursedata (name,aim_url,desc_text,lean_num,time,dgrees) VALUES ('%s','%s','%s','%s','%s','%s')"%(name,aim_url,desc_text,lean_num,time,dgrees)
        cur.execute(sql)
        print("插入数据成功！")
        con.commit()

#爬取的主要程序
def main_spider():
        ba_url='http://www.jikexueyuan.com/course/web/?pageNum='
        #ba_url='https://movie.douban.com/'
        pagenum=1

        while pagenum<=Maxpagenum:
                url=ba_url+str(pagenum)
				print("即将爬取：",url)

                try:
                        page=requests.get(url=url)
                except:
                        print("获取页面失败，正在重新抓取："+url)
                        continue

                soup=BeautifulSoup(page.content,"html5lib")
                lesson_list=soup.find_all("div",class_="lesson-infor")
                for i in lesson_list:
                        try:
                                if(i.contents[1].text):
                                        name=i.contents[1].text
                                        aim_url=i.find("a").get("href")
                                        desc_text=i.contents[3].text
                                        lean_peo=i.find("em",class_="learn-number").text
                                        lean_num=re.match(r'(\d*)',lean_peo)   #使用goup方法返回匹配内容
                                        lean_num=lean_num.group()
                                        time=i.find("dd",class_="mar-b8").contents[1].text
                                        dgrees=i.find("dd",class_="zhongji").find("em").text
                                        course_info={"name":name,"aim_url":aim_url,
                                                    "desc_text":desc_text,
                                                     "lean_num":lean_num,"time":time,
                                                     "dgrees":dgrees}
                                        print(course_info)
                                        addtosqlite(course_info)
                                        #print(name,"\n",aim_url,"\n",desc_text,"\n",lean_num.group())
                        except:
                                pass
                pagenum=pagenum+1


if __name__=='__main__':
        startime=datetime.now()
        #creatsqlit()
        initsqlit()
        main_spider()
        endtiem=datetime.now()
        print("共耗时：",(endtiem-startime).seconds,"秒")


