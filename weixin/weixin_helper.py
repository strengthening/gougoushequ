# -*- coding:utf-8 -*-
from __future__ import division
#import os,sys
#sys.path.append('..')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gougoushequ.settings")


#################################################################
from weixin.models import Token_data
from gougoushequ import settings
import requests,json,string,random


#获取微信token
def getToken():
    token = ''
    jsticket = ''
    if Token_data.objects.count()==0 or not Token_data.objects.order_by('-time')[0].has_valid_token():
        r = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+settings.WEIXIN['appid']+'&secret='+settings.WEIXIN['appsecret'],verify=False)
        r1 = requests.get('https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token='+r.json()['access_token']+'&type=jsapi',verify=False)
        token_data = Token_data(token=r.json()['access_token'],jsticket=r1.json()['ticket'])
        token_data.save()
        token = r.json()['access_token']
        jsticket = r1.json()['ticket']
    else:
        token_data = Token_data.objects.order_by('-time')[0]
        token = token_data.token
        jsticket = token_data.jsticket 
    
    return token,jsticket
#生成微信菜单
def setMenu():
    menu = {
    "button": [
        #{
        #    "name": "支付", 
        #    "sub_button": [
        #        {
        #            "type": "scancode_waitmsg", 
        #            "name": "扫码支付", 
        #            "key": "ggsqmenu_0_0", 
        #            "sub_button": [ ]
        #        }, 
        #        {
        #            "type": "view", 
        #            "name": "收款地址", 
        #            "key": "ggsqmenu_0_1",
        #            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+settings.WEIXIN['appid']+"&redirect_uri=http://"+settings.WEIXIN['domainname']+"/weixin/account&response_type=code&scope=snsapi_base&state=123#wechat_redirect",
        #        }
        #    ]
        #}, 
        {
            "name": "活动", 
            "sub_button": [
                #{
                #    "type": "click", 
                #    "name": "狗狗行情", 
                #    "key": "ggsqmenu_1_0", 
                # }, 
                #{
                #    "type": "click", 
                #    "name": "比特行情", 
                #    "key": "ggsqmenu_1_1", 
                #}, 
                #{
                #    "type": "click", 
                #    "name":"莱特行情", 
                #    "key": "ggsqmenu_1_2", 
                #},
                {
                    "type":"click",
                    "name":"doge信息",
                    "key":"ggsqmenu_1_3",
                },{
                    "type":"view",
                    "name":"多吉红包",
                    "key":"ggsqmenu_1_4",
                    "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid="+settings.WEIXIN['appid']+"&redirect_uri=http://"+settings.WEIXIN['domainname']+"/weixin/hongbao&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect",
                }

            ]
        }, 
        {
            "name": "我&我们", 
            "sub_button": [
                {
                    "type":"view",
                    "name":"关于doge",
                    "key":"ggsqmenu_2_0",
                    "url":"http://"+settings.WEIXIN['domainname']+"/introduction/",
                },
                {
                    "type":"view",
                    "name":"我的doge",
                    "key":"ggsqmenu_2_1",
                    "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid="+settings.WEIXIN['appid']+"&redirect_uri=http://"+settings.WEIXIN['domainname']+"/weixin/account&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
                },{
                    "type":"view",
                    "name":"提币/充值",
                    "key":"ggsqmenu_2_2",
                    "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid="+settings.WEIXIN['appid']+"&redirect_uri=http://"+settings.WEIXIN['domainname']+"/weixin/sraccount&response_type=code&scope=snsapi_base&state=123#wechat_redirect",
                },
                {
                    "type":"view",
                    "name":"吾爱doge",
                    "key":"ggsqmenu_2_3",
                    "url":"http://"+settings.WEIXIN['domainname']
                }
            ] 
        }
    ]
    }
    token,jsticket = getToken()
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+token
    r = requests.post(url,data=json.dumps(menu, ensure_ascii=False))
    print r.text

#生成回复文本
def get_xml_text(root,respond_text):
    xml_text = '<xml><ToUserName><![CDATA['+root.getiterator("xml")[0].find('FromUserName').text+']]></ToUserName><FromUserName><![CDATA['+settings.WEIXIN['username']+']]></FromUserName><CreateTime>'+root.getiterator("xml")[0].find('CreateTime').text+'</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA['+respond_text+']]></Content></xml>'
    print root.getiterator("xml")[0].find('FromUserName').text
    return xml_text

