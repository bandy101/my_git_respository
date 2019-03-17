# -*- coding: utf-8 -*-
#########################################################################
# Author: jonyqin
# Created Time: Thu 11 Sep 2014 03:55:41 PM CST
# File Name: Sample.py
# Description: WXBizMsgCrypt 浣跨敤demo鏂囦欢
#########################################################################
import sys  
import os
import time
import json
import httplib
from WXBizMsgCrypt import WXBizMsgCrypt
from django.http import HttpResponse,JsonResponse
from django.utils.encoding import smart_str,smart_unicode
from share import *
import xml.etree.cElementTree as ET

def callback(request):
    wxcpt=WXBizMsgCrypt(Token,EncodingAESKey,AppId)
    sVerifyMsgSig=request.GET.get('signature','')
    sVerifyTimeStamp=request.GET.get('timestamp','')
    sVerifyNonce=request.GET.get('nonce','')
    sVerifyEchoStr=request.GET.get('echostr','')
    response=HttpResponse(sVerifyEchoStr)
    # return HttpResponse(sVerifyEchoStr)
    # if sVerifyEchoStr !='':
    #     return HttpResponse(sVerifyEchoStr)
    # else:
    #     if request.method == 'POST':
    #         response=  HttpResponse(responseMsg(request.body),content_type="application/xml")

        # xml="""<xml> 
        # <ToUserName>< ![CDATA[toUser] ]></ToUserName> 
        # <FromUserName>< ![CDATA[fromUser] ]></FromUserName> 
        # <CreateTime>12345678</CreateTime> 
        # <MsgType>< ![CDATA[text] ]></MsgType> 
        # <Content>< ![CDATA[你好] ]></Content> 
        # </xml>"""
    # ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
    # if(ret!=0):
    #     #write_sql("ERR: VerifyURL ret: " + str(ret))
    #     return HttpResponse(request,"ERR: VerifyURL ret: " + str(ret))
    # return HttpResponse(request,sEchoStr)
    response = None
    if request.method == 'GET':
        # response = HttpResponse(checkSignature(request),content_type="text/plain")
        response = HttpResponse(request.GET.get('echostr',''))
    elif request.method == 'POST':
        # print request.body
        response=  HttpResponse(responseMsg(request.body),content_type="application/xml")
    else:
        response = None
    return response
def responseMsg(postContent):
    resultStr=''
    # resultStr="""<xml><ToUserName><![CDATA[oz5ycv4zJvO4nR-UMKU9vQjdDkuI]]></ToUserName><FromUserName><![CDATA[oz5ycv4zJvO4nR-UMKU9vQjdDkuI]]></FromUserName> 
    #     <CreateTime>12345678</CreateTime> 
    #     <MsgType><![CDATA[text]]></MsgType> 
    #     <Content><![CDATA[你好]]></Content> 
    #     </xml>"""
    postStr = smart_str(postContent)
    if postStr:
        msg = xmlContent2Dic(postStr)
        print msg
        if msg['MsgType']:
            if msg['MsgType'] == 'event':
                resultStr = handleEvent(msg)  #处理事件推送
        else:
            resultStr = ''    

    return resultStr

#函数把微信XML格式信息转换成字典格式
def xmlContent2Dic(xmlContent):  
    dics = {}  
    elementTree = ET.fromstring(xmlContent)
    if elementTree.tag == 'xml':  
        for child in elementTree :  
            dics[child.tag] = smart_unicode(child.text)  
    return dics

def handleEvent(msg):
    resultStr=''
    if msg['Event'] == 'subscribe':
        content="""您好！欢迎关注宝鹰集团工程综合部！
绑定身份后，可享有宝鹰集团劳务服务平台众多贴心的服务功能。如：直接向总部领导反映项目问题、接收各类集团信息、招投标信息、报名、接收总部工资到账调查信息等。反馈信息全程保密。

<a href="http://lw.szby.cn/complaint/login/default?fid=login">立即绑定身份</a>"""
        resultStr="<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content></xml>"
        resultStr = resultStr % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'text',content)  
    return resultStr

def callback_tj(request):
    wxcpt=WXBizMsgCrypt(Token_tj,EncodingAESKey_tj,AppId_tj)
    sVerifyMsgSig=request.GET.get('signature','')
    sVerifyTimeStamp=request.GET.get('timestamp','')
    sVerifyNonce=request.GET.get('nonce','')
    sVerifyEchoStr=request.GET.get('echostr','')
    
    return HttpResponse(sVerifyEchoStr)
    ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
    if(ret!=0):
        #write_sql("ERR: VerifyURL ret: " + str(ret))
        return HttpResponse(request,"ERR: VerifyURL ret: " + str(ret))
    return HttpResponse(request,sEchoStr)

def callback_gy(request):
    wxcpt=WXBizMsgCrypt(Token_gy,EncodingAESKey_gy,AppId_gy)
    sVerifyMsgSig=request.GET.get('signature','')
    sVerifyTimeStamp=request.GET.get('timestamp','')
    sVerifyNonce=request.GET.get('nonce','')
    sVerifyEchoStr=request.GET.get('echostr','')
    
    response = None
    if request.method == 'GET':
        # response = HttpResponse(checkSignature(request),content_type="text/plain")
        response = HttpResponse(request.GET.get('echostr',''))
    elif request.method == 'POST':
        # print request.body
        response=  HttpResponse(responseMsg_gy(request.body),content_type="application/xml")
    else:
        response = None
    return response
