# -*- coding:utf-8 -*-

import os,sys
#sys.path.append('..')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gougoushequ.settings")



###########################################

from django.core.cache import cache
import weixin_helper,weixin_account_helper
from weixin_dogecoind_helper import MyDogecoinConn
from django.http import Http404
from gougoushequ import settings
from weixin.models import User,Hongbao
import time
from weixin.weixin_dogecoind_helper import DogeConfig

def respond_btcprice_text(root):
    try:
        caches = cache.get_many(['btc_ok_last', 'btc_ok_buy', 'btc_ok_sell','btc_ok_high','btc_ok_low','btc_ok_vol','btc_huobi_last','btc_huobi_buy','btc_huobi_sell','btc_huobi_high','btc_huobi_low','btc_huobi_vol','btc_bitstamp_last','btc_bitstamp_buy','btc_bitstamp_sell','btc_bitstamp_high','btc_bitstamp_low','btc_bitstamp_vol'])
        btc_ok_vol ="%.1f" %float(caches['btc_ok_vol'])
        btc_huobi_vol ="%.1f" %float(caches['btc_huobi_vol'])
        btc_bitstamp_vol ="%.1f" %float(caches['btc_bitstamp_vol'])
        btc_ok_str = '【OKCoin最新行情】\n'+'价格:'+caches['btc_ok_last']+'CNY\n买一:'+caches['btc_ok_buy']+'CNY\n卖一:'+caches['btc_ok_sell']+'CNY\n最高:'+caches['btc_ok_high']+'CNY\n最低:'+caches['btc_ok_low']+'CNY\n成交量:'+str(btc_ok_vol)+'\n\n'

        btc_huobi_str = '【火币最新行情】\n'+'价格:'+caches['btc_huobi_last']+'CNY\n买一:'+caches['btc_huobi_buy']+'CNY\n卖一:'+caches['btc_huobi_sell']+'CNY\n最高:'+caches['btc_huobi_high']+'CNY\n最低:'+caches['btc_huobi_low']+'CNY\n成交量:'+str(btc_huobi_vol)+'\n\n'
        btc_bitstamp_str = '【bitstamp最新行情】\n'+'价格:'+caches['btc_bitstamp_last']+'USD\n买一:'+caches['btc_bitstamp_buy']+'USD\n卖一:'+caches['btc_bitstamp_sell']+'USD\n最高:'+caches['btc_bitstamp_high']+'USD\n最低:'+caches['btc_bitstamp_low']+'USD\n成交量:'+str(btc_bitstamp_vol)
        return weixin_helper.get_xml_text(root,btc_ok_str+btc_huobi_str+btc_bitstamp_str)
    except Exception,e:
        print >>sys.stderr , e
        raise Http404

def respond_ltcprice_text(root):
    try:
        caches = cache.get_many(['ltc_ok_last', 'ltc_ok_buy', 'ltc_ok_sell','ltc_ok_high','ltc_ok_low','ltc_ok_vol','ltc_huobi_last','ltc_huobi_buy','ltc_huobi_sell','ltc_huobi_high','ltc_huobi_low','ltc_huobi_vol','ltc_cryptsy_last','ltc_cryptsy_buy','ltc_cryptsy_sell','ltc_cryptsy_high','ltc_cryptsy_low','ltc_cryptsy_vol'])

        ltc_ok_vol ="%.1f" %float(caches['ltc_ok_vol'])
        ltc_huobi_vol ="%.1f" %float(caches['ltc_huobi_vol'])
        ltc_cryptsy_vol ="%.1f" %float(caches['ltc_cryptsy_vol'])

        ltc_ok_str = '【OKCoin最新行情】\n'+'价格:'+caches['ltc_ok_last']+'CNY\n买一:'+caches['ltc_ok_buy']+'CNY\n卖一:'+caches['ltc_ok_sell']+'CNY\n最高:'+caches['ltc_ok_high']+'CNY\n最低:'+caches['ltc_ok_low']+'CNY\n成交量:'+str(ltc_ok_vol)+'\n\n'
        ltc_huobi_str = '【火币最新行情】\n'+'价格:'+caches['ltc_huobi_last']+'CNY\n买一:'+caches['ltc_huobi_buy']+'CNY\n卖一:'+caches['ltc_huobi_sell']+'CNY\n最高:'+caches['ltc_huobi_high']+'CNY\n最低:'+caches['ltc_huobi_low']+'CNY\n成交量:'+str(ltc_huobi_vol)+'\n\n'
        ltc_cryptsy_str = '【cryptsy最新行情】\n'+'价格:'+caches['ltc_cryptsy_last']+'BTC\n买一:'+caches['ltc_cryptsy_buy']+'BTC\n卖一:'+caches['ltc_cryptsy_sell']+'BTC\n最高:'+caches['ltc_cryptsy_high']+'BTC\n最低:'+caches['ltc_cryptsy_low']+'BTC\n成交量:'+str(ltc_cryptsy_vol)

        return weixin_helper.get_xml_text(root,ltc_ok_str+ltc_huobi_str+ltc_cryptsy_str)
    except Exception,e:
        print >>sys.stderr , e
        raise Http404 

