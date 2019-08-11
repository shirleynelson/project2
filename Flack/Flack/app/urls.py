from __future__ import unicode_literals
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("Home", views.index, name="home"),
    path("singlepage0", views.singlepage0, name="singlepage0"),
    path("first", views.first, name="first"),
    path("second", views.second, name="second"),
    path("third", views.third, name="third"),
    path("adddomain", views.adddomain, name="adddomain"),
    path("domainchannels", views.domainchannelindex, name="domainchannelindex"),
    path("usermessages", views.usermessageindex, name="usermessageindex"),
    path("channelusers", views.channeluserindex, name="channeluserindex"),
    path("<int:domain_id>", views.domain, name="domain"),
    path("files/", views.file_list, name="file_list"),
    path("files/upload", views.upload_filev3, name="upload_filev3"),
    path("upload/", views.upload, name="upload"),
    path("<int:domainchannel_id>", views.domainchannel, name="domainchannel"),
    path("<int:channeluser_id>", views.channeluser, name="channeluser"),
    path("<int:usermessage_id>", views.usermessage, name="usermessage"),
    path("<int:domainchannel_id>/addusermessage", views.addusermessage, name="addusermessage"),
    path("<int:domainchannel_id>/addchanneluser", views.addchanneluser, name="addchanneluser"),
    path("<int:domain_id>/adddomainchannel", views.adddomainchannel, name="adddomainchannel"),
    path("<slug:domain_name>/adddomain", views.adddomain, name="adddomain")
               ]