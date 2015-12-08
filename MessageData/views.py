# -*- coding: utf-8 -*-
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from MessageData.models import *
from users.models import UserData
from GameData.models import *
from ShopData.models import Shop_CashData
from datetime import datetime, timedelta
import myUtil



# 토큰메세지 가져오기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
Count = 메세지 갯수.
-SN = 메세지SN
-SendUserSN= 보낸 유저SN

"""
@csrf_exempt
def TokenMessageResponse(request):
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
    dataList = list(TokenMessage.objects.filter(UserSN = request.POST.get('SN')))
    dataList.reverse()

    ItemList = []
    removedata = []

    for msg in dataList:
        if myUtil.NowTime() > msg.RemoveTime:
            removedata.append(msg)
        else:
            # 상위 50개만 보내주고 나머진 제거;
            if len(ItemList) < 50:
                data = {}
                data['SN'] = msg.id
                data['SendUserSN'] = msg.SendUserSN
                ItemList.append(data);
            else:
                removedata.append(msg)

    # 날짜가 지난메세지 제거.
    for msg in removedata:
        msg.delete()

    SendData = {'Count' : len(ItemList)}
    if len(ItemList) > 0:
        SendData['Data'] = ItemList


    return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

#-------------------------------------------------------------------------------

# 캐쉬선물 메세지 가져오기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
Count = 메세지 갯수.
Data
    -SN = 메세지 SN
    -SendUserSN= 보낸 유저SN

"""
@csrf_exempt
def GiftMessageResponse(request):
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
    dataList = list(GiftMessage.objects.filter(UserSN = request.POST.get('SN')))

    ItemList = []
    for msg in dataList:
        data = {}
        data['SN'] = msg.id
        data['SendUserSN'] = msg.SendUserSN
        ItemList.append(data);

    SendData = {'Count' : len(ItemList)}
    if len(ItemList) > 0:
        SendData['Data'] = ItemList

    return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


#-------------------------------------------------------------------------------

# 받은 선물 가져오기 (캐쉬, 토큰).
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
Count = 메세지 갯수.
Data
    -SN = 메세지 SN
    -Type = (1 : 토큰, 2 : 캐쉬).
    -SendUserSN= 보낸 유저SN
    -Value = 수량.
    -UserName = 유저 이름.
    -UserPicture = 유저사진URL

"""
@csrf_exempt
def GiftAllMsgResponse(request):
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
    dataList = list(GiftMessage.objects.filter(UserSN = request.POST.get('SN')))

    ItemList = []
    for msg in dataList:
        data = {}
        data['SN'] = msg.id
        data['Type'] = 2
        data['SendUserSN'] = msg.SendUserSN
        data['Value'] = msg.CashValue
        userData = list(UserData.objects.filter(UserSN = msg.SendUserSN))
        if len(userData) > 0:
            userData = userData[0]
            data['UserName'] = userData.UserName
            data['UserPicture'] = userData.PictureURL

        ItemList.append(data);

    dataList = list(TokenMessage.objects.filter(UserSN = request.POST.get('SN')))
    dataList.reverse()

    cnt = 0
    removedata = []
    for msg in dataList:
        if myUtil.NowTime() > msg.RemoveTime:
            removedata.append(msg)
        else:
            # 상위 50개만 보내주고 나머진 제거;
            if cnt < 50:
                data = {}
                data['SN'] = msg.id
                data['Type'] = 1
                data['SendUserSN'] = msg.SendUserSN
                data['Value'] = 1
                userData = list(UserData.objects.filter(id = msg.SendUserSN))
                if len(userData) > 0:
                    userData = userData[0]
                    data['UserName'] = userData.UserName
                    data['UserPicture'] = userData.PictureURL
                ItemList.append(data);
            else:
                removedata.append(msg)

            cnt = cnt + 1

    # 날짜가 지난메세지 제거.
    for msg in removedata:
        msg.delete()

    SendData = {'Count' : len(ItemList)}
    if len(ItemList) > 0:
        SendData['Data'] = ItemList

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 선물 갯수..가져오기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
Count = 메세지 갯수.

"""
@csrf_exempt
def GiftAllMsgCount(request):
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
    dataList = list(GiftMessage.objects.filter(UserSN = request.POST.get('SN')))

    SendData['Count'] = len(dataList)

    dataList = list(TokenMessage.objects.filter(UserSN = request.POST.get('SN')))
    dataList.reverse()

    cnt = 0
    removedata = []
    for msg in dataList:
        if myUtil.NowTime() > msg.RemoveTime:
            removedata.append(msg)
        else:
            # 상위 50개만 보내주고 나머진 제거;
            if cnt < 50:
                SendData['Count'] = SendData['Count'] + 1
            else:
                removedata.append(msg)

            cnt = cnt + 1

    # 날짜가 지난메세지 제거.
    for msg in removedata:
        msg.delete()

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')