def respond_dogeprice_text(root):
    try:    
        caches = cache.get_many(['btc_ok_last','btc_huobi_last','bter_last', 'bter_buy', 'bter_sell','bter_high','bter_low','bter_vol','btc38_last','btc38_buy','btc38_sell','btc38_high','btc38_low','btc38_vol','cryptsy_last','cryptsy_buy','cryptsy_sell','cryptsy_high','cryptsy_low','cryptsy_vol','btc100_last','btc100_buy','btc100_sell','btc100_high','btc100_low','btc100_vol'])
 
        btc_ok_price =float(caches['btc_ok_last'])
        btc_huobi_price =float(caches['btc_huobi_last'])
        cryptsy_price = float(caches['cryptsy_last'])
        cryptsy_cny_price ="%.7f" %float((btc_ok_price+btc_huobi_price)/2*cryptsy_price)
#        print btc_ok_price, btc_huobi_price, cryptsy_price,cryptsy_cny_price

        bter_vol ="%.1f" %float(caches['bter_vol'])
        btc38_vol ="%.1f" %float(caches['btc38_vol'])
        cryptsy_vol ="%.1f" %float(caches['cryptsy_vol'])
        btc100_vol = "%.1f" % float (caches['btc100_vol'])

        bter_str = '【比特儿最新行情】\n'+'价格:'+caches['bter_last']+'CNY\n买一:'+caches['bter_buy']+'CNY\n卖一:'+caches['bter_sell']+'CNY\n最高:'+caches['bter_high']+'CNY\n最低:'+caches['bter_low']+'CNY\n成交量:'+str(bter_vol)+'\n\n'
        btc38_str = '【比特时代最新行情】\n'+'价格:'+caches['btc38_last']+'CNY\n买一:'+caches['btc38_buy']+'CNY\n卖一:'+caches['btc38_sell']+'CNY\n最高:'+caches['btc38_high']+'CNY\n最低:'+caches['btc38_low']+'CNY\n成交量:'+str(btc38_vol)+'\n\n'
        btc100_str = '【btc100最新行情】\n'+'价格:'+caches['btc100_last']+'CNY\n买一:'+caches['btc100_buy']+'CNY\n卖一:'+caches['btc100_sell']+'CNY\n最高:'+caches['btc100_high']+'CNY\n最低:'+caches['btc100_low']+'CNY\n成交量:'+str(btc100_vol)+'\n\n'
        cryptsy_str = '【C网最新行情】\n'+'价格:'+caches['cryptsy_last']+'BTC\n约合:'+cryptsy_cny_price+'CNY\n买一:'+caches['cryptsy_buy']+'BTC\n'+'卖一:'+caches['cryptsy_sell']+'BTC\n最高:'+caches['cryptsy_high']+'BTC\n最低:'+caches['cryptsy_low']+'BTC\n成交量:'+str(cryptsy_vol)

        return weixin_helper.get_xml_text(root,btc38_str+bter_str+btc100_str+cryptsy_str)
    except Exception,e:
        print >>sys.stderr,e
        raise Http404

