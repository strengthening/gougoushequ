from django.conf.urls import patterns, url

from weixin import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^account$', views.account, name='account'),
    url(r'^sraccount$', views.sraccount, name='sraccount'),
    url(r'^senddoge$',views.senddoge,name='senddoge'),
    url(r'^hongbao$',views.hongbao, name='hongbao'),
    url(r'^hongbao/(?P<enhbid>\S+)$',views.hongbaodesc, name='hongbaodesc'),
    url(r'^confhb/(?P<entext>\S+)/$',views.confhb, name='confhb'),
    url(r'^hbreceivelist/(?P<entext>\S+)/$',views.hbreceivelist, name='hbreceivelist'),
    url(r'^hbsendlist/(?P<entext>\S+)/$',views.hbsendlist, name='hbsendlist'),
    url(r'^hbrichlist/(?P<entext>\S+)/$',views.hbrichlist, name='hbrichlist'),
    url(r'^sendhb$',views.sendhb,name='sendhb'),
    url(r'^gethb/(?P<enhbid>\S+)/$',views.gethb,name='gethb'),
    url(r'^test/$',views.test,name='test'),
    # url(r'^price/(?P<site_name>\S+)$', views.price_type, name='price_type'),

    # url(r'^(?P<univer_abb>[a-z]+)/(?P<pageno>[0-9]+)/$', views.detail_pageno, name='detail_pageno'),
)

