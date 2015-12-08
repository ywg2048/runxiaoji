# -*- coding: utf-8 -*-
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from Ranking.models import *
from ShopData.models import *
from users.models import UserData
from users.models import FriendData
from GameData.models import MoneyData
from GameData.models import ItemData
from MessageData.models import TokenReceiveData
from datetime import datetime, timedelta
from django.db.models import Q
import myUtil

# 排名初始化检查.
"""
호출 값
"""
@csrf_exempt
def InitRankCheck(request):
    return HttpResponse('', content_type='application/json')
    # 处理结果

    # 朋友每周排名.
    rankdata = list(RankInfoData.objects.filter(FriendInitTime__lt = datetime.today())[0:1])
    if len(rankdata) > 0:
        rankdata = rankdata[0]
        # # 无穷远模式.
        # InfiniteWeekList = list(InfiniteFriendWeekRankData.objects.order_by('-Score'))
        # InfiniteFriendLastWeekRankData.objects.all().delete()
        # cnt = 1
        # for data in InfiniteWeekList:
        #     rank = InfiniteFriendLastWeekRankData()
        #     rank.UserSN = data.UserSN
        #     rank.Score = data.Score
        #     rank.Confirm = False
        #     rank.save()

        #     cnt = cnt + 1

        # InfiniteFriendWeekRankData.objects.all().update(Score = 0)

        # # 타임어택.
        # TimeAttackWeekList = list(TimeAttackFriendWeekRankData.objects.order_by('-Score'))
        # TimeAttackFriendLastWeekRankData.objects.all().delete()
        # cnt = 1
        # for data in TimeAttackWeekList:
        #     rank = TimeAttackFriendLastWeekRankData()
        #     rank.UserSN = data.UserSN
        #     rank.Score = data.Score
        #     rank.Confirm = False
        #     rank.save()

        #     cnt = cnt + 1

        # TimeAttackFriendWeekRankData.objects.all().update(Score = 0)

        rankdata.FriendInitTime = rankdata.FriendInitTime + timedelta(days=7)
        rankdata.save()

    # 주간랭킹.
    rankdata = list(RankInfoData.objects.filter(WeekInitTime__lt = datetime.today())[0:1])
    if len(rankdata) > 0:
        rankdata = rankdata[0]
        # 무한모드.
        InfiniteWeekList = list(InfiniteWeekRankData.objects.order_by('-Score'))
        InfiniteLastWeekRankData.objects.all().delete()
        cnt = 1
        for data in InfiniteWeekList:
            rank = InfiniteLastWeekRankData()
            rank.UserSN = data.UserSN
            rank.Score = data.Score
            rank.Confirm = False
            rank.save()

            cnt = cnt + 1

        InfiniteWeekRankData.objects.all().update(Score = 0)

        # 타임어택.
        TimeAttackWeekList = list(TimeAttackWeekRankData.objects.order_by('-Score'))
        TimeAttackLastWeekRankData.objects.all().delete()
        cnt = 1
        for data in TimeAttackWeekList:
            rank = TimeAttackLastWeekRankData()
            rank.UserSN = data.UserSN
            rank.Score = data.Score
            rank.Confirm = False
            rank.save()

            cnt = cnt + 1

        TimeAttackWeekRankData.objects.all().update(Score = 0)

        rankdata.WeekInitTime = rankdata.WeekInitTime + timedelta(days=7)
        rankdata.save()

    # 월간랭킹.
    rankdata = list(RankInfoData.objects.filter(MonthInitTime__lt = datetime.today())[0:1])
    if len(rankdata) > 0:
        rankdata = rankdata[0]
        # 무한모드.
        InfiniteMonthList = list(InfiniteMonthRankData.objects.order_by('-Score'))
        InfiniteLastMonthRankData.objects.all().delete()
        cnt = 1
        for data in InfiniteMonthList:
            rank = InfiniteLastMonthRankData()
            rank.UserSN = data.UserSN
            rank.Score = data.Score
            rank.Confirm = False
            rank.save()

            cnt = cnt + 1

        InfiniteMonthRankData.objects.all().update(Score = 0)

        # 타임어택.
        TimeAttackMonthList = list(TimeAttackMonthRankData.objects.order_by('-Score'))
        TimeAttackLastMonthRankData.objects.all().delete()
        cnt = 1
        for data in TimeAttackMonthList:
            rank = TimeAttackLastMonthRankData()
            rank.UserSN = data.UserSN
            rank.Score = data.Score
            rank.Confirm = False
            rank.save()

            cnt = cnt + 1

        TimeAttackMonthRankData.objects.all().update(Score = 0)

        year = rankdata.MonthInitTime.year
        month = rankdata.MonthInitTime.month
        if rankdata.MonthInitTime.month == 12:
            year = year + 1
            month = 1
        else:
            month = month + 1

        rankdata.MonthInitTime = datetime(year, month, 1, rankdata.MonthInitTime.hour, rankdata.MonthInitTime.minute, rankdata.MonthInitTime.second)
        rankdata.save()

    return HttpResponse('', content_type='application/json')

