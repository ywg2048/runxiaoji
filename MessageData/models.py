# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.


# 토큰 받은 메세지.
class TokenMessage(models.Model):
    # 유저 SN.
    UserSN = models.IntegerField()
    # 보낸사람 SN.
    SendUserSN = models.IntegerField()
    # 삭제할시간.
    RemoveTime = models.DateTimeField()


# 캐쉬 선물 메세지.
class GiftMessage(models.Model):
    #유저 SN.
    UserSN = models.IntegerField()
    # 보낸사람 SN.
    SendUserSN = models.IntegerField()
    # 삭제할시간.
    RemoveTime = models.DateTimeField()
    # 수량.
    CashValue = models.IntegerField()

# 토큰수신상태 데이터.
class TokenReceiveData(models.Model):
    #유저SN.
    UserSN = models.IntegerField()
    #보낸사람 SN.
    SendUserSN = models.IntegerField()
    #수신가능여부.
    IsReceive = models.BooleanField(default=False)
    #수신가능시간.
    ReceiveTime = models.DateTimeField()


admin.site.register(TokenMessage)
admin.site.register(GiftMessage)
admin.site.register(TokenReceiveData)
