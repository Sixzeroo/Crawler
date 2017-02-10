#coding=utf-8
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
import os
import codecs
import time

class HDOJ(object):
    def __init__(self):
        self.runid=self.get_runid()
        self.base_url="http://acm.hdu.edu.cn/status.php?first="

    # 创建记录数据库
    def creatsqlit(self):
        con = sqlite3.connect("HDOJ_submit.db")
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE submit_OJ(id integer primary KEY ,submit_runid varchar ,submit_proid varchar,submit_memory varchar,submit_times varchar,submit_codelen varchar,submit_time varchar)")
        con.commit()  # 在创建的连接对象上提交
    #初始化数据库
    def initsqlit(self):
        path = os.getcwd()
        path = os.path.join(path, "HDOJ_submit.db")
        if (not os.path.exists(path)):
            t=0
        else:
            t=1
        con = sqlite3.connect("HDOJ_submit.db")
        cur = con.cursor()
        if(t):
            cur.execute("DROP TABLE submit_OJ")
        cur.execute(
            "CREATE TABLE submit_OJ(id integer primary KEY ,submit_runid varchar ,submit_proid varchar,submit_memory varchar,submit_times varchar,submit_codelen varchar,submit_time varchar)")
        con.commit()

    # 将数据插入到数据
    def addtosqlite(self,submit_group):
        con = sqlite3.connect("HDOJ_submit.db")
        cur = con.cursor()
        # 数据表中插入数据要输入字段的名字
        sql = "INSERT INTO submit_OJ(submit_runid,submit_proid,submit_memory,submit_times,submit_codelen,submit_time) VALUES ('%s','%s','%s','%s','%s','%s')" % (
            submit_group["submit_runid"],submit_group["submit_proid"], submit_group["submit_memory"], submit_group["submit_times"], submit_group["submit_codelen"], submit_group["submit_time"])
        cur.execute(sql)
        print("插入数据成功！")
        con.commit()

    #获得网页soup信息
    def get_soup(self,runid):
        url = self.base_url+str(runid)
        t = 0
        while (t < 10):
            try:
                r = requests.get(url=url)
                t = 10
            except Exception as e:
                print("未能成功加载：", url, "\n错误信息：", e)
                time.sleep(5)
                t = t + 1
        soup = BeautifulSoup(r.content, "html5lib")
        return soup

    def get_initsoup(self):
        url ="http://acm.hdu.edu.cn/status.php"
        t = 0
        while (t < 10):
            try:
                r = requests.get(url=url)
                t = 10
            except Exception as e:
                print("未能成功加载：", url, "\n错误信息：", e)
                time.sleep(5)
                t = t + 1
        soup = BeautifulSoup(r.content, "html5lib")
        return soup

    #获取最新提交的runid
    def get_runid(self):
        soup=self.get_initsoup()
        runid=soup.find_all("tbody")[3].find_all("tr")[1].find_all("td")[0].text
        return runid

    #进行一次更新，数据导入数据库
    def update(self,runid):
        soup=self.get_soup(runid)
        sub_list = soup.find_all("tbody")[3].find_all("tr")
        for submit in sub_list[1:]:
            submit_info = submit.find_all("td")
            submit_resu = submit_info[2].text
            if (submit_resu == "Accepted"):
                submit_proid = submit_info[3].text
                submit_runid = submit_info[0].text
                submit_memory = submit_info[5].text
                submit_times = submit_info[4].text
                submit_codelen=submit_info[6].text
                submit_time=submit_info[1].text
                submit_group = {"submit_runid": submit_runid, "submit_proid": submit_proid,
                                "submit_memory": submit_memory, "submit_times": submit_times,
                                "submit_codelen":submit_codelen,"submit_time":submit_time}
                print(submit_group)
                self.addtosqlite(submit_group)

    def main_work(self):
        now_id = self.get_runid()
        while(1):
            now_id = self.get_runid()
            while (int(now_id) - int(self.runid) < 15):
                time.sleep(10)
                now_id = self.get_runid()
            self.runid=str(int(self.runid)+15)
            try:
                self.update(self.runid)
            except Exception as e:
                print("出现错误",e,"程序继续运行")



if __name__ == '__main__':
    startime = datetime.now()
    hdoj=HDOJ()
    hdoj.initsqlit()
    hdoj.main_work()
    endtime=datetime.now()
    print("共耗时：",(endtime-startime).seconds,"秒")