#

#-------------------------------------------------------------------------------

# 전적정보 가져오기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
# 무한모드 랭킹 1등 횟수.
InfiniteModeRank_1
# 무한모드 랭킹 2등 횟수.
InfiniteModeRank_2
# 무한모드 랭킹 3등 횟수.
InfiniteModeRank_3
# 타임어택 랭킹 1등 횟수.
TimeAttackModeRank_1
# 타임어택 랭킹 2등 횟수.
TimeAttackModeRank_2
# 타임어택 랭킹 3등 횟수.
TimeAttackModeRank_3
"""
@csrf_exempt
def BestRecodDataResponse(request):
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
    dataList = list(BestRecodData.objects.filter(UserSN = request.POST.get('SN')))

    if len(dataList) == 0:
        return HttpResponse('', content_type='application/json')

    record = dataList[0]
    SendData = {}
    SendData['InfiniteModeRank_1'] = record.InfiniteModeRank_1
    SendData['InfiniteModeRank_2'] = record.InfiniteModeRank_2
    SendData['InfiniteModeRank_3'] = record.InfiniteModeRank_3
    SendData['TimeAttackModeRank_1'] = record.TimeAttackModeRank_1
    SendData['TimeAttackModeRank_2'] = record.TimeAttackModeRank_2
    SendData['TimeAttackModeRank_3'] = record.TimeAttackModeRank_3

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 무한모드 친구 주간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
S_No = 시작위치.
E_No = 끝위치.

리턴값
data['UserSN'] = rankData.UserSN
data['Score'] = rankData.Score
data['CharacterSN'] = rankData.CharacterSN
data['PetSN'] = rankData.PetSN
data['VehicleSN'] = rankData.VehicleSN
data['IsReceive'] = True
data['ReceiveTime'] = 0
임시추가..
data['UserName'] = 유저이름.
data['PictureURL'] = 유저 사진url
"""
@csrf_exempt
def FriendInfiniteWeekRankResponse(request):
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

    elif not request.POST.get('S_No'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'S_No does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('E_No'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'E_No does not exist',
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
    friendList = []
    friendRankList = []
    for friendData in list(FriendData.objects.filter(UserSN = request.POST.get('SN'))):
        friendList.append(friendData.FriendSN)

    min = int(request.POST.get('S_No'))
    max = int(request.POST.get('E_No'))

    cnt = min
    for rankData in list(InfiniteFriendWeekRankData.objects.order_by('-Score')[min : max]):
        if rankData.UserSN in friendList or rankData.UserSN == int(request.POST.get('SN')):
            tokenReceive = list(TokenReceiveData.objects.filter(UserSN = rankData.UserSN, SendUserSN = rankData.UserSN))
            userData = list(UserData.objects.filter(id = rankData.UserSN))
            cnt = cnt + 1
            data = {}
            data['UserSN'] = rankData.UserSN
            data['Rank'] = cnt
            data['Score'] = rankData.Score
            data['CharacterSN'] = rankData.CharacterSN
            data['Pet1SN'] = rankData.Pet1SN
            data['Pet2SN'] = rankData.Pet2SN
            data['VehicleSN'] = rankData.VehicleSN
            if len(tokenReceive) > 0:
                data['IsReceive'] = tokenReceive[0].IsReceive
                data['ReceiveTime'] = myUtil.ToSecRemaining(tokenReceive[0].ReceiveTime)
            else:
                data['IsReceive'] = True
                data['ReceiveTime'] = 0

            if len(userData) > 0:
                data['UserName'] = myUtil.encodeStr(userData[0].UserName)
                data['PictureURL'] = userData[0].PictureURL
            friendRankList.append(data)

    return HttpResponse(myUtil.JsonPaser(friendRankList), content_type='application/json')

#-------------------------------------------------------------------------------

# 타임어택 친구 주간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
S_No = 시작위치.
E_No = 끝위치.

리턴값
data['UserSN'] = rankData.UserSN
data['Score'] = rankData.Score
data['CharacterSN'] = rankData.CharacterSN
data['PetSN'] = rankData.PetSN
data['VehicleSN'] = rankData.VehicleSN

임시추가..
data['UserName'] = 유저이름.
data['PictureURL'] = 유저 사진url
"""
@csrf_exempt
def FriendTimeAttackWeekRankResponse(request):
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

    elif not request.POST.get('S_No'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'S_No does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('E_No'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'E_No does not exist',
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
    friendList = []
    friendRankList = []
    for friendData in list(FriendData.objects.filter(UserSN = request.POST.get('SN'))):
        friendList.append(friendData.FriendSN)

    min = int(request.POST.get('S_No'))
    max = int(request.POST.get('E_No'))

    cnt = min
    for rankData in list(TimeAttackFriendWeekRankData.objects.order_by('-Score')[min : max]):
        if rankData.UserSN in friendList or str(rankData.UserSN) == request.POST.get('SN'):
            tokenReceive = list(TokenReceiveData.objects.filter(UserSN = rankData.UserSN, SendUserSN = rankData.UserSN))
            userData = list(UserData.objects.filter(id = rankData.UserSN))
            cnt = cnt + 1
            data = {}
            data['UserSN'] = rankData.UserSN
            data['Rank'] = cnt
            data['Score'] = rankData.Score
            data['CharacterSN'] = rankData.CharacterSN
            data['Pet1SN'] = rankData.Pet1SN
            data['Pet2SN'] = rankData.Pet2SN
            data['VehicleSN'] = rankData.VehicleSN
            if len(tokenReceive) > 0:
                data['IsReceive'] = tokenReceive[0].IsReceive
                data['ReceiveTime'] = myUtil.ToSecRemaining(tokenReceive[0].ReceiveTime)
            else:
                data['IsReceive'] = True
                data['ReceiveTime'] = 0

            if len(userData) > 0:
                data['UserName'] = myUtil.encodeStr(userData[0].UserName)
                data['PictureURL'] = userData[0].PictureURL
            friendRankList.append(data)

    return HttpResponse(myUtil.JsonPaser(friendRankList), content_type='application/json')


#-------------------------------------------------------------------------------

# 무한모드 주간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
S_No = 시작위치.
E_No = 끝위치.

리턴값
MyRank = 내랭킹 데이터.
RankData = 랭킹데이터..

data['UserSN'] = rankData.UserSN
data['Score'] = rankData.Score
data['CharacterSN'] = rankData.CharacterSN
data['PetSN'] = rankData.PetSN
data['VehicleSN'] = rankData.VehicleSN

임시추가..
data['UserName'] = 유저이름.
data['PictureURL'] = 유저 사진url
"""
@csrf_exempt
def InfiniteWeekRankResponse(request):
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

    elif not request.POST.get('S_No'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'S_No does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('E_No'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'E_No does not exist',
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
    RankList = []
    # min = int(request.POST.get('S_No'))
    # max = int(request.POST.get('E_No'))
    min = 0
    max = 30

    cnt = min
    myRank = 0
    for rankData in list(InfiniteWeekRankData.objects.filter(
            (Q(Score__gt = 0) | Q(UserSN = user.id)) & Q(Score__lt = 1000000)
    ).order_by('-Score')[min : max]):
        userData = list(UserData.objects.filter(id = rankData.UserSN))
        cnt = cnt + 1
        data = {}
        data['UserSN'] = rankData.UserSN
        data['Rank'] = cnt
        data['Score'] = rankData.Score
        data['CharacterSN'] = rankData.CharacterSN
        data['Pet1SN'] = rankData.Pet1SN
        data['Pet2SN'] = rankData.Pet2SN
        data['VehicleSN'] = rankData.VehicleSN

        if len(userData) > 0:
            data['UserName'] = myUtil.encodeStr(userData[0].UserName)
            data['PictureURL'] = userData[0].PictureURL
        else:
            continue
            
        RankList.append(data)

        if rankData.UserSN == int(request.POST.get('SN')):
            SendData['MyRank'] = data
            myRank = cnt

    SendData['RankData'] = RankList
    SendData['MyPercent'] = int(myRank / cnt * 100)
    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 타임어택 주간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
S_No = 시작위치.
E_No = 끝위치.

리턴값
data['UserSN'] = rankData.UserSN
data['Score'] = rankData.Score
data['CharacterSN'] = rankData.CharacterSN
data['PetSN'] = rankData.PetSN
data['VehicleSN'] = rankData.VehicleSN
"""
@csrf_exempt
def TimeAttackWeekRankResponse(request):
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
    RankList = []
    min = int(request.POST.get('S_No'))
    max = int(request.POST.get('E_No'))

    cnt = min
    myRank = 0
    for rankData in list(TimeAttackWeekRankData.objects.order_by('-Score')[min : max]):
        userData = list(UserData.objects.filter(id = rankData.UserSN))
        cnt = cnt + 1
        data = {}
        data['UserSN'] = rankData.UserSN
        data['Rank'] = cnt
        data['Score'] = rankData.Score
        data['CharacterSN'] = rankData.CharacterSN
        data['Pet1SN'] = rankData.Pet1SN
        data['Pet2SN'] = rankData.Pet2SN
        data['VehicleSN'] = rankData.VehicleSN

        if len(userData) > 0:
            data['UserName'] = myUtil.encodeStr(userData[0].UserName)
            data['PictureURL'] = userData[0].PictureURL
        RankList.append(data)

        if rankData.UserSN == int(request.POST.get('SN')):
            SendData['MyRank'] = data
            myRank = cnt

        SendData['RankData'] = RankList
        SendData['MyPercent'] = int(myRank / cnt * 100)

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')

#-------------------------------------------------------------------------------

# 무한모드 월간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
S_No = 시작위치.
E_No = 끝위치.

리턴값
data['UserSN'] = rankData.UserSN
data['Score'] = rankData.Score
data['CharacterSN'] = rankData.CharacterSN
data['PetSN'] = rankData.PetSN
data['VehicleSN'] = rankData.VehicleSN
"""
@csrf_exempt
def InfiniteMonthRankResponse(request):
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
    RankList = []
    min = int(request.POST.get('S_No'))
    max = int(request.POST.get('E_No'))

    min = 0
    max = 30

    cnt = min
    myRank = 0
    for rankData in list(InfiniteMonthRankData.objects.filter(
            (Q(Score__gt = 0) | Q(UserSN = user.id)) & Q(Score__lt = 1000000)
    ).order_by('-Score')[min : max]):
        userData = list(UserData.objects.filter(id = rankData.UserSN))
        cnt = cnt + 1
        data = {}
        data['UserSN'] = rankData.UserSN
        data['Rank'] = cnt
        data['Score'] = rankData.Score
        data['CharacterSN'] = rankData.CharacterSN
        data['Pet1SN'] = rankData.Pet1SN
        data['Pet2SN'] = rankData.Pet2SN
        data['VehicleSN'] = rankData.VehicleSN

        if len(userData) > 0:
            data['UserName'] = myUtil.encodeStr(userData[0].UserName)
            data['PictureURL'] = userData[0].PictureURL
        else:
            continue
            
        RankList.append(data)

        if rankData.UserSN == int(request.POST.get('SN')):
            SendData['MyRank'] = data
            myRank = cnt

        SendData['RankData'] = RankList
        SendData['MyPercent'] = int(myRank / cnt * 100)

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 타임어택 월간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
S_No = 시작위치.
E_No = 끝위치.

리턴값
data['UserSN'] = rankData.UserSN
data['Score'] = rankData.Score
data['CharacterSN'] = rankData.CharacterSN
data['PetSN'] = rankData.PetSN
data['VehicleSN'] = rankData.VehicleSN
"""
@csrf_exempt
def TimeAttackMonthRankResponse(request):
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
    RankList = []
    min = int(request.POST.get('S_No'))
    max = int(request.POST.get('E_No'))

    cnt = min
    myRank = 0
    for rankData in list(TimeAttackMonthRankData.objects.order_by('-Score')[min : max]):
        userData = list(UserData.objects.filter(id = rankData.UserSN))
        cnt = cnt + 1
        data = {}
        data['UserSN'] = rankData.UserSN
        data['Rank'] = cnt
        data['Score'] = rankData.Score
        data['CharacterSN'] = rankData.CharacterSN
        data['Pet1SN'] = rankData.Pet1SN
        data['Pet2SN'] = rankData.Pet2SN
        data['VehicleSN'] = rankData.VehicleSN

        if len(userData) > 0:
            data['UserName'] = myUtil.encodeStr(userData[0].UserName)
            data['PictureURL'] = userData[0].PictureURL
        RankList.append(data)

        if rankData.UserSN == int(request.POST.get('SN')):
            SendData['MyRank'] = data
            myRank = cnt

        SendData['RankData'] = RankList
        SendData['MyPercent'] = int(myRank / cnt * 100)

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 무한모드 친구 전주간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
MyRank = 내랭킹
RewardData
    - Type = 1 : 골드, 2 : 캐쉬, 3 : 아이템.
    - ItemSN = 아이템SN.
    - Value = 수량.
RankData
    - UserSN = 유저 번호.
    - Rank = 랭킹.
    - Score = 점수.
    - UserName = 유저 이름.
    - PictureURL = 사진URL.

"""
@csrf_exempt
def FriendInfiniteLastWeekRankResponse(request):
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

    # 랭킹확인여부.
    confirmData = list(InfiniteFriendLastWeekRankData.objects.filter(UserSN = request.POST.get('SN')))
    if len(confirmData) == 0 or confirmData[0].Confirm == True:
        return HttpResponse('', content_type='application/json')

    confirmData[0].Confirm = True
    confirmData[0].save()

    friendList = []
    friendRankList = []
    SendData = {}
    RewardData = []
    RewardList = []
    for friendData in list(FriendData.objects.filter(UserSN = request.POST.get('SN'))):
        friendList.append(friendData.FriendSN)

    cnt = 1
    for rankData in list(InfiniteFriendLastWeekRankData.objects.order_by('-Score')):
        if rankData.UserSN in friendList or rankData.UserSN == int(request.POST.get('SN')):
            userData = list(UserData.objects.filter(id = rankData.UserSN))
            data = {}
            data['UserSN'] = rankData.UserSN
            data['Score'] = rankData.Score
            data['Rank'] = cnt

            if len(userData) > 0:
                data['UserName'] = myUtil.encodeStr(userData[0].UserName)
                data['PictureURL'] = userData[0].PictureURL

            friendRankList.append(data)

            if rankData.Score > 0:
                # 보상처리.
                if cnt == 1 and int(request.POST.get('SN')) == rankData.UserSN:
                    SendData['MyRank'] = cnt
                    RewardList = list(FriendRankNo1Reward.objects.all())
                elif cnt == 2 and int(request.POST.get('SN')) == rankData.UserSN:
                    SendData['MyRank'] = cnt
                    RewardList = list(FriendRankNo2Reward.objects.all())
                elif cnt == 3 and int(request.POST.get('SN')) == rankData.UserSN:
                    SendData['MyRank'] = cnt
                    RewardList = list(FriendRankNo3Reward.objects.all())
            else:
                RewardList = []

            cnt = cnt + 1

    for reward in RewardList:
        data = {}
        if reward.Type == 1:
            UserList = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))
            if len(UserList) > 0:
                money = UserList[0]
                money.GoldValue = money.GoldValue + reward.Value
                money.save()
                data['Type'] = reward.Type
                data['ItemSN'] = reward.ItemSN
                data['Value'] = reward.Value
        elif reward.Type == 2:
            UserList = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))
            if len(UserList) > 0:
                money = UserList[0]
                money.CashValue = money.CashValue + reward.Value
                money.save()
                data['Type'] = reward.Type
                data['ItemSN'] = reward.ItemSN
                data['Value'] = reward.Value
        elif reward.Type == 3:
            myItem = list(ItemData.objects.filter(UserSN = request.POST.get('SN'), ItemSN = reward.ItemSN))
            if len(myItem) > 0:
                myItem[0].Value = myItem[0].Value + reward.Value
                myItem[0].save()
            else:
                itemdata = ItemData(UserSN = request.POST.get('SN'), ItemSN = reward.ItemSN, Value = reward.Value)
                itemdata.save()

            data['Type'] = reward.Type
            data['ItemSN'] = reward.ItemSN
            data['Value'] = reward.Value

        RewardData.append(data)

    SendData['RankData'] = friendRankList
    SendData['RewardData'] = RewardData

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 타임어택 친구 전주간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
MyRank = 내랭킹
RewardData
    - Type = 1 : 골드, 2 : 캐쉬, 3 : 아이템.
    - ItemSN = 아이템SN.
    - Value = 수량.