#-------------------------------------------------------------------------------

# 토큰 보내기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
TargetSN = 받을 유저SN.

리턴값
TargetSN = 받을 유저SN
Value = 수량.
ReceiveTime = 다음 토큰 수신받을수있는 남은 초.
-ChickenScore = 치킨점수.
"""
@csrf_exempt
def SendTokenMessageResponse(request):
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
    tokenmsg = TokenMessage()
    tokenmsg.UserSN = request.POST.get('TargetSN')
    tokenmsg.SendUserSN = request.POST.get('SN')
    tokenmsg.RemoveTime = datetime.now() + timedelta(days=3)
    tokenmsg.save()

    chickenScoreData = list(ChickenScoreRewardData.objects.filter(UserSN = request.POST.get('SN')))[0]
    chickenScoreData.Score = chickenScoreData.Score + 3
    chickenScoreData.save()

    SendData = { 'ChickenScore' : chickenScoreData.Score }
    SendData = { 'TargetSN' : request.POST.get('TargetSN'), 'Value' : 1}

    ReceiveList= list(TokenReceiveData.objects.filter(UserSN = request.POST.get('TargetSN'), SendUserSN = request.POST.get('SN')))
    if len(ReceiveList) > 0:
        receiveData = ReceiveList[0]
        receiveData.ReceiveTime = datetime.today() + timedelta(days = 1) # 24시간.
        SendData['ReceiveTime'] = myUtil.TimedeltaToSeconds(receiveData.ReceiveTime - datetime.now())
        receiveData.save()
    else:
        # 데이터가 존재하지 않으면 새로 생성.
        receiveData = TokenReceiveData()
        receiveData.UserSN = request.POST.get('TargetSN')
        receiveData.SendUserSN = request.POST.get('SN')
        receiveData.IsReceive = True
        receiveData.ReceiveTime = datetime.today() + timedelta(days = 1) # 24시간.
        SendData['ReceiveTime'] = myUtil.TimedeltaToSeconds(receiveData.ReceiveTime - datetime.now())
        receiveData.save()


    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 캐쉬선물 보내기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
TargetSN = 받을 유저SN.
CashSN = 캐쉬SN
리턴값
TargetSN = 받을 유저SN.
Value = 수량.

"""
@csrf_exempt
def SendGiftMessageResponse(request):
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
    cashData = list(Shop_CashData.objects.filter(CashSN = request.POST.get('CashSN')))
    if len(cashData) > 0:
        cashData = cashData[0]
        gift = GiftMessage()
        gift.UserSN = request.POST.get('TargetSN')
        gift.SendUserSN = request.POST.get('SN')
        gift.RemoveTime = datetime.now() + timedelta(days=365)
        gift.CashValue = cashData.Value
        gift.save()

    SendData = {
            'TargetSN' : request.POST.get('TargetSN'),
            'Value' : cashData.Value,
        }
    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')

#-------------------------------------------------------------------------------

