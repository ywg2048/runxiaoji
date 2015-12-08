# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
import sys

# Create your models here.

class UserData(models.Model):
    # 유저 아이디 (카톡아이디).
    UserID = models.CharField(max_length=40, blank = True, null = True)
    # 인증 토큰.
    Auth = models.CharField(max_length=40, blank = True, null = True)
    # 최초 플레이 시간.
    FirstPlayTime = models.DateTimeField(blank = True, null = True)
    # 마지막 플레이 시간.
    LastPlayTime = models.DateTimeField(blank = True, null = True)
    # OS타입 (ios, android).
    OSType = models.CharField(max_length = 10, blank = True, null = True)
    # 국가코드.
    ContryCode = models.CharField(max_length=10, blank = True, null = True)

    #임시 필드...
    UserName = models.CharField(max_length = 40, blank = True, null = True)
    PictureURL = models.CharField(max_length = 200, blank = True, null = True)

    def __str__(self):
        return "%d-%s" % (self.id, self.UserName)
            
# 친구데이터.
class FriendData(models.Model):
    #유저SN.
    UserSN = models.IntegerField()
    FriendSN = models.IntegerField()

    def __str__(self):
        return "%d-%d" % (self.UserSN, self.FriendSN)

admin.site.register(UserData)
admin.site.register(FriendData)
