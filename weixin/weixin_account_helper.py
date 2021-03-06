# -*- coding:utf-8 -*-
#import sys,os
#sys.path.append('..')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gougoushequ.settings")


#----------------------------------------------------------------------

from gougoushequ import settings
from  weixin_dogecoind_helper import MyDogecoinConn
from weixin.models import User,Userdetail
import time
import traceback
from PIL import Image
import qrcode
from weixin import  weixin_helper
import requests,json


def register_account(openid):
    try:
        ret,conn = MyDogecoinConn().getConn()
        if ret!=0:
            return None
        address =  conn.getaccountaddress(settings.WEIXIN['prefix']+openid)

        user_data = User(
            openid = openid,
            account = settings.WEIXIN['prefix']+openid,
            address = address,
            lockamount = 0,
            createdtimestamp = int(time.time()*1000),
            subscribetimestamp = int(time.time()*1000),
            subscribe = True,
            istest = settings.WEIXIN['istest'],
        )
        user_data.save()
        #generateImg(address,'dogecoin:')
        #updateUserdetail(user_data)
        import tasks
        tasks.gen_account_info(user_data)#异步生成二维码、更新用户的详细信息
    except Exception, e:
        traceback.print_exc() 
        #print e
        #print >>sys.stderr, e

def classify_account(openid,action):
    try:
        if action=='subscribe' or action=='SCAN':
            if User.objects.filter(openid=openid).count()==1:
                user_data = User.objects.get(openid=openid)
                if user_data.subscribe:
                    return
                user_data.subscribe = True
                user_data.subscribetimestamp = int(time.time()*1000)
                user_data.save()
            else:
                register_account(openid)
        elif action=='unsubscribe':
            user_data = User.objects.get(openid=openid)
            user_data.subscribe = False
            user_data.save()
        
    except Exception, e:
        traceback.print_exc()

def verify_address(address):
    print address
    #return 
    ret,result = MyDogecoinConn().getConn()
    hehe = result.validateaddress(address)
    print hehe
    return hehe
    

def generateImg(address,prefix):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2
    )
    qr.add_data(prefix+address)
    qr.make(fit=True)
 
    img = qr.make_image()
    img = img.convert("RGBA")
    icon = Image.open(settings.WEIXIN['fileurl']+"gougoushequ/favicon.png")
 
    img_w, img_h = img.size
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)
 
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
 
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    img.paste(icon, (w, h), icon)
 
    img.save(settings.WEIXIN['fileurl']+"gougoushequ/static/qrcode/"+address+".png")

def updateUserdetail(user_data):
    token,jsticket = weixin_helper.getToken()
    r = requests.get(url='https://api.weixin.qq.com/cgi-bin/user/info?access_token='+token+'&openid='+user_data.openid+'&lang=zh_CN')
    r.encoding = 'utf-8'
    jdata = json.loads(r.text.encode('utf-8'))
    print jdata
    ud_data = Userdetail(
        openid = user_data,
        sex = jdata['sex'],
        language = jdata['language'],
        city = jdata['city'],
        province = jdata['province'],
        country = jdata['country'],
        headimgurl = jdata['headimgurl'],
        updatetime = time.time()*1000,
    )
    ud_data.save()
    user_data.nickname = jdata['nickname']
    user_data.save()

if __name__ == '__main__':
    #generateImg('DD2UBru51aoxMUwWvFaiL32Mw28pHkJe8B','dogecoin:')
    user_data = User.objects.get(openid='o3-17uBfR2HBCkIPsQ1iYvv6l_ag')
    #updateUserdetail(user_data)
    #verify_address('DKhnu9vYHcbq9hxm1dRo4xxYGwQz9vbVCT')