def get_xml_pictext(root,title,description,picurl,url):
    xml_pictext = '<xml><ToUserName><![CDATA['+root.getiterator("xml")[0].find('FromUserName').text+']]></ToUserName><FromUserName><![CDATA['+settings.WEIXIN['username']+']]></FromUserName><CreateTime>'+root.getiterator("xml")[0].find('CreateTime').text+'</CreateTime><MsgType><![CDATA[news]]></MsgType><ArticleCount>1</ArticleCount><Articles><item><Title><![CDATA['+title+']]></Title><Description><![CDATA['+description+']]></Description><PicUrl><![CDATA['+picurl+']]></PicUrl><Url><![CDATA['+url+']]></Url></item></Articles></xml>'
    return xml_pictext


def get_tmp_qrcode(sceneid):
    token,jsticket = getToken()
    url ='https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token='+token
    data ={"expire_seconds": 1800, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": sceneid}}}
    print data
    r=requests.post(url,data=json.dumps(data),verify=False)
    print  r.json()
    if r.json().has_key('errcode'):
        return None
    elif r.json().has_key('ticket'):
        ticket =  r.json()['ticket']
        print ticket
        return "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="+ticket

def get_limit_qrcode(sceneid):
    token,jsticket = getToken()
    url ='https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token='+token
    data = {"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": sceneid}}}
    r=requests.post(url,data=json.dumps(data))
    print >>sys.stderr, '----------', sceneid,'---',r.text
    if r.json().has_key('errcode'):
        return None
    elif r.json().has_key('ticket'):
        ticket =  r.json()['ticket']
        print ticket
        return "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="+ticket

def get_random_str(n):
    """ 随机生成n位字符串
    @return: n位字符串
    """
    rule = string.digits
    str = random.sample(rule, n)
    return "".join(str)

def divide_str(txt):
    pos = txt.index('-#-')
    pre_str = txt[0:pos]
    last_str = txt[pos+3:]
    return pre_str,last_str

def divide_str_dvdstr(txt,dvdstr):
    pos = txt.index(dvdstr)
    pre_str = txt[0:pos]
    last_str = txt[pos+3:]
    return pre_str,last_str

def get_hongbao_random(hbsum,hbnum,multiple):
    arr = []
    sumnum = 0
    for i in range(0,hbnum):
        randomnum = random.randint(1, multiple)
        sumnum = sumnum+randomnum
        arr.append(randomnum)
    sumfnum=0
    for n in range(0,hbnum):
        if n!=(hbnum-1):
            fnum = arr[n]/sumnum*hbsum
            arr[n]=float("%.8f" % fnum)
            sumfnum = sumfnum+arr[n]
        else:
            arr[n] = float("%.8f" % (hbsum-sumfnum))
        
 
    return arr

def get_qrsceneid(eventkey):
    if eventkey=="" or eventkey ==None:
        return None
    if eventkey.startswith("qrscene"):
        pos = eventkey.index('_')
        rst = eventkey[pos+1:]
        return rst
    else:
        return None

def trans_number(inumber):
    if inumber == None or inumber == 0:
        inumber = 0
    return inumber

def tran_url(murl):
    pos = murl.index('/?')
    pre_str = murl[0:pos]
    last_str = murl[pos:]
    pre_str = pre_str.replace("=","%3D")
    return pre_str+last_str

if __name__ == '__main__':
    #sys.path.append("/var/www/html/gougoushequ")
    #getToken()
    #setMenu()
    #print get_simple_encode('dfsdfdsf/sdfsdf/sd')
    #print get_random_str(5)
    #print  get_tmp_qrcode('10001')
    #get_tmp_qrcode(100027)
    #get_hongbao_random(111,7,4)
    #print get_qrsceneid("qrscene_100001")
    #get_tmp_qrcode('1')
    tran_url('http://www.5idoge.com/weixin/hbreceivelist/Sm5URDJzUXFkZUYreWtRR3VsbVhKL1BwVEg5SHJWcXVaNVAzaXd0Q1ljRVlsMElkU3duVWF2bVdDaXlLMlZwZktIUjlSZmtNK0dwbG9udXpyRCtXS2EvU0hJQjcycjN3UXZjRktxVzdsbncvQ20rcU8vSVgrbzJIbFZQWEUrL2c=/?code=021911198429b16f6ddec1ac48b50cbu&state=STATE')
