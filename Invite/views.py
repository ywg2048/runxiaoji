# -*- coding: utf-8 -*-
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from Invite.models import *
from users.models import UserData
from datetime import *
import myUtil


# 카카오 친구초대 등록.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
UserID = 초대받은유저 ID

리턴값
Count = 초대한횟수.
"""
@csrf_exempt
def InsertKakaoInviteResponse(request):
    # 호출인자 검사.
    if request.method == 'GET':
        data = {
            'ErrorCode' : '99',
            'Message' : 'error',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    if not request.POST.get('SN'):
        data = {
            'ErrorCode' : '101',
            'Message' : 'SN does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('Auth'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'Auth does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('UserID'):
        data = {
            'ErrorCode' : '105',
            'Message' : 'UserID does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    user = list(UserData.objects.filter(id = request.POST.get('SN')))
    if len(user) == 0:
        data = {
            'ErrorCode' : '103',
            'Message' : 'UserData does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    user = user[0]
    if user.Auth != request.POST.get('Auth'):
        data = {
            'ErrorCode' : '104',
            'Message' : 'Auth is invalid.',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    # 결과 처리.

    userData = list(KakaoInviteData.objects.filter(UserSN = request.POST.get('SN'), UserID = request.POST.get('UserID') ))
    if len(userData) > 0:
        data = {
            'ErrorCode' : '106',
            'Message' : 'UserID is exist.',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    inviteData = KakaoInviteData(UserSN = request.POST.get('SN'), UserID = request.POST)
    inviteData.InviteDate = datetime.today()
    inviteData.save()

    SendData = {}
    SendData['Count'] = KakaoInviteData.objects.filter(UserSN = request.POST.get('SN')).count()

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')

#-------------------------------------------------------------------------------


# 카카오 초대한친구리스트 가져오기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
Count = 초대한횟수.
UserID = 초대받은유저ID 배열.
"""
@csrf_exempt
def KakaoInviteListResponse(request):
    # 호출인자 검사.
    if request.method == 'GET':
        data = {
            'ErrorCode' : '99',
            'Message' : 'error',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    if not request.POST.get('SN'):
        data = {
            'ErrorCode' : '101',
            'Message' : 'SN does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('Auth'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'Auth does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    user = list(UserData.objects.filter(id = request.POST.get('SN')))
    if len(user) == 0:
        data = {
            'ErrorCode' : '103',
            'Message' : 'UserData does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    user = user[0]
    if user.Auth != request.POST.get('Auth'):
        data = {
            'ErrorCode' : '104',
            'Message' : 'Auth is invalid.',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    # 결과 처리.

    SendData = {}
    SendData['Count'] = KakaoInviteData.objects.filter(UserSN = request.POST.get('SN')).count()
    inviteDataList = list(KakaoInviteData.objects.filter(UserSN = request.POST.get('SN')))
    if len(inviteDataList) > 0:
        data = []
        for inviteData in inviteDataList:
            data.append(inviteData.UserID)

        SendData['UserID'] = data

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