RankData
    - UserSN = 유저 번호.
    - Rank = 랭킹.
    - Score = 점수.
    - UserName = 유저 이름.
    - PictureURL = 사진URL.

"""
@csrf_exempt
def FriendTimeAttackLastWeekRankResponse(request):
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

    # 랭킹확인여부.
    confirmData = list(TimeAttackFriendLastWeekRankData.objects.filter(UserSN = request.POST.get('SN')))
    if len(confirmData) == 0 or confirmData[0].Confirm == True:
        return HttpResponse('', content_type='application/json')

    confirmData[0].Confirm = True
    confirmData[0].save()

    friendList = []
    friendRankList = []
    SendData = {}
    RewardData = []
    RewardList = []
    for friendData in list(FriendData.objects.filter(UserSN = request.POST.get('SN'))):
        friendList.append(friendData.FriendSN)

    cnt = 1
    for rankData in list(TimeAttackFriendLastWeekRankData.objects.order_by('-Score')):
        if rankData.UserSN in friendList or rankData.UserSN == int(request.POST.get('SN')):
            userData = list(UserData.objects.filter(id = rankData.UserSN))
            data = {}
            data['UserSN'] = rankData.UserSN
            data['Score'] = rankData.Score
            data['Rank'] = cnt

            if len(userData) > 0:
                data['UserName'] = myUtil.encodeStr(userData[0].UserName)
                data['PictureURL'] = userData[0].PictureURL

            friendRankList.append(data)

            if rankData.Score > 0:
                # 보상처리.
                if cnt == 1 and int(request.POST.get('SN')) == rankData.UserSN:
                    SendData['MyRank'] = cnt
                    RewardList = list(FriendRankNo1Reward.objects.all())
                elif cnt == 2 and int(request.POST.get('SN')) == rankData.UserSN:
                    SendData['MyRank'] = cnt
                    RewardList = list(FriendRankNo2Reward.objects.all())
                elif cnt == 3 and int(request.POST.get('SN')) == rankData.UserSN:
                    SendData['MyRank'] = cnt
                    RewardList = list(FriendRankNo3Reward.objects.all())
            else:
                RewardList = []

            cnt = cnt + 1

    for reward in RewardList:
        data = {}
        if reward.Type == 1:
            UserList = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))
            if len(UserList) > 0:
                money = UserList[0]
                money.GoldValue = money.GoldValue + reward.Value
                money.save()
                data['Type'] = reward.Type
                data['ItemSN'] = reward.ItemSN
                data['Value'] = reward.Value
        elif reward.Type == 2:
            UserList = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))
            if len(UserList) > 0:
                money = UserList[0]
                money.CashValue = money.CashValue + reward.Value
                money.save()
                data['Type'] = reward.Type
                data['ItemSN'] = reward.ItemSN
                data['Value'] = reward.Value
        elif reward.Type == 3:
            myItem = list(ItemData.objects.filter(UserSN = request.POST.get('SN'), ItemSN = reward.ItemSN))
            if len(myItem) > 0:
                myItem[0].Value = myItem[0].Value + reward.Value
                myItem[0].save()
            else:
                itemdata = ItemData(UserSN = request.POST.get('SN'), ItemSN = reward.ItemSN, Value = reward.Value)
                itemdata.save()

            data['Type'] = reward.Type
            data['ItemSN'] = reward.ItemSN
            data['Value'] = reward.Value

        RewardData.append(data)

    SendData['RankData'] = friendRankList
    SendData['RewardData'] = RewardData

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 무한모드 전주간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
SendData['MyRank'] = 내랭크.
SendData['MyReward'] = 보상 값.
RankData
    data['UserSN'] = rankData.UserSN
    data['Score'] = rankData.Score

    data['UserName'] = myUtil.encodeStr(userData[0].UserName)
    data['PictureURL']

"""
@csrf_exempt
def InfiniteLastWeekRankResponse(request):
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

    # 랭킹확인여부.
    confirmData = list(InfiniteLastWeekRankData.objects.filter(UserSN = request.POST.get('SN')))
    if len(confirmData) == 0 or confirmData[0].Confirm == True:
        return HttpResponse('', content_type='application/json')

    confirmData[0].Confirm = True
    confirmData[0].save()


    data = {
            'IsReward' : False,
            'RewardValue' : 0,
        }
    return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    RankList = []
    SendData = {}
    cnt = 1
    for rankData in list(InfiniteLastWeekRankData.objects.order_by('-Score')):
        userData = list(UserData.objects.filter(id = rankData.UserSN))
        data = {}
        data['UserSN'] = rankData.UserSN
        data['Score'] = rankData.Score
        data['Rank'] = cnt

        if len(userData) > 0:
            data['UserName'] = myUtil.encodeStr(userData[0].UserName)
            data['PictureURL'] = userData[0].PictureURL

        RankList.append(data)

        if rankData.Score > 0:
            # 보상처리.
            if cnt == 1 and request.POST.get('SN') == rankData.UserSN:
                UserList = list(MoneyData.objects.filter(UserSN = rankData.UserSN))
                if len(UserList) > 0:
                    MoneyData = UserList[0]
                    MoneyData.CashValue = 5
                    MoneyData.save()
                    SendData['MyRank'] = 1
                    SendData['MyReward'] = 5
            elif cnt == 2 and request.POST.get('SN') == rankData.UserSN:
                UserList = list(MoneyData.objects.filter(UserSN = rankData.UserSN))
                if len(UserList) > 0:
                    MoneyData = UserList[0]
                    MoneyData.GoldValue = 5
                    MoneyData.save()
                    SendData['MyRank'] = 2
                    SendData['MyReward'] = 5
            elif cnt == 3 and request.POST.get('SN') == rankData.UserSN:
                itemdata = ItemData(UserSN = rankData.UserSN, ItemSN = 1)
                itemdata.save()
                SendData['MyRank'] = 3
                SendData['MyReward'] = 1

        cnt = cnt + 1

    SendData['RankData'] = RankList

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 타임어택 전주간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
data['UserSN'] = rankData.UserSN
data['Score'] = rankData.Score