def responseMsg_gy(postContent):
    resultStr=''
    postStr = smart_str(postContent)
    if postStr:
        msg = xmlContent2Dic(postStr)
        if msg['MsgType']:
            if msg['MsgType'] == 'event':
                resultStr = handleEvent_gy(msg)  #处理事件推送
            elif msg['MsgType'] == 'text':
                resultStr = handleMsg_gy(msg)  #处理消息
        else:
            resultStr = ''    

    return resultStr

def ToGBK(s):
    try:
        s=str(s.decode("utf-8").encode("GBK"))
    except:
        s=s
    s = s.replace("\n","\r\n")
    return s
def handleEvent_gy(msg):
    resultStr=''
    if msg['Event'] == 'subscribe':
        return resultStr
        '''content="""感谢您关注供应商服务平台微信公众号，本平台将会根据您绑定的身份，提供相应的工作信息，点击信息底部链接，即可查看学习本平台基本操作方法
<a href="https://lw.szby.cn/fs/manual/manual.docx">【供应商服务平台操作手册】</a>"""
        resultStr="<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content></xml>"
        resultStr = resultStr % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'text',content)  '''
        title = '供应商服务平台操作手册'
        description="""感谢您关注供应商服务平台微信公众号，本平台将会根据您绑定的身份，提供相应的工作信息，点击信息，即可查看学习本平台基本操作方法"""
        picurl = 'https://mmbiz.qpic.cn/mmbiz_jpg/jicaLFFicibTgnNMWjibib4flgC4x81AEA182hhdyjEicFHrrtj2ibyolJHyDibWbiaicGbvH2mQeGtqNBsSXLYOicDZVLhSg/0?wx_fmt=jpeg' 
        url = 'https://lw.szby.cn/lwerp/lw/src/html/operationRule.html'
        resultStr="""<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    <ArticleCount>1</ArticleCount>
    <Articles>
        <item>
            <Title><![CDATA[%s]]></Title>
            <Description><![CDATA[%s]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
        </item>
    </Articles></xml>"""
        resultStr = resultStr % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'news',title,description,picurl,url)  
    return resultStr
def handleMsg_gy(msg):
    resultStr=''
    if msg['Content'] == u'教程':
        return resultStr
        title = '供应商服务平台操作手册'
        description="""感谢您关注供应商服务平台微信公众号，本平台将会根据您绑定的身份，提供相应的工作信息，点击信息，即可查看学习本平台基本操作方法"""
        picurl = 'https://mmbiz.qpic.cn/mmbiz_jpg/jicaLFFicibTgnNMWjibib4flgC4x81AEA182hhdyjEicFHrrtj2ibyolJHyDibWbiaicGbvH2mQeGtqNBsSXLYOicDZVLhSg/0?wx_fmt=jpeg' 
        url = 'https://lw.szby.cn/lwerp/lw/src/html/operationRule.html'
        resultStr="""<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    <ArticleCount>1</ArticleCount>
    <Articles>
        <item>
            <Title><![CDATA[%s]]></Title>
            <Description><![CDATA[%s]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
        </item>
    </Articles></xml>"""
        resultStr = resultStr % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'news',title,description,picurl,url)  
        print ToGBK(resultStr)
    return resultStr
def lw(request):
    # print 'test'
    wxcpt=WXBizMsgCrypt(m_sToken_lw,m_sEncodingAESKey_lw,m_sCorpID)
    sVerifyMsgSig = request.GET.get('msg_signature','')
    sVerifyTimeStamp = request.GET.get('timestamp','')
    sVerifyNonce = request.GET.get('nonce','')
    sVerifyEchoStr = request.GET.get('echostr','')
    ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
    # print '--------------'
    # print sEchoStr
    if(ret!=0):
        #write_sql("ERR: VerifyURL ret: " + str(ret))
        return HttpResponseCORS(request,"ERR: VerifyURL ret: " + str(ret))
    return HttpResponseCORS(request,sEchoStr)

def tj(request):
    # print 'test'
    wxcpt=WXBizMsgCrypt(m_sToken_tj,m_sEncodingAESKey_tj,m_sCorpID)
    sVerifyMsgSig = request.GET.get('msg_signature','')
    sVerifyTimeStamp = request.GET.get('timestamp','')
    sVerifyNonce = request.GET.get('nonce','')
    sVerifyEchoStr = request.GET.get('echostr','')
    ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
    # print '--------------'
    # print sEchoStr
    if(ret!=0):
        #write_sql("ERR: VerifyURL ret: " + str(ret))
        return HttpResponseCORS(request,"ERR: VerifyURL ret: " + str(ret))
    return HttpResponseCORS(request,sEchoStr)

def gy(request):
    # print 'test'
    wxcpt=WXBizMsgCrypt(m_sToken_gy,m_sEncodingAESKey_gy,m_sCorpID)
    sVerifyMsgSig = request.GET.get('msg_signature','')
    sVerifyTimeStamp = request.GET.get('timestamp','')
    sVerifyNonce = request.GET.get('nonce','')
    sVerifyEchoStr = request.GET.get('echostr','')
    ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
    # print '--------------'
    # print sEchoStr
    if(ret!=0):
        #write_sql("ERR: VerifyURL ret: " + str(ret))
        return HttpResponseCORS(request,"ERR: VerifyURL ret: " + str(ret))
    return HttpResponseCORS(request,sEchoStr)