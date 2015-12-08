# -*- coding: utf-8 -*-
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from ServerInfo.models import *
import myUtil

# 서버체크.
"""
호출 값
OSType = ostype

리턴값.
# 서버 상태 (true : 정상, false : 점검)
IsServerRun = models.BooleanField()
# 최소 접속 가능 앱버전.
MinVersion = models.IntegerField()
# 최신 앱버전.
LastVersion = models.IntegerField()
# 문자열로된 버전..
MinVersionStr = 최소..
LastVersionStr = 마지막.
"""
@csrf_exempt
def ServerCheck(request):
    # 호출인자 검사.
    if request.method == 'GET':
        data = {
            'ErrorCode' : '99',
            'Message' : 'error',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    if not request.POST.get('OSType'):
        data = {
            'ErrorCode' : '101',
            'Message' : 'OSType does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    # 결과 처리.

    stateList = list(ServerState.objects.filter(OSType = request.POST.get('OSType')))
    if len(stateList) > 0:
        state = stateList[0]
        data = {
            'IsServerRun' : state.IsServerRun,
            'MinVersion' : state.MinVersion,
            'LastVersion' : state.LastVersion,
            'MinVersionStr' : state.MinVersionStr,
            'LastVersionStr' : state.LastVersionStr,
        }

        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')
    else:
        data = {
            'ErrorCode' : '99',
            'Message' : 'error',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


# 공지 호출.
"""
호출 값
Version = 공지를 받을 최소 버전.

리턴값
Count = 공지갯수.
Notice
 - [0 : 공지내용]... = 공지
"""
@csrf_exempt
def NoticeResponse(request):
    # 호출인자 검사.
    if request.method == 'GET':
        data = {
            'ErrorCode' : '99',
            'Message' : 'error',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    if not request.POST.get('Version'):
        data = {
            'ErrorCode' : '101',
            'Message' : 'Version does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    # 결과 처리.
    noticeList = list(NoticeData.objects.filter(MinVersion__gte = request.POST.get('Version')))
    cnt = 0
    data = {}
    for notice in noticeList:
        data[str(cnt)] = notice.Message
        cnt = cnt + 1
    SendData = {
        'Count' : cnt,
    }
    if cnt > 0:
            SendData['Notice'] = data
    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


# 이벤트 호출.
"""
호출 값
Version = 공지를 받을 최소 버전.

리턴값
Count = 공지갯수.
URL
 - [0 : 공지내용]... = 공지
"""
@csrf_exempt
def EventURLResponse(request):
    # 호출인자 검사.
    if request.method == 'GET':
        data = {
            'ErrorCode' : '99',
            'Message' : 'error',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    if not request.POST.get('Version'):
        data = {
            'ErrorCode' : '101',
            'Message' : 'Version does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    # 결과 처리.
    noticeList = list(EventData.objects.filter(MinVersion__gte = request.POST.get('Version')))
    cnt = 0
    data = {}
    for notice in noticeList:
        data[str(cnt)] = notice.URL
        cnt = cnt + 1
    SendData = {
        'Count' : cnt,
    }
    if cnt > 0:
            SendData['URL'] = data
    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
