from django.db import models
import datetime,time

# Create your models here.

class Token_data(models.Model):
    token = models.CharField(max_length=1024)
    jsticket = models.CharField(max_length=1024)
    time = models.DateTimeField(auto_now=False, auto_now_add=True,default=datetime.datetime.now())
    def has_valid_token(self):
        rst = False
        if self.time >(datetime.datetime.now()+datetime.timedelta(seconds=-7000)):
            rst = True
        return rst

class User(models.Model):
    openid = models.CharField(unique=True,max_length=255)
    account = models.CharField(unique=True,max_length=255)
    unionid  = models.CharField(max_length=255)
    nickname =  models.CharField(max_length=255)
    address = models.CharField(unique=True,max_length=255)
    signmessage = models.CharField(max_length=255)
    lockamount = models.DecimalField(max_digits=40, decimal_places=8)
    createdtimestamp = models.BigIntegerField()
    subscribetimestamp = models.BigIntegerField()
    subscribe = models.BooleanField(default=False)
    istest = models.BooleanField()

class User_Token_data(models.Model):
    openid = models.ForeignKey(User,related_name='utd_user',to_field='openid')
    access_token = models.CharField(max_length=1024)
    refresh_token = models.CharField(max_length=1024)
    scope = models.CharField(max_length=1024)
    expirstime = models.BigIntegerField()
    updatetime = models.BigIntegerField()
    def has_expired(self):
        rst = False
        if self.expirstime < int(time.time()*1000):
            rst = True
        return rst

class Userdetail(models.Model):
    openid = models.ForeignKey(User,related_name='ud_user',to_field='openid')
    sex = models.IntegerField()
    language = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    headimgurl = models.CharField(max_length=2048)
    updatetime = models.BigIntegerField()
    

class Sendlist(models.Model):
    openid = models.ForeignKey(User,related_name='sl_user',to_field='openid')
    account = models.CharField(max_length=255)
    sluuid = models.CharField(unique=True,max_length=128)
    category = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=40, decimal_places=8)
    fee = models.DecimalField(max_digits=40, decimal_places=8)
    txid =  models.CharField(max_length=512)
    toaddress = models.CharField(max_length=255)
    toaccount =  models.CharField(max_length=255)
    sendtime = models.BigIntegerField()
    

class Hongbao(models.Model):
    hbuuid = models.CharField(unique=True,max_length=128)
    hbtype = models.CharField(max_length=12)
    hbid = models.IntegerField(unique=True)
    hbnum = models.IntegerField(max_length=8)
    hbrandomtype = models.IntegerField(max_length=2)
    hbsum = models.DecimalField(max_digits=40, decimal_places=8)
    hbgreetings = models.CharField(max_length=280)
    hbhost = models.ForeignKey(User,related_name='hb_user',to_field='openid')
    hbstime = models.BigIntegerField()
    hbutime = models.BigIntegerField()
    hbqrcodeurl = models.CharField(max_length=2048,default='wait')
    enhbid =  models.CharField(max_length=2048)
    qrcodeutime = models.BigIntegerField()
    isturnbacked = models.BooleanField(default=False)


class Hbdetail(models.Model):
    hbduuid = models.ForeignKey(Hongbao,related_name='hbd_hb',to_field='hbuuid')
    hbdseq = models.IntegerField(max_length=4)
    hbdnum = models.DecimalField(max_digits=40, decimal_places=8)
    hbdused = models.BooleanField(default=True)
    hbdowneropenid = models.ForeignKey(User,related_name='hbd_user',to_field='openid',blank = True,null=True)
    hbdgreetings = models.CharField(max_length=280)
    hbdusedtime = models.BigIntegerField(blank=True,null=True)
    
    
