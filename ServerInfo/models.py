# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.

# 서버 상태.
class ServerState(models.Model):
    # OS타입.
    OSType = models.CharField(max_length = 10)
    # 서버 상태 (true : 정상, false : 점검)
    IsServerRun = models.BooleanField(default=False)
    # 최소 접속 가능 앱버전.
    MinVersion = models.IntegerField()
    # 최신 앱버전.
    LastVersion = models.IntegerField()
    # 문자열버전..
    MinVersionStr = models.CharField(max_length = 10)
    LastVersionStr = models.CharField(max_length = 10)


# 공지 데이터.
class NoticeData(models.Model):
    # 메세지.
    Message = models.CharField(max_length=200)
    # 보여질 최소 버전.
    MinVersion = models.IntegerField()

class EventData(models.Model):
    #URL 주소.
    URL = models.CharField(max_length=200)
    # 보여질 최소 버전.
    MinVersion = models.IntegerField()

admin.site.register(ServerState)
admin.site.register(NoticeData)
admin.site.register(EventData)
