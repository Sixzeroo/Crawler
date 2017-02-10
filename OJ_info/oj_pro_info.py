#coding=utf-8
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import codecs
import time

class OJ(object):
        def __init__(self,id,ojname):
            self.id=id
            self.ojname=ojname
            self.info={"sub_name":"内容未找到！","sub_des":"内容未找到！",
                       "sub_input":"内容未找到！","sub_output":"内容未找到！",
                       "exam_in":"内容未找到！","exam_out":"内容未找到！"}

        def info_XCOJ(self):
            base_url="http://xcacm.hfut.edu.cn/problem.php?id="
            url=base_url+str(self.id)
            t=0
            while (t < 10):
                try:
                    r = requests.get(url=url)
                    t = 10
                except Exception as e:
                    print("未能成功加载：", url, "\n错误信息：", e)
                    time.sleep(5)
                    t = t + 1
            soup=BeautifulSoup(r.content,"html5lib")
            sub_name=soup.find("title").text      #******题目名字
            sub_list=soup.find_all("div",class_="panel panel-info")
            sub_des=sub_list[0].find("p").text    #******题目描述
            sub_input=sub_list[1].find("p").text
            sub_output=sub_list[2].find("p").text
            exam_list=soup.find_all("div",class_="col-md-6")
            exam_in=exam_list[0].find("span").text   #********样例输入输出
            exam_out=exam_list[1].find("span").text
            self.info = {"sub_name": sub_name, "sub_des": sub_des,
                         "sub_input": sub_input, "sub_output":sub_output,
                         "exam_in":exam_in, "exam_out": exam_out}
            print("成功爬取题目！")

        def info_POJ(self):
            base_url="http://poj.org/problem?id="
            url=base_url+str(self.id)
            t=0
            while(t<10):
                try:
                    r = requests.get(url=url)
                    t=10
                except Exception as e:
                    print("未能成功加载：", url, "\n错误信息：", e)
                    time.sleep(5)
                    t=t+1
            soup = BeautifulSoup(r.content, "html5lib")
            sub_name = soup.find("div",class_="ptt").text
            sub_list = soup.find_all("div", class_="ptx")
            sub_des = sub_list[0].text  # ******题目描述
            sub_input = sub_list[1].text
            sub_output = sub_list[2].text
            exam_list = soup.find_all("pre", class_="sio")
            exam_in = exam_list[0].text  # ********样例输入输出
            exam_out = exam_list[1].text
            self.info = {"sub_name": sub_name, "sub_des": sub_des,
                         "sub_input": sub_input, "sub_output": sub_output,
                         "exam_in": exam_in, "exam_out": exam_out}
            print(self.info)

        def info_HDOJ(self):
            base_url="http://acm.hdu.edu.cn/showproblem.php?pid="
            url=base_url+str(self.id)
            t = 0
            while (t < 10):
                try:
                    r = requests.get(url=url)
                    t = 10
                except Exception as e:
                    print("未能成功加载：", url, "\n错误信息：", e)
                    time.sleep(5)
                    t = t + 1
            soup=BeautifulSoup(r.content,"html5lib")
            sub_name1=soup.find_all("td",attrs={"align":"center"})
            sub_name=sub_name1[2].find("h1").text   #题目名称
            sub_list=soup.find_all("div",class_="panel_content")
            sub_des=sub_list[0].text
            sub_input=sub_list[1].text
            sub_output=sub_list[2].text
            exam_in=sub_list[3].text
            exam_out=sub_list[4].text
            self.info = {"sub_name": sub_name, "sub_des": sub_des,
                         "sub_input": sub_input, "sub_output": sub_output,
                         "exam_in": exam_in, "exam_out": exam_out}
            print(self.info)


        def get_info(self):
            if(self.ojname=="xcoj"):
                self.info_XCOJ()
            else if(self.ojname=="poj"):
                self.info_POJ()
            else if (self.ojname == "hdoj"):
                self.info_HDOJ()
                 else:
                print("题目来源非法！")

        def create_md(self):
            path="G:\code\problem"   #生成文件到指定路径
            #path=os.getcwd()
            path=path+"\\"+self.ojname+str(self.id)+".md"
            with codecs.open(path,'a','utf-8') as f:
                f.write(self.info["sub_name"])
                f.writelines("\n#### 题目描述\n")
                f.write(self.info["sub_des"])
                f.writelines(['\n<!--more-->\n','***\n','#### 输入\n'])
                f.write(self.info["sub_input"])
                f.writelines(['\n***\n','####  输出\n'])
                f.write(self.info["sub_output"])
                f.writelines(['\n***\n', '####  样例输入\n'])
                f.write(self.info["exam_in"])
                f.writelines(['\n***\n', '####  样例输出\n'])
                f.write(self.info["exam_out"])
                f.writelines(['\n***\n', '#### 解题思路\n','***\n', '#### 代码\n'])
                f.close()
            print("成功写入文件")


if __name__ == '__main__':
    type=input("请输入题目来源：（选项：xcoj  poj hdoj）\n")
    id=input("请输入题号：\n")
    startime = datetime.now()
    xc=OJ(id,type)
    xc.get_info()
    xc.create_md()
    endtiem=datetime.now()
    print("共耗时：",(endtiem-startime).seconds,"秒")

