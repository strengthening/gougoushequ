# -*- coding:utf-8 -*-

import os,sys
sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gougoushequ.settings")

##########################################################

import base64
from WXBizMsgCrypt import Prpcrypt,MyCrypt
from gougoushequ import settings

if __name__ =='__main__':
    #try:
    #    key = base64.b64decode("WgcW5hFF61wJCkUXmCDiSsdx7e8eA47mhlVSSr7HWr0"+"=")
    #    assert len(key) == 32
    #except:
    #    throw_exception("[error]: EncodingAESKey unvalid !", FormatException)
        #return weixin_error.WXBizMsgCrypt_IllegalAesKey)

    #print key
    #pc = Prpcrypt(key)
    #ret,encrypt = pc.encrypt("12345678900987654321","dogecoinchina")
    #print ret,encrypt
    #ret,dec = pc.decrypt(encrypt,"dogecoinchina")    
    #print ret,dec
    
    mc = MyCrypt("WgcW5hFF61wJCkUXmCDiSsdx7e8eA47mhlVSSr7HWr0","dogecoinchina")
    print mc.EncryptMsg("12312312eweqwe")
    ret,enText = mc.EncryptMsg("12312312ew")
    
    print mc.DecryptMsg(enText)

    #print DecryptMsg 