"""
@csrf_exempt
def TimeAttackLastWeekRankResponse(request):
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

    # 랭킹확인여부.
    confirmData = list(TimeAttackLastWeekRankData.objects.filter(UserSN = request.POST.get('SN')))
    if len(confirmData) == 0 or confirmData[0].Confirm == True:
        return HttpResponse('', content_type='application/json')

    confirmData[0].Confirm = True
    confirmData[0].save()

    data = {
            'IsReward' : False,
            'RewardValue' : 0,
        }
    return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    RankList = []
    SendData = {}
    cnt = 1
    for rankData in list(TimeAttackLastWeekRankData.objects.order_by('-Score')):
        data = {}
        data['UserSN'] = rankData.UserSN
        data['Score'] = rankData.Score
        data['Rank'] = cnt

        RankList.append(data)

        if rankData.Score > 0:
            # 보상처리.
            if cnt == 1 and request.POST.get('SN') == rankData.UserSN:
                UserList = list(MoneyData.objects.filter(UserSN = rankData.UserSN))
                if len(UserList) > 0:
                    MoneyData = UserList[0]
                    MoneyData.CashValue = 5
                    MoneyData.save()
                    SendData['MyRank'] = 1
                    SendData['MyReward'] = 5
            elif cnt == 2 and request.POST.get('SN') == rankData.UserSN:
                UserList = list(MoneyData.objects.filter(UserSN = rankData.UserSN))
                if len(UserList) > 0:
                    MoneyData = UserList[0]
                    MoneyData.GoldValue = 5
                    MoneyData.save()
                    SendData['MyRank'] = 2
                    SendData['MyReward'] = 5
            elif cnt == 3 and request.POST.get('SN') == rankData.UserSN:
                itemdata = ItemData(UserSN = rankData.UserSN, ItemSN = 1)
                itemdata.save()
                SendData['MyRank'] = 3
                SendData['MyReward'] = 1

        cnt = cnt + 1

    SendData['RankData'] = RankList

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 무한모드 전월간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
data['UserSN'] = rankData.UserSN
data['Score'] = rankData.Score

"""
@csrf_exempt
def InfiniteLastMonthRankResponse(request):
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

    # 랭킹확인여부.
    confirmData = list(InfiniteLastMonthRankData.objects.filter(UserSN = request.POST.get('SN')))
    if len(confirmData) > 0 and confirmData[0].Confirm == True:
        return HttpResponse('', content_type='application/json')

    confirmData[0].Confirm = True
    confirmData[0].save()

    data = {
            'IsReward' : False,
            'RewardValue' : 0,
        }
    return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    RankList = []
    SendData = {}
    cnt = 1
    for rankData in list(InfiniteLastMonthRankData.objects.order_by('-Score')):
        data = {}
        data['UserSN'] = rankData.UserSN
        data['Score'] = rankData.Score
        data['Rank'] = cnt

        RankList.append(data)

        if rankData.Score > 0:
            # 보상처리.
            if cnt == 1 and request.POST.get('SN') == rankData.UserSN:
                UserList = list(MoneyData.objects.filter(UserSN = rankData.UserSN))
                if len(UserList) > 0:
                    MoneyData = UserList[0]
                    MoneyData.CashValue = 5
                    MoneyData.save()
                    SendData['MyRank'] = 1
                    SendData['MyReward'] = 5
            elif cnt == 2 and request.POST.get('SN') == rankData.UserSN:
                UserList = list(MoneyData.objects.filter(UserSN = rankData.UserSN))
                if len(UserList) > 0:
                    MoneyData = UserList[0]
                    MoneyData.GoldValue = 5
                    MoneyData.save()
                    SendData['MyRank'] = 2
                    SendData['MyReward'] = 5
            elif cnt == 3 and request.POST.get('SN') == rankData.UserSN:
                itemdata = ItemData(UserSN = rankData.UserSN, ItemSN = 1)
                itemdata.save()
                SendData['MyRank'] = 3
                SendData['MyReward'] = 1

        cnt = cnt + 1

    SendData['RankData'] = RankList

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 타임어택 전월간랭킹
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
data['UserSN'] = rankData.UserSN
data['Score'] = rankData.Score

