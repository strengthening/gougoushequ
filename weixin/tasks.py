# -*- coding:utf-8 -*-
from gougoushequ.celery import app
from weixin.models import Hbdetail,User
from django.db.models import Sum
from weixin import weixin_account_helper
 
@app.task
def hello_world1(hbuuid,openid):
    hbbal = Hbdetail.objects.filter(hbduuid=hbuuid,hbdused=False).aggregate(Sum('hbdnum'))['hbdnum__sum']
    if hbbal is None:
        print  'hongbao get emptyed--',hbbal
        return
    print  'hongbao get leaved--',hbbal
    user_data = User.objects.get(openid=openid)
    hongbao_data = Hongbao.objects.get(hbuuid=hbuuid)
    if hongbao_data.isturnbacked:
        print 'error hongbao had turnbacked'
        return
    if (user_data.lockamount-hbbal) < 0:
        print 'hongbao turnback error--',hbuuid,'--',openid
        return
    user_data.lockamount = user_data.lockamount-hbbal
    user_data.save()
    hongbao_data.isturnbacked = True
    hongbao_data.save()
    
@app.task
def classify_account(openid,event):
    print '录入用户信息'
    weixin_account_helper.classify_account(openid,event)



@app.task
def gen_account_info(user_data):
    weixin_account_helper.generateImg(user_data.address,'dogecoin:')
    weixin_account_helper.updateUserdetail(user_data)

