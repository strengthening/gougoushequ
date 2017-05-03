from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gougoushequ.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','gougoushequ.views.index',name='index'),
    url(r'^introduction/$','gougoushequ.views.introduction',name='introduction'),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^weixin/', include('weixin.urls')),
    url(r'^testapp/', include('testapp.urls')),

)
urlpatterns += staticfiles_urlpatterns()