"""
@csrf_exempt
def TimeAttackLastMonthRankResponse(request):
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

    # 랭킹확인여부.
    confirmData = list(TimeAttackLastMonthRankData.objects.filter(UserSN = request.POST.get('SN')))
    if len(confirmData) > 0 and confirmData[0].Confirm == True:
        return HttpResponse('', content_type='application/json')

    confirmData[0].Confirm = True
    confirmData[0].save()

    data = {
            'IsReward' : False,
            'RewardValue' : 0,
        }
    return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    RankList = []
    SendData = {}
    cnt = 1
    for rankData in list(TimeAttackLastMonthRankData.objects.order_by('-Score')):
        data = {}
        data['UserSN'] = rankData.UserSN
        data['Score'] = rankData.Score
        data['Rank'] = cnt

        RankList.append(data)

        if rankData.Score > 0:
            # 보상처리.
            if cnt == 1 and request.POST.get('SN') == rankData.UserSN:
                UserList = list(MoneyData.objects.filter(UserSN = rankData.UserSN))
                if len(UserList) > 0:
                    MoneyData = UserList[0]
                    MoneyData.CashValue = 5
                    MoneyData.save()
                    SendData['MyRank'] = 1
                    SendData['MyReward'] = 5
            elif cnt == 2 and request.POST.get('SN') == rankData.UserSN:
                UserList = list(MoneyData.objects.filter(UserSN = rankData.UserSN))
                if len(UserList) > 0:
                    MoneyData = UserList[0]
                    MoneyData.GoldValue = 5
                    MoneyData.save()
                    SendData['MyRank'] = 2
                    SendData['MyReward'] = 5
            elif cnt == 3 and request.POST.get('SN') == rankData.UserSN:
                itemdata = ItemData(UserSN = rankData.UserSN, ItemSN = 1)
                itemdata.save()
                SendData['MyRank'] = 3
                SendData['MyReward'] = 1

        cnt = cnt + 1

    SendData['RankData'] = RankList

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')

#-------------------------------------------------------------------------------

# 랭킹 초기화 시간 가져오기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
SendData['Week'] = 주간랭킹 남은초.
SendData['Month'] = 뭘간랭킹 남은초.
SendData['Friend'] = 친구 주간랭킹 남은초.
"""
@csrf_exempt
def InitRankTimeResponse(request):
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
    rankData = list(RankInfoData.objects.all())[0]
    SendData = {}
    SendData['Week'] = myUtil.ToSecRemaining(rankData.WeekInitTime)
    SendData['Month'] = myUtil.ToSecRemaining(rankData.MonthInitTime)
    SendData['Friend'] = myUtil.ToSecRemaining(rankData.FriendInitTime)

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 치킨 주간랭킹 초기화 여부.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
Confirm = 주간랭킹 확인여부.