def respond_mininginfo_text(root):
    try:
        #print >>sys.stderr,'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        #conn = dogecoinrpc.connect_to_remote(settings.RPC_USERNAME, settings.RPC_PASSWORD, host=settings.RPC_IP, port=22555)
        ret,conn = MyDogecoinConn().getConn()
        if ret!=0:
            raise Http404
        
        rpc_mininginfo = conn.getmininginfo()
        hash_rate_float = float(rpc_mininginfo.networkhashps)/1000000000
        hash_rate="%.1fGHash/s" % hash_rate_float

        dogeinfo_str = '【doge最新信息】\n'+'当前区块:'+str(rpc_mininginfo.blocks)+'\n当前难度:'+"%.1f" % float(rpc_mininginfo.difficulty)+'\n当前算力:'+hash_rate
        #print dogeinfo_str
        return weixin_helper.get_xml_text(root,dogeinfo_str)
    except Exception,e:
        print >>sys.stderr, e
        raise Http404

def respond_test_text(root):
    #print >> sys.stderr,root.getiterator("xml")[0].getiterator("ScanCodeInfo")[0].find('ScanResult').text
    address = root.getiterator("xml")[0].getiterator("ScanCodeInfo")[0].find('ScanResult').text
    print >> sys.stderr,weixin_account_helper.verify_address(address) 
    title=address
    description='test'
    picurl='fsdfsdf'
    url='http://'+settings.WEIXIN['domainname']+'/weixin/payment?msg='+root.getiterator("xml")[0].find('FromUserName').text+root.getiterator("xml")[0].getiterator("ScanCodeInfo")[0].find('ScanResult').text+str(time.time()*1000)
    return weixin_helper.get_xml_pictext(root,title,description,picurl,url)
   
def respond_hongbao_text(root,qrsceneid):
    openid = root.getiterator("xml")[0].find('FromUserName').text
    print >> sys.stderr,'-----------------',openid
    event = root.getiterator("xml")[0].find('Event').text
    eventkey = ""
    if qrsceneid == None:
        eventkey = root.getiterator("xml")[0].find('EventKey').text
    else:
        eventkey = qrsceneid
    hongbao_data = Hongbao.objects.get(hbid=eventkey)
    print >> sys.stderr,'-------111----------',hongbao_data.hbhost.openid

    ntimestamp = time.time()*1000
    if hongbao_data.hbtype == 'temporary':
        if ntimestamp-int(hongbao_data.hbstime)>29.9*60*1000:
            response_txt = '对不起，这个多吉红包已经过期'
            return weixin_helper.get_xml_text(root,response_txt)
    elif hongbao_data.hbtype == 'eternal':
         if ntimestamp-int(hongbao_data.hbstime)>23.99*60*60*1000:
            response_txt = '对不起，这个多吉红包已经过期'
            return weixin_helper.get_xml_text(root,response_txt) 
                  
    user_data = User.objects.get(openid=openid)
    response_txt = ""
    if hongbao_data.hbhost.openid == openid:
        response_txt = 'WOW！自己发的红包还是留给别人抢吧！！'
        return weixin_helper.get_xml_text(root,response_txt)
    if hongbao_data.hbd_hb.filter(hbdused=True).count()==hongbao_data.hbnum:
        response_txt = 'WOW！你来晚了。。这个多吉红包已经被抢光啦！'
        return weixin_helper.get_xml_text(root,response_txt)
    if hongbao_data.hbd_hb.filter(hbdused=True,hbdowneropenid = user_data).count()>0:
        response_txt = 'WOW！你已经拿过这个红包了，让别人也多吉一下吧~'
        return weixin_helper.get_xml_text(root,response_txt)

    hbd_data = hongbao_data.hbd_hb.filter(hbdused=False)[0]
    ret,conn = MyDogecoinConn().move(hongbao_data.hbhost,hongbao_data.hbhost.account,user_data.account,hbd_data.hbdnum,DogeConfig.DOGE_MIN_CONF,"hongbao")
    if ret!=0:
        response_txt = '领红包失败！！！！失败中的失败！！！'
        return weixin_helper.get_xml_text(root,response_txt)

    hbd_data.hbdused = True
    hbd_data.hbdowneropenid = user_data
    hbd_data.hbdusedtime = int(time.time()*1000)
    hbd_data.save()
    hbhost  = hongbao_data.hbhost
    hbhost.lockamount = hbhost.lockamount-hbd_data.hbdnum
    hbhost.save()
    response_txt = '成功领取红包,红包中放了'+str(hbd_data.hbdnum)+'个doge!'
    return weixin_helper.get_xml_text(root,response_txt)

if __name__ == '__main__':
    respond_mininginfo_text()

