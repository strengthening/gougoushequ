# -*- coding:utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,Http404
from gougoushequ import settings
import requests,hashlib,json
from django.views.decorators.csrf import csrf_exempt
import weixin_helper,weixin_response_helper
from weixin_dogecoind_helper import MyDogecoinConn,DogeConfig
from xml.etree import ElementTree
from WXBizMsgCrypt import WXBizMsgCrypt,MyCrypt
from django.core.urlresolvers import reverse
import sys
import weixin_account_helper
from weixin.models import User,Userdetail,Hongbao,Hbdetail
from django.shortcuts import render_to_response
import time
import uuid,base64,urllib,random,decimal,string 
from django.db.models import Max,Sum
from .tasks  import hello_world1,classify_account


@csrf_exempt
def index(request):
    #return HttpResponse(checkSignature(request))
    if request.method=='GET':
        return  HttpResponse(weixin_helper.getToken())
    else:
        token = settings.WEIXIN['token']
        encodingaeskey = settings.WEIXIN['encodingaeskey']
        appid = settings.WEIXIN['appid']
	root = None 
        decryp_xml = None
        wxcrypt  = None
        print >>sys.stderr, request.body
        if settings.WEIXIN['istest']==1:
            root = ElementTree.fromstring(request.body)
        else:
            wxcrypt = WXBizMsgCrypt(token,encodingaeskey,appid)
            ret,decryp_xml = checkAesSignature(request,wxcrypt)
            root = ElementTree.fromstring(decryp_xml)
            if ret != 0:
                raise Http404

        msgtype = root.getiterator("xml")[0].find('MsgType').text
        if msgtype=='event':
            event = root.getiterator("xml")[0].find('Event').text
            eventkey = root.getiterator("xml")[0].find('EventKey').text
            print eventkey
            if event=='CLICK' and eventkey=='ggsqmenu_1_0':
                #return HttpResponse(encrypt_response(request,weixin_response_helper.respond_dogeprice_text(root),wxcrypt))
                return HttpResponse(weixin_response_helper.respond_dogeprice_text(root))
            elif event=='CLICK' and eventkey=='ggsqmenu_1_1':
                #return HttpResponse(encrypt_response(request,weixin_response_helper.respond_btcprice_text(root),wxcrypt))
                return HttpResponse(weixin_response_helper.respond_btcprice_text(root))
            elif event=='CLICK' and eventkey=='ggsqmenu_1_2':
                #return HttpResponse(encrypt_response(request,weixin_response_helper.respond_ltcprice_text(root),wxcrypt))
                return HttpResponse(weixin_response_helper.respond_ltcprice_text(root))
            elif event=='CLICK' and eventkey=='ggsqmenu_1_3':
                return HttpResponse(encrypt_response(request,weixin_response_helper.respond_mininginfo_text(root),wxcrypt))
                #return HttpResponse(weixin_response_helper.respond_mininginfo_text(root))
            elif event=='SCAN':
                #weixin_account_helper.classify_account(root.getiterator("xml")[0].find('FromUserName').text,event) 
                weixin_account_helper.classify_account(root.getiterator("xml")[0].find('FromUserName').text,event)
                return HttpResponse(weixin_response_helper.respond_hongbao_text(root,None))
                #return HttpResponse(encrypt_response(request,weixin_response_helper.respond_hongbao_text(root),wxcrypt))
            elif event=='scancode_waitmsg' and eventkey=='ggsqmenu_0_0':
                return HttpResponse(weixin_response_helper.respond_test_text(root))
            elif event=='subscribe':
                weixin_account_helper.classify_account(root.getiterator("xml")[0].find('FromUserName').text,event)
                if weixin_helper.get_qrsceneid(eventkey) == None:
                    return HttpResponse("")
                else:
                    qrsceneid = weixin_helper.get_qrsceneid(eventkey)
                    return HttpResponse(weixin_response_helper.respond_hongbao_text(root,qrsceneid))
                return HttpResponse("")
            elif event=='unsubscribe':
                classify_account(root.getiterator("xml")[0].find('FromUserName').text,event)
                return HttpResponse("")
        elif msgtype=='text':
            return HttpResponse("")
        else:
            print ';'
    return HttpResponse(checkSignature(request))