"""
@csrf_exempt
def IsChickenLastWeekRank(request):
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
    SendData['Confirm'] = True;
    # 랭킹확인여부.
    confirmData = list(InfiniteLastWeekRankData.objects.filter(UserSN = request.POST.get('SN')))
    if len(confirmData) > 0 and confirmData[0].Confirm == False:
        SendData['Confirm'] = False;

    confirmData = list(TimeAttackLastWeekRankData.objects.filter(UserSN = request.POST.get('SN')))
    if len(confirmData) > 0 and confirmData[0].Confirm == False:
        SendData['Confirm'] = False;


    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 치킨 월간랭킹 초기화 여부.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
Confirm = 월간랭킹 확인여부.

"""
@csrf_exempt
def IsChickenLastMonthRank(request):
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
    SendData['Confirm'] = True;
    # 랭킹확인여부.
    confirmData = list(InfiniteLastMonthRankData.objects.filter(UserSN = request.POST.get('SN')))
    if len(confirmData) > 0 and confirmData[0].Confirm == False:
        SendData['Confirm'] = False;

    confirmData = list(TimeAttackLastMonthRankData.objects.filter(UserSN = request.POST.get('SN')))
    if len(confirmData) > 0 and confirmData[0].Confirm == False:
        SendData['Confirm'] = False;


    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
