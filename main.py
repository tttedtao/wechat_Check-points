# -*- coding:utf-8 -*-
import hashlib
import time
from xml.etree.ElementTree import fromstring
import datetime
from flask import Flask, render_template
from flask import request

import model
from data_get import getscore, gettable, getUserinfo
from database import insertiUserinfo, web2db, updateclass, updatescore

app = Flask(__name__)
app.debug = False
def log_text(log_file,text):
    with open(log_file,'a',encoding='utf-8') as t:
        t.write(text)

# def hashcode(text):
#     code = hashlib.sha1(text.encode('utf-8')).hexdigest()
#     return code


# 格式化成2016-03-20 11:45:39形式
ti = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())








@app.route('/wx',methods=['GET','POST'])
def wechat():

    if request.method == 'GET':
        #微信公众平台里输入的token
        token = 'test1234'
        #获取输入参数
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        #字典排序
        list = [token, timestamp, nonce]
        list.sort()

        s = list[0] + list[1] + list[2]
        #sha1加密算法
        hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        #如果是来自微信的请求，则回复echostr
        if hascode == signature:
            return echostr
        else:
            return ""

    if request.method == 'POST':

        str_xml = request.stream.read()
        xml = fromstring(str_xml)
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        xml_model = model.reply_model(msgType)

        print(msgType)

        if msgType == "text":
            content = xml.find("Content").text
            log_text("log.txt","时间："+ti+"  消息类型："+ msgType+"  用户:"+fromUser + "\n""内容:" + content+"\n")
            print(fromUser + ":" + content)
            if content =="成绩":
                content = getscore(fromUser)
            elif content =="课表":
                content = gettable(fromUser)
            elif content == "密钥":
                content = fromUser
            elif content =="绑定":
                content = " http://64bc16e4.ngrok.io/signin"
            elif content == "同步数据":
                 content = web2db(fromUser)
            elif content =="更新课表":
                content =updateclass(fromUser)
            elif content =="更新成绩":
                content = updatescore(fromUser)
            else:
                content = xml.find("Content").text

            return xml_model % (fromUser, toUser, int(time.time()), content)

        elif msgType == "image":
            mediaid = xml.find("MediaId").text
            log_text("log.txt", "时间：" + ti + "  消息类型：" + msgType + "  用户:" + fromUser + "\n""内容:" + mediaid + "\n")
            print(xml_model % (fromUser, toUser, int(time.time()), mediaid))
            return xml_model % (fromUser, toUser, int(time.time()), mediaid)

        elif msgType=="voice"or"video"or"shortvideo"or"location"or"link":

            return '麻瓜是看不懂这条回复的\n神秘代码：55Lw3PFyHvvV6pKX0LkEh14bEboWIRpcDxjiG80sBlML2dgRXy6Zngvd2xJgNOLb'
        else:
            itemDic = [{'Title': 'Title', 'Description': 'Description',
                        'PicUrl': 'https://ss0.baidu.com/73x1bjeh1BF3odCf/it/u=3705265267,3767781981&fm=85&s=DE0A5C2A7D264E1B62FD99CB0300C0B1',
                        'Url': 'www.baidu.com'}, {'Title': 'Title1', 'Description': 'Description1',
                                                  'PicUrl': 'https://ss0.baidu.com/73x1bjeh1BF3odCf/it/u=3705265267,3767781981&fm=85&s=DE0A5C2A7D264E1B62FD99CB0300C0B1',
                                                  'Url': 'www.baidu.com'}]
            fromUser = xml.find("FromUserName").text
            toUser = xml.find("ToUserName").text
            mediaid = xml.find("MediaId").text
            return model.image_text_new_model(itemDic) % (fromUser, toUser, int(time.time()))

@app.route('/signin',methods=['GET','POST'])
def signin_from():

    if request.method == 'GET':

        return render_template('form.html')

    elif request.method =='POST':
        openid = request.form['openid']
        user = request.form['username']
        svpn = request.form['vpn']
        pw = request.form['password']
        if getUserinfo(openid) == None:
            if len(user)==10 and len(openid)==28:
                insertiUserinfo(openid,user,svpn,pw)
                return render_template('reply1.html')
            else:
                return render_template('form.html',message = '错误的密钥或者学号 ')
        else:
            return render_template('reply2.html')
    return
    # else:
    #     return render_template('form.html',message = 'Bad username or password',username = username)



if __name__ == '__main__':
    app.run(port=80)