def account(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code==None or state ==None:
        raise Http404
    url = "http://"+settings.WEIXIN['domainname']+"/weixin/account?code="+code+"&state="+state
    jsconfig = getJSConfig(request,url)
    r = requests.post(url='https://api.weixin.qq.com/sns/oauth2/access_token?appid='+settings.WEIXIN['appid']+'&secret='+settings.WEIXIN['appsecret']+'&code='+code+'&grant_type=authorization_code')
    wdata = r.text.encode('utf-8')
    openid = json.loads(wdata)['openid']
    user_data = User.objects.get(openid=openid)
    
    ret,bal = MyDogecoinConn().getbalance(user_data.account,DogeConfig.DOGE_MIN_CONF)
    ret1,bal1 = MyDogecoinConn().getbalance(user_data.account,0)
    if ret!=0 or ret1!=0:
        raise Http404
    unconbal = bal1-bal
    if unconbal ==0:
        unconbal="0.00000000"
    lockamount = user_data.lockamount
    bal = decimal.Decimal(bal)-lockamount
    address = user_data.address
    return render_to_response('account.html',{'address':address,'lockamount':lockamount,'bal':bal,'unconbal':unconbal,'jsconfig':jsconfig})

def sraccount(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    
    if code==None or state ==None:
        raise Http404

    url = "http://"+settings.WEIXIN['domainname']+"/weixin/sraccount?code="+code+"&state="+state
    jsconfig = getJSConfig(request,url)

    r = requests.post(url='https://api.weixin.qq.com/sns/oauth2/access_token?appid='+settings.WEIXIN['appid']+'&secret='+settings.WEIXIN['appsecret']+'&code='+code+'&grant_type=authorization_code')
    wdata = r.text.encode('utf-8')
    print >>sys.stderr, '----------', wdata,jsconfig
    wjdata = json.loads(wdata)
    access_token = wjdata['access_token']
    openid = wjdata['openid']
    mc = MyCrypt(settings.WEIXIN['encodingaeskey'],settings.WEIXIN['appid'])
    timestamp = '%d' % (time.time()*1000)
    ret,entext = mc.EncryptMsg(openid+"-##"+timestamp)

    if ret!=0:
        entext = None
    user_data = User.objects.get(openid=openid)
    ret,bal = MyDogecoinConn().getbalance(user_data.account,DogeConfig.DOGE_MIN_CONF)
    if ret!=0:
        raise Http404
 
    lockamount = user_data.lockamount
    bal = decimal.Decimal(bal)-lockamount-1
    if bal<0:
        bal=0.00000000
    return render_to_response('sraccount.html',{'entext':entext,'address':user_data.address,'bal':bal,'jsconfig':jsconfig}) 


def hongbao(request):
    #return render_to_response('hongbao.html',{'enText':'2131231'})
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code==None or state ==None:
        raise Http404
    r = requests.post(url='https://api.weixin.qq.com/sns/oauth2/access_token?appid='+settings.WEIXIN['appid']+'&secret='+settings.WEIXIN['appsecret']+'&code='+code+'&grant_type=authorization_code')
    wdata = r.text.encode('utf-8')
    
    wjdata = json.loads(wdata)
    access_token = wjdata['access_token']
    openid = wjdata['openid']
    mc = MyCrypt(settings.WEIXIN['encodingaeskey'],settings.WEIXIN['appid'])
    timestamp = '%d' % (time.time()*1000)
    ret,enText = mc.EncryptMsg(openid+"-#-"+timestamp)
    if ret!=0:
        enText = None
    enText = base64.urlsafe_b64encode(enText)
    user_data = User.objects.get(openid=openid)
    ud_data = Userdetail.objects.get(openid=openid)
    
    #TODO:定时更新用户数据
    if user_data.ud_user.all().count()==0:
        weixin_account_helper.updateUserdetail(user_data)
    
    #myhbs = Hongbao.objects.filter(hbhost=openid,hbstime__gte=str(int(timestamp)-1000*30*60))

    url = "http://"+settings.WEIXIN['domainname']+"/weixin/hongbao?code="+code+"&state="+state
    jsconfig = getJSConfig(request,url)
    confhburl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+settings.WEIXIN['appid']+"&redirect_uri=http://"+settings.WEIXIN['domainname']+"/weixin/confhb/"+enText+"&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
    hbreceivelisturl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+settings.WEIXIN['appid']+"&redirect_uri=http://"+settings.WEIXIN['domainname']+"/weixin/hbreceivelist/"+enText+"&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
    hbsendlisturl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+settings.WEIXIN['appid']+"&redirect_uri=http://"+settings.WEIXIN['domainname']+"/weixin/hbsendlist/"+enText+"&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
    return render_to_response('hongbao.html',{'enText':enText,'user_data':user_data,'userdetail':ud_data,'jsconfig':jsconfig,'confhburl':confhburl,'hbreceivelisturl':hbreceivelisturl,'hbsendlisturl':hbsendlisturl})

def hongbaodesc(request,enhbid):
    
    content = {}
    url="http://"+request.get_host()+request.get_full_path()
    url = url.replace('=',"%3D")
    print >> sys.stderr, '------hehehehe----',url
    if request.GET.get('ismine'):
        content['ismine'] = request.GET.get('ismine')

    try:
        mc = MyCrypt(settings.WEIXIN['encodingaeskey'], settings.WEIXIN['appid'])
        ret,detxt = mc.DecryptMsg(base64.urlsafe_b64decode(enhbid.encode("utf-8")))
        if ret!=0:
            raise Http404 
        
        jsconfig = getJSConfig(request,url)
        hbid,hbstime = weixin_helper.divide_str_dvdstr(detxt,'-#-')
        hongbao_data = Hongbao.objects.get(hbid=hbid,hbstime=hbstime)
        if hongbao_data is None:
            raise Http404        

        ntimestamp = int(time.time()*1000)
        if hongbao_data.hbtype == 'temporary':        
            if (ntimestamp-1000*60*30) > int(hbstime):
                return render_to_response('hongbao_fail.html',{'errmsg':'超过红包有效时限，遗憾呐！！'})
        elif hongbao_data.hbtype == 'eternal':
            if (ntimestamp-1000*60*60*24) > int(hbstime):
                return render_to_response('hongbao_fail.html',{'errmsg':'超过红包有效时限，遗憾呐！！'})
            if (ntimestamp-1000*60*29)>int(hongbao_data.qrcodeutime):
                qrcodeurl = weixin_helper.get_tmp_qrcode(hbid)
                if qrcodeurl is None:
                    raise Http404
                hongbao_data.hbqrcodeurl = qrcodeurl
                hongbao_data.qrcodeutime = ntimestamp
                hongbao_data.save()

        user_data = hongbao_data.hbhost
        content['nickname'] = user_data.nickname
        content['hbsum'] = hongbao_data.hbsum
        content['hbnum'] = hongbao_data.hbnum
        content['hbgreetings'] = hongbao_data.hbgreetings
        content['gethburl']="https://open.weixin.qq.com/connect/oauth2/authorize?appid="+settings.WEIXIN['appid']+"&redirect_uri=http://"+settings.WEIXIN['domainname']+"/weixin/gethb/"+enhbid+"&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
        content['hbqrcodeurl'] = hongbao_data.hbqrcodeurl
        content['jsconfig'] = jsconfig

    except Exception,e:
        print >>sys.stderr, '----------', e
        raise Http404
    
    return render_to_response('hongbao_success.html',content)

def confhb(request,entext):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code == None or state == None:
        raise  Http404
    r = requests.get(url="https://api.weixin.qq.com/sns/oauth2/access_token?appid="+settings.WEIXIN['appid']+"&secret="+settings.WEIXIN['appsecret']+"&code="+code+"&grant_type=authorization_code")
    r.encoding = 'utf-8'
    jdata = json.loads(r.text)
    
    access_token = jdata['access_token']
    openid = jdata['openid']
    
    mc = MyCrypt(settings.WEIXIN['encodingaeskey'],settings.WEIXIN['appid'])
    ret,detext = mc.DecryptMsg(base64.urlsafe_b64decode(entext.encode("utf-8")))
    openid1,utimestamp = weixin_helper.divide_str_dvdstr(detext,'-#-')
    if openid!=openid1:
        raise Http404
    else:
        print >>sys.stderr, '--htmlhtml1--',entext
    url = weixin_helper.tran_url("http://"+request.get_host()+request.get_full_path())
    jsconfig = getJSConfig(request,url)
    return render_to_response('hongbao_config.html',{'entext':entext,'jsconfig':jsconfig,})

def hbreceivelist(request,entext):
    #imgurl = request.GET.get('imgurl')
    #nickname = request.GET.get('nickname')
    mc = MyCrypt(settings.WEIXIN['encodingaeskey'],settings.WEIXIN['appid'])
    ret,entext = mc.DecryptMsg(base64.urlsafe_b64decode(entext.encode("utf-8")))
    openid,utimestamp = weixin_helper.divide_str_dvdstr(entext,'-#-')
    user_data = User.objects.raw("select a.id as id,a.nickname as nickname,b.headimgurl as imgurl from weixin_user a,weixin_userdetail b where a.openid='"+openid+"' and b.openid_id=a.openid")
    #todo:判断超时问题

    hbsum =  weixin_helper.trans_number(Hbdetail.objects.filter(hbdowneropenid=openid,hbdused=True).aggregate(Sum('hbdnum'))['hbdnum__sum'])
    hbnum =  weixin_helper.trans_number(Hbdetail.objects.filter(hbdowneropenid=openid,hbdused=True).count())
    #myreceivehbs = Hbdetail.objects.filter(hbdowneropenid=openid,hbdused=True).order_by('hbdusedtime')[:10]
    myreceivehbs = Hbdetail.objects.raw("select a.id,FROM_UNIXTIME(left(a.hbdusedtime,10),'%%Y-%%m-%%d') as hbdusedtime,b.hbtype as hbtype,a.hbdnum as hbdnum,c.nickname as nickname from weixin_hbdetail a,weixin_hongbao b,weixin_user c where a.hbdowneropenid_id='"+openid+"' and a.hbdused='1' and a.hbduuid_id =b.hbuuid and c.openid = b.hbhost_id  order by a.hbdusedtime desc")[:10]
    url = weixin_helper.tran_url("http://"+request.get_host()+request.get_full_path())
    jsconfig = getJSConfig(request,url)
    return render_to_response('hongbao_hbreceivelist.html',{'entext':entext,'imgurl':user_data[0].imgurl,'nickname':user_data[0].nickname,'hbsum':hbsum,'hbnum':hbnum,'myreceivehbs':myreceivehbs,'jsconfig':jsconfig,})

def hbsendlist(request,entext):
    #imgurl = request.GET.get('imgurl')
    #nickname = request.GET.get('nickname')
    mc = MyCrypt(settings.WEIXIN['encodingaeskey'],settings.WEIXIN['appid'])
    ret,entext = mc.DecryptMsg(base64.urlsafe_b64decode(entext.encode("utf-8")))
    openid,utimestamp = weixin_helper.divide_str_dvdstr(entext,'-#-')
    user_data = User.objects.raw("select a.id as id,a.nickname as nickname,b.headimgurl as imgurl from weixin_user a,weixin_userdetail b where a.openid='"+openid+"' and b.openid_id=a.openid")
    #todo:判断超时问题

    hbssum = weixin_helper.trans_number(Hongbao.objects.filter(hbhost=openid).aggregate(Sum('hbsum'))['hbsum__sum'])
    hbsnum = weixin_helper.trans_number(Hongbao.objects.filter(hbhost=openid).aggregate(Sum('hbnum'))['hbnum__sum'])
    mysendhbs = Hongbao.objects.raw("select a.id, a.hbuuid as hbuuid, a.hbnum as hbnum , count(b.hbdowneropenid_id) as  hbdusednum ,FROM_UNIXTIME(left(a.hbstime,10),'%%Y-%%m-%%d') as hbtime ,a.hbtype as bhtype ,a.hbsum as hbsum,replace(a.enhbid,'=','%%3D') as enhbid from weixin_hongbao a right join weixin_hbdetail b on a.hbuuid=b.hbduuid_id where a.hbhost_id='"+openid+"'  group by a.hbuuid order by a.hbstime desc")[:10]
    url = weixin_helper.tran_url("http://"+request.get_host()+request.get_full_path())
    jsconfig = getJSConfig(request,url)
    return render_to_response('hongbao_hbsendlist.html',{'entext':entext,'imgurl':user_data[0].imgurl,'nickname':user_data[0].nickname,'mysendhbs':mysendhbs,'hbssum':hbssum,'hbsnum':hbsnum,'jsconfig':jsconfig})

def hbrichlist(request,entext):
    return render_to_response('hongbao_hbrichlist.html',{'entext':entext})

@csrf_exempt
def senddoge(request):
    if request.method=='GET':
        raise  Http404
    outaddress = request.POST.get('outaddress')
    outnum = request.POST.get('outnum')
    entext = request.POST.get('entext')
    #return HttpResponse(outaddress+outnum+entext)
    if outaddress==None or outnum==None or entext==None:
        return HttpResponse(json.dumps({'success':1,'errmsg':'请填写完整提币信息'}, ensure_ascii=False), content_type="application/json")
    mc = MyCrypt(settings.WEIXIN['encodingaeskey'],settings.WEIXIN['appid'])
    ret,detxt = mc.DecryptMsg(entext)
    if ret!=0:
        raise Http404
    openid,stimestamp = weixin_helper.divide_str_dvdstr(detxt,"-##")
    ntimestamp = time.time()*1000
    if (ntimestamp-1000*60*5)>int(stimestamp):
        return HttpResponse(json.dumps({'success':1,'errmsg':'此页面已经超时，请关闭此页，重新打开'}, ensure_ascii=False), content_type="application/json")
    user_data = User.objects.get(openid=openid)
    if user_data.lockamount < 0 :
        return HttpResponse(json.dumps({'success':1,'errmsg':'账户异常！'}, ensure_ascii=False), content_type="application/json")
    ret,rst = MyDogecoinConn().sendfrom(user_data,user_data.account,outaddress,outnum,DogeConfig.DOGE_MIN_CONF,str(ntimestamp),"from http://www.5idoge.com")
    if ret!=0:
        return HttpResponse(json.dumps({'success':1,'errmsg':rst}, ensure_ascii=False), content_type="application/json")
    return HttpResponse(json.dumps({'success':ret,'errmsg':rst}, ensure_ascii=False), content_type="application/json")
    
    


@csrf_exempt
def sendhb(request):
    if request.method=='GET':
        raise  Http404
    hbsum = request.POST.get('hbsum')
    hbnum = request.POST.get('hbnum')
    entext = request.POST.get('entext')
    hbtype = request.POST.get('hbtype')
    hbgreetings = request.POST.get('hbgreetings')

    enhbid=''
    try:
        mc = MyCrypt(settings.WEIXIN['encodingaeskey'],settings.WEIXIN['appid'])
        ret,entext = mc.DecryptMsg(base64.urlsafe_b64decode(entext.encode("utf-8")))
        openid,utimestamp = weixin_helper.divide_str_dvdstr(entext,'-#-')

        user_data = User.objects.get(openid=openid)
        if user_data is None:
            return render_to_response('hongbao_config.html',{'entext':entext,'errmsg':'还没有关注【吾爱doge】公众账号吧！请关注公众账号再发送'})
        else:
            nickname = user_data.nickname
        stimestamp = int(time.time()*1000)
        if (stimestamp-int(utimestamp))>30*60*1000:
            return render_to_response('hongbao_config.html',{'entext':entext,'errmsg':'链接超时，请关闭此页面重新点击活动--》红包'})

        ret,rst = MyDogecoinConn().getbalance(user_data.account,DogeConfig.DOGE_MIN_CONF)
        print >>sys.stderr, ret,type(rst)
        if ret!=0:
            return HttpResponse('内部异常！！')
        if rst<(decimal.Decimal(hbsum)+user_data.lockamount):
            return HttpResponse('主人，你的账号里doge不足啊')
     
        hbid = 0
        if hbtype == 'temporary' or hbtype == 'eternal':
            if Hongbao.objects.filter(hbid__gt=100000).count() == 0:
                hbid = 100001
            else:
                hbid = int(Hongbao.objects.filter(hbid__gt=100000).aggregate(Max('hbid'))['hbid__max'])+1

        hongbao_data = Hongbao(
            hbuuid = str(uuid.uuid4()),
            hbtype = hbtype,
            hbid = hbid,
            hbnum = hbnum,
            hbrandomtype = '1',
            hbsum = hbsum,
            hbhost = user_data,
            hbgreetings = hbgreetings,
            hbstime = stimestamp,
            hbutime = utimestamp,
            qrcodeutime = stimestamp,
        )
        hongbao_data.save()
        hbdarr = weixin_helper.get_hongbao_random(float(hbsum),int(hbnum),random.randint(3,5))
        print >>sys.stderr, hbdarr
        for n in range(0,len(hbdarr)):
            hbd_data = Hbdetail(
                hbduuid = hongbao_data,
                hbdseq = n,
                hbdnum = hbdarr[n],
                hbdused = False,
                #hbdowneropenid = user_data,
            )
            hbd_data.save()        

        hbqrcodeurl = weixin_helper.get_tmp_qrcode(hbid)
        ret,enhbid = mc.EncryptMsg(str(hbid)+'-#-'+str(stimestamp))
        enhbid = base64.urlsafe_b64encode(enhbid)

        if hbqrcodeurl is None:
            hongbao_data.hbqrcodeurl='fail'
        hongbao_data.hbqrcodeurl = hbqrcodeurl
        hongbao_data.enhbid = enhbid
        hongbao_data.save()
        user_data.lockamount = decimal.Decimal(hbsum)+user_data.lockamount
        user_data.save()
        #TODO: 区分限时和不限时的差别
        if hongbao_data.hbtype == 'temporary':
            hello_world1.apply_async((hongbao_data.hbuuid,user_data.openid), countdown=60*32, retry=False)
        elif hongbao_data.hbtype == 'eternal':
            hello_world1.apply_async((hongbao_data.hbuuid,user_data.openid), countdown=60*60*24, retry=False)
        print >> sys.stderr, '------sendhb base64------', enhbid 
    except Exception, e:
        print >> sys.stderr, '------sendhberror------', e
        return render_to_response('hongbao_fail.html')
    return HttpResponseRedirect(reverse('weixin.views.hongbaodesc', args=(enhbid,))+"/?ismine=1")

def gethb(request,enhbid):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code == None or state == None:
        raise  Http404
    mc = MyCrypt(settings.WEIXIN['encodingaeskey'],settings.WEIXIN['appid'])
    ret,detxt = mc.DecryptMsg(base64.urlsafe_b64decode(enhbid.encode("utf-8")))
    if ret!=0:
        raise  Http404
    try:
        r = requests.get(url="https://api.weixin.qq.com/sns/oauth2/access_token?appid="+settings.WEIXIN['appid']+"&secret="+settings.WEIXIN['appsecret']+"&code="+code+"&grant_type=authorization_code")
        r.encoding = 'utf-8'
        jdata = json.loads(r.text)
        access_token = jdata['access_token']
        openid = jdata['openid']
        user_data = User.objects.get(openid=openid)
        hbid,hbstime = weixin_helper.divide_str(detxt)
        hongbao_data = Hongbao.objects.get(hbid=hbid,hbstime=hbstime)

        if hongbao_data.hbtype == 'temporary':
            if int(time.time()*1000)-29.9*60*1000>int(hbstime):
                return HttpResponse('唉！已经过了这个多吉红包的时限，期待下次多吉红包时刻吧！')
        elif hongbao_data.hbtype == 'eternal':
            if int(time.time()*1000)-23.99*60*60*1000>int(hbstime):
                return HttpResponse('唉！已经过了这个多吉红包的时限，期待下次多吉红包时刻吧！')
        
        if hongbao_data.hbhost.openid == openid:
            return HttpResponse('主人，自己发的红包还是留给别人抢吧！！')
        if hongbao_data.hbd_hb.filter(hbdused = True).count() == hongbao_data.hbnum:
            return HttpResponse('主人，你来晚了。。这个多吉红包已经被抢光啦！')

        if hongbao_data.hbd_hb.filter(hbdused = True,hbdowneropenid = user_data).count()>0:
            return HttpResponse('主人，你已经拿过这个红包了，让别人也多吉一下吧~')

        hbd_data = hongbao_data.hbd_hb.filter(hbdused = False)[0]
        ret,conn = MyDogecoinConn().move(hongbao_data.hbhost,hongbao_data.hbhost.account,user_data.account,hbd_data.hbdnum,DogeConfig.DOGE_MIN_CONF,"hongbao")
        if ret!=0:
            return HttpResponse('领红包失败！！！！失败中的失败！！！')

        
        hbd_data.hbdused = True
        hbd_data.hbdowneropenid = user_data
        hbd_data.hbdusedtime = int(time.time()*1000)
        hbd_data.save()
        hbhost  = hongbao_data.hbhost
        hbhost.lockamount = hbhost.lockamount-hbd_data.hbdnum
        hbhost.save()
    except Exception,e:
        print >>sys.stderr, '------gethb------', e
        return render_to_response('hongbao_fail.html')
     
    return render_to_response('gethongbao_success.html',{'hbdnum':hbd_data.hbdnum}) # HttpResponse('成功抢到红包了，红包中放了'+hbd_data.hbdnum+'个doge!')

def test(request):
    return render_to_response('hongbao.html',{'hbdnum':11})

def checkSignature(request):
    signature=request.GET.get('signature',None)
    timestamp=request.GET.get('timestamp',None)
    nonce=request.GET.get('nonce',None)
    echostr=request.GET.get('echostr',None)

    token=settings.WEIXIN['token']
    print token

    tmplist=[token,timestamp,nonce]
    tmplist.sort()
    tmpstr="%s%s%s"%tuple(tmplist)
    tmpstr=hashlib.sha1(tmpstr).hexdigest()
    print signature,timestamp,nonce
    if tmpstr == signature:
        print echostr
        return echostr
    else:
        return False

def getJSConfig(request,url):
    token,jsticket = weixin_helper.getToken()
    noncestr = ''.join(random.sample(string.ascii_letters+string.digits,8))
    timestamp = str(int(time.time()))
   
    string1 = "jsapi_ticket="+jsticket+"&noncestr="+noncestr+"&timestamp="+timestamp+"&url="+url
    signature =  hashlib.sha1(string1).hexdigest()

    jsconfig = {'debug':settings.WEIXIN['istest'],'appId':settings.WEIXIN['appid'],'timestamp':timestamp,'nonceStr':noncestr,'signature':signature}
    return jsconfig

def checkAesSignature(request,wxcrypt):
    signature=request.GET.get('signature',None)
    timestamp=request.GET.get('timestamp',None)
    nonce=request.GET.get('nonce',None)
    #echostr=request.GET.get('echostr',None)

    encrypt_type = request.GET.get('encrypt_type',None)
    msg_signature = request.GET.get('msg_signature',None)

    ret,decryp_xml = wxcrypt.DecryptMsg(request.body,msg_signature,timestamp,nonce)
    #print ret ,decryp_xml
    #print >>sys.stderr , decryp_xml
    return ret,decryp_xml



def encrypt_response(request,data,wxcrypt):
    #return data
    timestamp=request.GET.get('timestamp',None)
    nonce=request.GET.get('nonce',None)
    ret,xml_content = wxcrypt.EncryptMsg(data,timestamp)
    #print >>sys.stderr , xml_content
    return xml_content
    
    


