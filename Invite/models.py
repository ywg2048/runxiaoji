# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
# Create your models here.

# 카카오 친구초대 리스트.
class KakaoInviteData(models.Model):
    #유저 SN.
    UserSN = models.IntegerField()
    #유저 아이디.
    UserID = models.CharField(max_length = 40)
    #초대한날짜.
    InviteDate = models.DateTimeField()


admin.site.register(KakaoInviteData)