# 토큰 받는 상태 변경.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
IsReceive = 상태값 리턴.
"""
@csrf_exempt
def TokenIsReceiveResponse(request):
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
    ReceiveList= list(TokenReceiveData.objects.filter(UserSN = request.POST.get('SN')))
    if len(ReceiveList) > 0:
        for receiveData in ReceiveList:
            receiveData.IsReceive = not receiveData.IsReceive
            receiveData.save()

        SendData['IsReceive'] = receiveData.IsReceive
    else:
        # 데이터가 존재하지 않으면 새로 생성.
        receiveData = TokenReceiveData()
        receiveData.UserSN = request.POST.get('SN')
        receiveData.SendUserSN = request.POST.get('SN')
        receiveData.IsReceive = False
        receiveData.ReceiveTime = datetime.today()
        receiveData.save()
        SendData['IsReceive'] = receiveData.IsReceive

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 선물 받기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
GiftSN = 선물sn.
Type = (1 : 토큰, 2 : 캐쉬).

리턴값
GiftSN = 받은 선물 SN.
Type = (1 : 토큰, 2 : 캐쉬).
Value = 수량.
"""
@csrf_exempt
def GetGiftItem(request):
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

    elif not request.POST.get('GiftSN'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'GiftSN does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('Type'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'Type does not exist',
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
    if int(request.POST.get('Type')) == 1:
        tokenList = list(TokenMessage.objects.filter(id = request.POST.get('GiftSN')))
        if len(tokenList) > 0:
            SendData['GiftSN'] = tokenList[0].id
            SendData['Type'] = 1
            SendData['Value'] = 1
            tokenList[0].delete()
            token = TokenData.objects.filter(UserSN = request.POST.get('SN'))[0]
            token.ToeknValue = token.ToeknValue + 1
            token.save()
        else:
            SendData['ErrorCode'] = '105'
            SendData['Message'] = 'Data dose not exist'

    elif int(request.POST.get('Type')) == 2:
        giftList = list(GiftMessage.objects.filter(id = request.POST.get('GiftSN')))
        if len(giftList) > 0:
            value = giftList[0].CashValue
            SendData['GiftSN'] = giftList[0].id
            SendData['Type'] = 2
            SendData['Value'] = value
            giftList[0].delete()
            money = MoneyData.objects.filter(UserSN = request.POST.get('SN'))
            money.CashValue = money.CashValue + value
            money.save()
        else:
            SendData['ErrorCode'] = '105'
            SendData['Message'] = 'Data dose not exist'

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 모든선물 받기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
Type = (1 : 토큰, 2 : 캐쉬).

리턴값
Type = (1 : 토큰, 2 : 캐쉬).
Value = 수량.
"""
@csrf_exempt
def GetAllGiftItem(request):
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

    elif not request.POST.get('Type'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'Type does not exist',
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
    if int(request.POST.get('Type')) == 1:
        tokenList = list(TokenMessage.objects.filter(UserSN = request.POST.get('SN')))
        tokenList.reverse()
        tokenValue = 0
        if len(tokenList) > 0:
            cnt = 0
            for data in tokenList:
                if myUtil.NowTime() < data.RemoveTime and cnt < 50:
                    tokenValue = tokenValue + 1
                cnt = cnt + 1

            for data in tokenList:
                data.delete()

            SendData['Type'] = 1
            SendData['Value'] = tokenValue
            token = TokenData.objects.filter(UserSN = request.POST.get('SN'))[0]
            token.ToeknValue = token.ToeknValue + tokenValue
            token.save()
        else:
            SendData['ErrorCode'] = '105'
            SendData['Message'] = 'Data dose not exist'

    elif int(request.POST.get('Type')) == 2:
        giftList = list(GiftMessage.objects.filter(UserSN = request.POST.get('SN')))
        Value = 0
        if len(giftList) > 0:
            for data in giftList:
                Value = Value + data.CashValue
                data.delete()

            SendData['Type'] = 2
            SendData['Value'] = Value
            money = MoneyData.objects.filter(UserSN = request.POST.get('SN'))
            money.CashValue = money.CashValue + Value
            money.save()
        else:
            SendData['ErrorCode'] = '105'
            SendData['Message'] = 'Data dose not exist'

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
