# -*- coding:utf-8 -*-



text_str = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content></xml>"

img_str = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[image]]></MsgType><Image><MediaId><![CDATA[%s]]></MediaId></Image></xml>"


image_text_lj = "<ArticleCount>%s</ArticleCount><Articles>%s</Articles></xml>"
image_text_item = "<item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item>"


def reply_model(type):

    if type == "text":
        return text_str
    elif type == "image":
        return img_str





def image_text_new_model(itemDic):

    items = ""
    for item in itemDic:
        items += image_text_item % (item['Title'], item['Description'], item['PicUrl'], item['Url'])


    return image_text_item + (image_text_lj % (len(itemDic), items))