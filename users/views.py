# -*- coding: utf-8 -*-
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from users.models import *
from GameData.models import *
from Ranking.models import *
from ServerInfo.models import *
from GameData.models import *
from datetime import *
import myUtil

import logging
logger = logging.getLogger('ckw')

@csrf_exempt
def login(request):
    if request.method == 'GET':
        data = {
            'ErrorCode' : '99',
            'Message' : 'error',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    if not request.POST.get('UserID'):
        data = {
            'ErrorCode' : '101',
            'Message' : 'UserID does not exist',
        }
        return ResponseData(data)
    elif not request.POST.get('LoginTime'):
        data = { 'ErrorCode' : '102', 'Message' : 'LoginTime does not exist'}
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    userid = str(request.POST.get('UserID',''));
    userList = list(UserData.objects.filter(UserID = userid))
    newUser = 1
    if len(userList) > 0 :
        user = userList[0]
        user.LastPlayTime = datetime.strptime(request.POST.get('LoginTime'), '%Y-%m-%d/%H:%M:%S')
        user.Auth = myUtil.encodeStr(myUtil.random_char(20))
        user.save()
        newUser = 0
    else :
        user = UserData(UserID = userid, Auth = myUtil.encodeStr(myUtil.random_char(20)), FirstPlayTime = datetime.strptime(request.POST.get('LoginTime'), '%Y-%m-%d/%H:%M:%S'), LastPlayTime = datetime.strptime(request.POST.get('LoginTime'), '%Y-%m-%d/%H:%M:%S'))
        user.OSType = request.POST.get('OSType')
        user.ContryCode = request.POST.get('ContryCode')
        user.save()

        user.UserName = 'Player' + str(user.id)
        user.PictureURL = ''
        user.save()

        charData = CharacterData()
        charData.UserSN = user.id
        charData.CharacterSN = 1
        charData.Level_HP = 1
        charData.Level_MP = 1
        charData.Level_Magnet = 1
        charData.Level_GodDash = 1
        charData.Level_Shield = 1
        charData.Level_Big = 1
        charData.Level_Small = 1
        charData.save()

        petData = PetData()
        petData.UserSN = user.id
        petData.PetSN = 6
        petData.Grade = 3
        petData.save()

        playData = CurrPlayData()
        playData.UserSN = user.id
        playData.CharacterSN = 1
        playData.GameMode = 1
        playData.Pet1SN = 6
        playData.Pet2SN = -1
        playData.VehicleSN = 0
        playData.save()

        recordData = PlayRecordData()
        recordData.UserSN = user.id
        recordData.TotalInviteFriend = 0
        recordData.TotalPlay = 1
        recordData.TotalRelayPlay = 0
        recordData.BestScore = 0
        recordData.TotalScore = 0
        recordData.BestDistance = 0
        recordData.TotalDistance = 0
        recordData.BestGetCoin = 0
        recordData.TotalGetCoin = 0
        recordData.TotalGold = 0
        recordData.TotalUseGold = 0
        recordData.BestDashScore = 0
        recordData.TotalUseDash = 0
        recordData.Item_1 = 0
        recordData.Item_2 = 0
        recordData.Item_3 = 0
        recordData.Item_4 = 0
        recordData.Item_5 = 0
        recordData.save()

        token = TokenData()
        token.UserSN = user.id
        token.ToeknValue = 6
        token.CreateTime = datetime.now()
        token.save()

        CSRData = ChickenScoreRewardData()
        CSRData.UserSN = user.id
        CSRData.Score = 0
        CSRData.save()

        rank = InfiniteWeekRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()
        rank = TimeAttackWeekRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()
        rank = InfiniteMonthRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()
        rank = TimeAttackMonthRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()
        rank = InfiniteFriendWeekRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()
        rank = TimeAttackFriendWeekRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()

        moneyData = MoneyData(UserSN = user.id, GoldValue = 5000, CashValue = 5)
        moneyData.save()

        newUser = 1

    if userid.startswith("xiaomi-"):
        userName = str(request.POST.get('UserName', user.UserName))
        userImgUrl = str(request.POST.get('UserImgUrl', user.PictureURL))

        changed = False
        if userName != user.UserName :
            changed = True
            user.UserName = userName
        if userImgUrl != user.PictureURL :
            changed = True
            user.PictureURL = userImgUrl

        if changed: user.save()

        # logger.info(str(request.POST.getlist('Friend')))
        for friendID in request.POST.getlist('Friend'):
            friend = UserData.objects.filter(UserID = friendID)
            if len(friend) > 0:
                fList = list(FriendData.objects.filter(UserSN=user.id, FriendSN=friend[0].id))
                if len(fList) == 0 :
                    fd = FriendData(UserSN=user.id, FriendSN=friend[0].id)
                    fd.save()

    data = {'SN' : user.id,'Auth' : user.Auth, 'NewUser' : newUser}
    return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

@csrf_exempt
def login2(request):
    if request.method == 'GET':
        data = {
            'ErrorCode':'99',
            'Message':'error',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    if not request.POST.get('UserID'):
        data = {
            'ErrorCode':'101',
            'Message':'UserID does not exist',
        }
        return ResponseData(data)
    elif not request.POST.get('LoginTime'):
        data = { 'ErrorCode':'102','Message':'LoginTime does not exist'}
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')   
    elif not request.POST.get('OSType'):
        data = {
            'ErrorCode':'101',
            'Message':'OSType does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json') 
    if not request.POST.get('Version'):
        data = {
            'ErrorCode':'101',
            'Message':'Version does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


    userid = str(request.POST.get('UserID',''));
    userList = list(UserData.objects.filter(UserID = userid))
    newUser = 1
    if len(userList) > 0 :
        user = userList[0]
        user.LastPlayTime = datetime.strptime(request.POST.get('LoginTime'), '%Y-%m-%d/%H:%M:%S')
        user.Auth = myUtil.encodeStr(myUtil.random_char(20))
        user.save()
        newUser = 0
    else :
        user = UserData(UserID = userid, Auth = myUtil.encodeStr(myUtil.random_char(20)), FirstPlayTime = datetime.strptime(request.POST.get('LoginTime'), '%Y-%m-%d/%H:%M:%S'), LastPlayTime = datetime.strptime(request.POST.get('LoginTime'), '%Y-%m-%d/%H:%M:%S'))
        user.OSType = request.POST.get('OSType')
        user.ContryCode = request.POST.get('ContryCode')
        user.save()

        user.UserName = 'Player' + str(user.id)
        user.PictureURL = ''
        user.save()

        charData = CharacterData()
        charData.UserSN = user.id
        charData.CharacterSN = 1
        charData.Level_HP = 1
        charData.Level_MP = 1
        charData.Level_Magnet = 1
        charData.Level_GodDash = 1
        charData.Level_Shield = 1
        charData.Level_Big = 1
        charData.Level_Small = 1
        charData.save()

        petData = PetData()
        petData.UserSN = user.id
        petData.PetSN = 6
        petData.Grade = 3
        petData.save()

        playData = CurrPlayData()
        playData.UserSN = user.id
        playData.CharacterSN = 1
        playData.GameMode = 1
        playData.Pet1SN = 6
        playData.Pet2SN = -1
        playData.VehicleSN = 0
        playData.save()

        recordData = PlayRecordData()
        recordData.UserSN = user.id
        recordData.TotalInviteFriend = 0
        recordData.TotalPlay = 1
        recordData.TotalRelayPlay = 0
        recordData.BestScore = 0
        recordData.TotalScore = 0
        recordData.BestDistance = 0
        recordData.TotalDistance = 0
        recordData.BestGetCoin = 0
        recordData.TotalGetCoin = 0
        recordData.TotalGold = 0
        recordData.TotalUseGold = 0
        recordData.BestDashScore = 0
        recordData.TotalUseDash = 0
        recordData.Item_1 = 0
        recordData.Item_2 = 0
        recordData.Item_3 = 0
        recordData.Item_4 = 0
        recordData.Item_5 = 0
        recordData.save()

        token = TokenData()
        token.UserSN = user.id
        token.ToeknValue = 6
        token.CreateTime = datetime.now()
        token.save()

        CSRData = ChickenScoreRewardData()
        CSRData.UserSN = user.id
        CSRData.Score = 0
        CSRData.save()

        rank = InfiniteWeekRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()
        rank = TimeAttackWeekRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()
        rank = InfiniteMonthRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()
        rank = TimeAttackMonthRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()
        rank = InfiniteFriendWeekRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()
        rank = TimeAttackFriendWeekRankData(UserSN = user.id, Score = 0, CharacterSN = 1, Pet1SN = 0, Pet2SN = 0, VehicleSN = 0)
        rank.save()

        moneyData = MoneyData(UserSN = user.id, GoldValue = 5000, CashValue = 5)
        moneyData.save()

        newUser = 1

    if userid.startswith("xiaomi-"):
        userName = str(request.POST.get('UserName', user.UserName))
        userImgUrl = str(request.POST.get('UserImgUrl', user.PictureURL))

        changed = False
        if userName != user.UserName :
            changed = True
            user.UserName = userName
        if userImgUrl != user.PictureURL :
            changed = True
            user.PictureURL = userImgUrl

        if changed: user.save()

        # logger.info(str(request.POST.getlist('Friend')))
        for friendID in request.POST.getlist('Friend'):
            friend = UserData.objects.filter(UserID = friendID)
            if len(friend) > 0:
                fList = list(FriendData.objects.filter(UserSN=user.id, FriendSN=friend[0].id))
                if len(fList) == 0 :
                    fd = FriendData(UserSN=user.id, FriendSN=friend[0].id)
                    fd.save()

    SendData = {}

    SendData['SN'] = user.id;
    SendData['Auth'] = user.Auth;
    SendData['NewUser'] = newUser;

    stateList = list(ServerState.objects.filter(OSType = request.POST.get('OSType')))
    if len(stateList) > 0:
        state = stateList[0]

        SendData['IsServerRun'] = state.IsServerRun
        SendData['MinVersion'] = state.MinVersion
        SendData['LastVersion'] = state.LastVersion
        SendData['MinVersionStr'] = state.MinVersionStr
        SendData['LastVersionStr'] = state.LastVersionStr
    else:
        data = {
            'ErrorCode':'99',
            'Message':'error',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    noticeList = list(NoticeData.objects.filter(MinVersion__gte = request.POST.get('Version')))
    data = []
    for notice in noticeList:
        data.append(notice.Message) 

    SendData['Notice'] = data

    eventList = list(EventData.objects.filter(MinVersion__gte = request.POST.get('Version')))
    data = []
    for event in eventList:
        data.append(event.URL) 

    SendData['Event'] = data

    #检查是否奖励金币
    dataList = list(DailyCheckData.objects.filter(UserSN = user.id))
    moneyData = MoneyData.objects.filter(UserSN = user.id)[0]
    if len(dataList) > 0:
        data = dataList[0]
        if date.today() > data.CheckTime:
            data.CheckTime = date.today()
            data.save()
            moneyData.CashValue = moneyData.CashValue + 1
            moneyData.save()
            SendData['Reward'] = True
        else:
            SendData['Reward'] = False
    else:
        dayData = DailyCheckData()
        dayData.UserSN = user.id
        dayData.CheckTime = date.today()
        dayData.save()
        SendData['Reward'] = False


    #http://ckw.luckyzune.com/CurrPlayDataResponse/
    playdatalist = list(CurrPlayData.objects.filter(UserSN = user.id))
    if len(playdatalist) > 0:
        playdata = playdatalist[0]
        SendData['CharacterSN'] = playdata.CharacterSN
        SendData['GameMode'] = playdata.GameMode
        SendData['Pet1SN'] = playdata.Pet1SN
        SendData['Pet2SN'] = playdata.Pet2SN
        SendData['VehicleSN'] = playdata.VehicleSN
    else:
        SendData['CharacterSN'] = 1
        SendData['GameMode'] = 1
        SendData['Pet1SN'] = 0
        SendData['Pet2SN'] = 0
        SendData['VehicleSN'] = 0


    #http://ckw.luckyzune.com/InvenDataResponse/
    CharList = list(CharacterData.objects.filter(UserSN = user.id))
    PetList = list(PetData.objects.filter(UserSN = user.id))
    VehicleList = list(VehicleData.objects.filter(UserSN = user.id))
    ItemList = list(ItemData.objects.filter(UserSN = user.id))
    MoenyList = list(MoneyData.objects.filter(UserSN = user.id))
    RewardList = list(ChickenScoreRewardData.objects.filter(UserSN = user.id))

    arr = []
    for CharData in CharList:
        data = {}
        data['CharacterSN'] = CharData.CharacterSN
        data['Level_HP'] = CharData.Level_HP
        data['Level_MP'] = CharData.Level_MP
        data['Level_Magnet'] = CharData.Level_Magnet
        data['Level_GodDash'] = CharData.Level_GodDash
        data['Level_Shield'] = CharData.Level_Shield
        data['Level_Big'] = CharData.Level_Big
        data['Level_Small'] = CharData.Level_Small
        arr.append(data)

    SendData['CharData'] = arr

    arr = []
    for Petdata in PetList:
        data = {}
        data['PetSN'] = Petdata.PetSN
        data['PetGrade'] = Petdata.Grade
        arr.append(data)
    
    SendData['PetData'] = arr

    arr = []
    for Vehicledata in VehicleList:
        data = {}
        data['VehicleSN'] = Vehicledata.VehicleSN
        data['Level'] = Vehicledata.Level
        arr.append(data)
    
    SendData['VehicleData'] = arr

    arr = []
    for Itemdata in ItemList:
        data = {}
        data['ItemSN'] = Itemdata.ItemSN
        data['Value'] = Itemdata.Value
        arr.append(data)
    
    SendData['ItemData'] = arr

    data = {}
    for Moneydata in MoenyList:
        data['GoldValue'] = Moneydata.GoldValue
        data['CashValue'] = Moneydata.CashValue
    
    SendData['MoneyData'] = data
    SendData['RewardData'] = RewardList[0].Score

    #http://ckw.luckyzune.com/TokenDataResponse/
    data = {}
    token = TokenData.objects.filter(UserSN = user.id)[0]
    data['Value'] = token.ToeknValue
    data['Time'] = myUtil.ToLastSec(token.CreateTime)
    SendData['Token'] = data

    #http://ckw.luckyzune.com/InitRankTimeResponse/
    rankDataList = list(RankInfoData.objects.all())
    if len(rankDataList) > 0 :
        rankData = rankDataList[0]
        SendData['Week'] = myUtil.ToSecRemaining(rankData.WeekInitTime)
        SendData['Month'] = myUtil.ToSecRemaining(rankData.MonthInitTime)
        SendData['Friend'] = myUtil.ToSecRemaining(rankData.FriendInitTime)

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
