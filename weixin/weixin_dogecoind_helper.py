# -*- coding:utf-8 -*-
#import os,sys
#sys.path.append('..')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gougoushequ.settings")


#--------------------------------------------------------------------
from decimal import *
from gougoushequ import settings
import dogecoinrpc
from dogecoinrpc.exceptions import *
import uuid,time, decimal
from weixin.models import Sendlist,User

class Singleton(object):
    _state = {}
    def __new__(cls,*args,**kw):
        ob = super(Singleton,cls).__new__(cls,*args,**kw)
        ob.__dict__ = cls._state
        return ob

class MyDogecoinConn(Singleton):
    conn = None
    def __init__(self):
        if self.conn==None:
            try:
                self.conn = dogecoinrpc.connect_to_remote(settings.DOGECOIND['rpc_username'], settings.DOGECOIND['rpc_password'], host=settings.DOGECOIND['rpc_ip'], port=22555)
            except Exception, e:
                traceback.print_exc()     
    def getConn(self):
        ret = DogeError.DOGE_ERR_DISCONN
        if self.conn !=None:
            ret = 0
        return ret,self.conn

    def move(self,user,fromaccount, toaccount, amount, minconf, comment):
        amount = Decimal(amount).quantize(Decimal('.00000001'), rounding=ROUND_DOWN)
        #print float(amount)
        if user.account!= fromaccount:
            return DogeError.DOGE_ERR_USERFACCOUNT,None
        if User.objects.filter(account=toaccount).count()!=1:
            return DogeError.DOGE_ERR_USERTACCOUNT,None
        ret,rst = self.getbalance(fromaccount,DogeConfig.DOGE_MIN_CONF)
        if ret!=0:
            return ret,rst
        if rst < amount:
            return DogeError.DOGE_ERR_LACK,None
 
        if self.conn.move(fromaccount, toaccount,float(amount), minconf, comment):
            sl_data = Sendlist(
                openid = user,
                account = fromaccount,
                sluuid = uuid.uuid4(),
                category = "move",
                amount = amount,
                fee = 0,
                toaccount = toaccount,
                sendtime = time.time()*1000,
            )
            sl_data.save()
            return 0,"success"
        else:
            return DogeError.DOGE_ERR_UNKNOWN,"unknown error maybe something err in dogenet"
        #return self.conn
    def sendfrom(self,user,fromaccount, toaddress, amount, minconf, comment, comment_to):
        amount = Decimal(amount).quantize(Decimal('.00000001'), rounding=ROUND_DOWN)
        if user.account!= fromaccount:
            return DogeError.DOGE_ERR_USERFACCOUNT,"账户不匹配"

        ret,rst = self.getbalance(fromaccount,DogeConfig.DOGE_MIN_CONF)
        if ret!=0:
            return ret,rst

        if rst < (amount+DogeConfig.DOGE_NET_FEE+user.lockamount):
            return DogeError.DOGE_ERR_LACK,"提币失败，您的账户余额不足"

        try:
            vobj = self.conn.validateaddress(toaddress)
            if vobj.isvalid and vobj.ismine:
                if vobj.account==fromaccount:
                    return DogeError.DOGE_ERR_FTACCOUNTSAME,"提币失败，不能往自己的账户中提币，调皮！"
                ret,rst = self.move(user,fromaccount,vobj.account,amount,minconf,comment)
                return ret,rst
            elif vobj.isvalid and not vobj.ismine:
                txid = self.conn.sendfrom(fromaccount, toaddress,float(amount), minconf, comment)
                sl_data = Sendlist(
                    openid = user,
                    account = fromaccount,
                    sluuid = uuid.uuid4(),
                    category = "send",
                    amount = amount,
                    fee = DogeConfig.DOGE_NET_FEE,
                    txid = txid,
                    toaddress = toaddress,
                    sendtime = time.time()*1000,
                )
                sl_data.save()
                return 0,"提币成功"
            else:
                return DogeError.DOGE_ERR_WRONGADDR,"错误的dogecoin地址"
        except InvalidAddressOrKey:
            return DogeError.DOGE_ERR_WRONGADDR,None

    def getbalance(self,account, minconf):
        if self.conn!=None:
            bal = self.conn.getbalance(account, minconf)
            if bal < 0:
                return DogeError.DOGE_ERR_BAL,bal

            return 0,self.conn.getbalance(account, minconf)
        else:
            return DogeError.DOGE_ERR_DISCONN,None

    def getrawtransaction(self,txid,verbose):
        return self.conn
    def getreceivedbyaccount(self,account,minconf):
        return self.conn
    def getreceivedbyaddress(self,dogecoinaddress,minconf):
        return self.conn
    def validateaddress():
        return self.conn
    

def add_quotes(str):
    return "'"+str+"'"

class DogeError():
    DOGE_ERR_DISCONN =                   40001
    DOGE_ERR_BAL =                       40002
    DOGE_ERR_LACK =                      40003
    DOGE_ERR_UNKNOWN =                   40004
    DOGE_ERR_USERFACCOUNT =              40005
    DOGE_ERR_USERTACCOUNT =              40006
    DOGE_ERR_WRONGADDR =                 40007
    DOGE_ERR_FTACCOUNTSAME =             40008

class DogeConfig():
    DOGE_MIN_CONF = 8
    DOGE_NET_FEE = 1

if __name__ == '__main__':
    mydogeconn = MyDogecoinConn()
    user_data = User.objects.get(openid='o3-17uPBsYXkC75ex3FWHZHfvQs4')
    #print mydogeconn.move(user_data,"test_o3-17uPBsYXkC75ex3FWHZHfvQs4","test_o3-17uBfR2HBCkIPsQ1iYvv6l_ag",1.000000019312312312132,8,"tttt_esssss")
    print mydogeconn.sendfrom(user_data,"test_o3-17uPBsYXkC75ex3FWHZHfvQs4", "DFsD4ydm5CvWdHuxmtvd8ekKde8P16c6Bx", 2, 8, "from", "to")
    #print mydogeconn.getbalance("test_o3-17uBfR2HBCkIPsQ1iYvv6l_ag",8)
    #mydogeconn1 = MyDogecoinConn()
    #print id(mydogeconn.getConn())
    #print id(mydogeconn1.getConn())

