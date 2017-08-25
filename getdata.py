# _*_ coding:utf-8 _*_
'''
爬取哈尔滨工程大学教务处成绩，课表
默认爬取与教务处当前展示成绩和课表

@author：ttt
@name:HEU_spider

'''

import urllib
import re
import http.cookiejar
import os
from urllib import request,parse
import ssl
from PIL import Image,ImageEnhance,ImageFilter
from bs4 import BeautifulSoup
from pytesseract import *

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def list2str(L):
    t = len(L)
    text = ''
    for i in range(t):
        for e in range(5):
            text += (L[i][e] + '\n')

    return text

def chen_ji(user,pw1,pw2):
    # class Heuspider(object):
    # def chen_ji(self,user,pw):

        # def __init__(self):


    headers =  {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"}
    cookie = http.cookiejar.CookieJar() #构造cookie实例
    handler1 = urllib.request.HTTPSHandler(context=ctx)
    handler2= urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler1,handler2) #创建opener
    req_1ur1='https://ssl.hrbeu.edu.cn/por/login_psw.csp'
    data_1 =parse.urlencode({'svpn_name':user,'svpn_password':pw1}).encode('utf-8')
    request_new1 = urllib.request.Request(url=req_1ur1, data=data_1, headers=headers)
    response1 = opener.open(request_new1)

    #验证码处理
    def checkcode():
        checkcode_url = "https://ssl.hrbeu.edu.cn/web/0/http/2/jw.hrbeu.edu.cn/ACTIONVALIDATERANDOMPICTURE.APPPROCESS"
        req = urllib.request.Request(checkcode_url, headers=headers)
        picture = opener.open(req).read()
        with open("checkcode.jpg", "wb") as f:
            f.write(picture)
            #os.system("checkcode.jpg") #调用系统图片查看，手动输入验证码
            # Agnomen = input(str("请输入验证码:"))
        image = Image.open("checkcode.jpg")
        text = image_to_string(image)#自动识别验证码

        Agnomen= text
        return Agnomen

    def login(user,pw2):
        Agnomen = checkcode()
        login_data = parse.urlencode({'WebUserNO':user,
                                             'Password':pw2,
                                          'Agnomen':Agnomen}).encode('GBK')
        request_url = "https://ssl.hrbeu.edu.cn/web/1/http/2/jw.hrbeu.edu.cn/ACTIONLOGON.APPPROCESS"
        request_new = urllib.request.Request(url=request_url,data=login_data, headers=headers)
        response = opener.open(request_new)
        #成绩页面
        url2_1 = "https://ssl.hrbeu.edu.cn/web/1/http/0/jw.hrbeu.edu.cn/ACTIONQUERYSTUDENTSCORE.APPPROCESS"
        #课表页面
        url2_2 = "https://ssl.hrbeu.edu.cn/web/1/http/2/jw.hrbeu.edu.cn/ACTIONQUERYELECTIVERESULTBYSTUDENT.APPPROCESS?mode=1"
        request_score = request.Request(url2_1,headers=headers)
        request_class = request.Request(url2_2, headers=headers)
        content1 = opener.open(request_score)
        content1 = content1.read().decode('gbk')
        content2 = opener.open(request_class)
        content2 = content2.read().decode('gbk')


        #成绩解析
        ###################################################
        a =r'<td height.*?"28".*?>(.*?)</td.*?td align.*?"center".*?>.*?<td nowrap>&nbsp;(.*?)</td.*?td.*?"center".*?>.*?<td.*?"center".*?>.*?<td.*?"center".*?>(.*?)</td.*?"center".*?>.*?<td.*?"center".*?>(.*?)</td.*?"center".*?>.*?</td>'     #正则表达式
        pattern = re.compile(a, re.S)
        res = pattern.findall(content1)
        class_property = []
        class_name = []
        class_credit = []
        class_grade = []

        for item in res:
            class_property.append(item[0])
            class_name.append(item[1])
            class_credit.append(item[2])
            class_grade.append(item[3])



        property = class_property
        name = class_name
        grade = class_grade
        credit = class_credit
        text_c = "课程名称\t学分\t成绩\n"
        for i in range(len(name)):
            text_c =text_c + name[i] + ' ' + credit[i] + ' ' + grade[i] + '\n'

        # return text_c
        #######################################
        #课表解析
        html_doc = content2

        soup = BeautifulSoup(html_doc, 'html.parser')  # 构造bs实例

        kechen = soup.find_all('script', language="JavaScript")  # 提取script节点下的信息
        # 创建节数 课名 教师 日期 地点 table 列表

        number = []
        class_name = []
        teacher = []
        class_week = []
        class_place = []
        table = []

        for k in kechen[3:]:  # 第一个节点信息无用
            text_t = k.get_text()  # 提取标签下的文字信息

            text_s = re.sub('\s', '', text_t)  # 除去空格\n\t\r
            text_ = re.sub('"', '', text_s)  # 除去‘ “ ’
            text_i = re.sub('InsertSchedule', '', text_)  # 除去字符‘InsertSchedule’
            text = re.sub(';', '', text_i)  # 除去‘；’

            r = text.split(',')  # 以‘，’为分隔符将str 变为 list
            r.pop()

            table.append(r[0][1:])
            class_name.append(r[2])
            teacher.append(r[3])
            class_week.append(r[4])
            class_place.append(r[6])
            # number.append(r[6])
            # number.append(r[7])

        # num1 = number[::2]
        # num2 = number[1:][::2]

        # 建立以table为key的dict，将table值变为具体课程时间

        dict1 = {"TABLE1#1": "11:1-2节",
                 "TABLE1#2": "21:1-2节",
                 "TABLE1#3": "31:1-2节",
                 "TABLE1#4": "41:1-2节",
                 "TABLE1#5": "51:1-2节",
                 "TABLE1#6": "61:1-2节",
                 "TABLE1#7": "71:1-2节",
                 "TABLE2#1": "12:3-4节",
                 "TABLE2#2": "22:3-4节",
                 "TABLE2#3": "32:3-4节",
                 "TABLE2#4": "42:3-4节",
                 "TABLE2#5": "52:3-4节",
                 "TABLE2#6": "62:3-4节",
                 "TABLE2#7": "72:3-4节",
                 "TABLE3#1": "13:5-6节",
                 "TABLE3#2": "23:5-6节",
                 "TABLE3#3": "33:5-6节",
                 "TABLE3#4": "43:5-6节",
                 "TABLE3#5": "53:5-6节",
                 "TABLE3#6": "63:5-6节",
                 "TABLE3#7": "73:5-6节",
                 "TABLE4#1": "14:7-8节",
                 "TABLE4#2": "24:7-8节",
                 "TABLE4#3": "34:7-8节",
                 "TABLE4#4": "44:7-8节",
                 "TABLE4#5": "54:7-8节",
                 "TABLE4#6": "64:7-8节",
                 "TABLE4#7": "74:7-8节",
                 "TABLE5#1": "15:9-10节",
                 "TABLE5#2": "25:9-10节",
                 "TABLE5#3": "35:9-10节",
                 "TABLE5#4": "45:9-10节",
                 "TABLE5#5": "55:9-10节",
                 "TABLE5#6": "65:9-10节",
                 "TABLE5#7": "75:9-10节",
                 "TABLE6#1": "15:9-10节",
                 "TABLE6#2": "25:9-10节",
                 "TABLE6#3": "36:11-12节",
                 "TABLE6#4": "46:11-12节",
                 "TABLE6#5": "56:11-12节",
                 "TABLE6#6": "66:11-12节",
                 "TABLE6#7": "76:11-12节",

                 }

        d = dict1
        class_time = []
        class_info = []
        for q in table:
            class_time.append(dict1[q])

        for t in range(len(table)):
            # print([class_time[t],class_week[t],class_name[t],teacher[t],class_place[t]])


            class_info.append([class_time[t], class_name[t], teacher[t], class_place[t], str(class_week[t] + '周')])

        Mon = []
        Tue = []
        Wen = []
        Thu = []
        Fri = []
        Sat = []
        Sun = []

        class_info = sorted(class_info)
        # print(class_info)

        for i in range(len(class_info)):
            t = int(class_info[i][0][0:1])

            if t == 1:
                Mon.append(class_info[i])
            elif t == 2:
                Tue.append(class_info[i])
            elif t == 3:
                Wen.append(class_info[i])
            elif t == 4:
                Thu.append(class_info[i])
            elif t == 5:
                Fri.append(class_info[i])
            elif t == 6:
                Sat.append(class_info[i])
            else:
                Sun.append(class_info[i])

        def list2str(L):
            t = len(L)
            text = ''
            for i in range(t):
                for e in range(4):
                    text += (L[i][e] + '\n')

            return text

        text_t ="【星期一】\n%s\n【星期二】\n%s\n【星期三】\n%s\n【星期四】\n%s\n【星期五】\n%s\n【星期六】\n%s\n【星期天】\n%s\n"%(list2str(Mon), list2str(Tue), list2str(Wen), list2str(Thu), list2str(Fri), list2str(Sat),
                         list2str(Sun))
        return text_c,text_t
    return login(user,pw2)







# if "__main__"==__name__:
#     print('请输入下列信息')
#     user = input(str('学号：'))
#     pw1 = input(str('信息门户密码：'))
#     pw2 = input(str('教务处密码：'))
#
#     result = chen_ji(user,pw1,pw2)
#     print(result[0],result[1])


