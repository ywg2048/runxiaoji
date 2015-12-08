# -*- coding: utf-8 -*-
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from GameData.models import *
from ShopData.models import *
from users.models import *
from Ranking.models import *
from MessageData.models import *
from Invite.models import *
from datetime import *
import myUtil

# 최근 플레이어 데이터 가져오기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
CharacterSN = 캐릭터 SN
GameMode = 1 : 무한, 2 : 타임어택.
Pet1SN = 펫 SN
Pet2SN = 펫 SN
VehicleSN = 탈것 SN
"""
@csrf_exempt
def CurrPlayDataResponse(request):
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
    playdatalist = list(CurrPlayData.objects.filter(UserSN = request.POST.get('SN')))
    if len(playdatalist) > 0:
        playdata = playdatalist[0]
        SendData = {
            'CharacterSN' : playdata.CharacterSN,
            'GameMode' : playdata.GameMode,
            'Pet1SN' : playdata.Pet1SN,
            'Pet2SN' : playdata.Pet2SN,
            'VehicleSN' : playdata.VehicleSN
        }
        return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    else:
        SendData = {
            'CharacterSN' : 1,
            'GameMode' : 1,
            'Pet1SN' : 0,
            'Pet2SN' : 0,
            'VehicleSN' : 0
        }
        return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')

#-------------------------------------------------------------------------------

# 플레이 기록데이터 가져오기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
TotalInviteFriend
TotalPlay
TotalRelayPlay
BestScore
TotalScore
BestDistance
TotalDistance
BestGetCoin
TotalGetCoin
TotalGold
TotalUseGold
BestDashScore
TotalUseDash
TotalStartDashItem
TotalMagnetItem
TotalShieldItem
TotalCoinDoubleItem
TotalFullDashGageItem

"""
@csrf_exempt
def PlayRecordDataResponse(request):
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
    dataList = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))
    if len(dataList) == 0:
        return HttpResponse('', content_type='application/json')

    data = {}
    recordData = dataList[0]
    data['TotalInviteFriend'] = recordData.TotalInviteFriend
    data['TotalPlay'] = recordData.TotalPlay
    data['TotalRelayPlay'] = recordData.TotalRelayPlay
    data['BestScore'] = recordData.BestScore
    data['TotalScore'] = recordData.TotalScore
    data['BestDistance'] = recordData.BestDistance
    data['TotalDistance'] = recordData.TotalDistance
    data['BestGetCoin'] = recordData.BestGetCoin
    data['TotalGetCoin'] = recordData.TotalGetCoin
    data['TotalGold'] = recordData.TotalGold
    data['TotalUseGold'] = recordData.TotalUseGold
    data['BestDashScore'] = recordData.BestDashScore
    data['TotalUseDash'] = recordData.TotalUseDash
    data['TotalStartDashItem'] = recordData.Item_1
    data['TotalMagnetItem'] = recordData.Item_2
    data['TotalShieldItem'] = recordData.Item_3
    data['TotalCoinDoubleItem'] = recordData.Item_4
    data['TotalFullDashGageItem'] = recordData.Item_5

    return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


#-------------------------------------------------------------------------------

# 내가 보유하고있는 데이터 가져오기(캐릭터, 펫, 탈것, 아이템, 머니).
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
CharData = {CharacterSN, Level_HP, Level_MP, Level_Magnet, Level_GodDash, Level_Shield, Level_Big, Level_Small}
PetData = {PetSN}
VehicleData = {VehicleSN, Level}
ItemData = {ItemSN, Value}
MoneyData = {GoldValue, CashValue}
RewardData = 치킨점수.

"""
@csrf_exempt
def InvenDataResponse(request):
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

    CharList = list(CharacterData.objects.filter(UserSN = request.POST.get('SN')))
    PetList = list(PetData.objects.filter(UserSN = request.POST.get('SN')))
    VehicleList = list(VehicleData.objects.filter(UserSN = request.POST.get('SN')))
    ItemList = list(ItemData.objects.filter(UserSN = request.POST.get('SN')))
    MoenyList = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))
    RewardList = list(ChickenScoreRewardData.objects.filter(UserSN = request.POST.get('SN')))

    SendData = {}

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

    if len(CharList) > 0:
        SendData['CharData'] = arr

    arr = []
    for Petdata in PetList:
        data = {}
        data['PetSN'] = Petdata.PetSN
        data['PetGrade'] = Petdata.Grade
        arr.append(data)
    if len(PetList) > 0:
        SendData['PetData'] = arr

    arr = []
    for Vehicledata in VehicleList:
        data = {}
        data['VehicleSN'] = Vehicledata.VehicleSN
        data['Level'] = Vehicledata.Level
        arr.append(data)
    if len(VehicleList) > 0:
        SendData['VehicleData'] = arr

    arr = []
    for Itemdata in ItemList:
        data = {}
        data['ItemSN'] = Itemdata.ItemSN
        data['Value'] = Itemdata.Value
        arr.append(data)
    if len(ItemList) > 0:
        SendData['ItemData'] = arr

    data = {}
    for Moneydata in MoenyList:
        data['GoldValue'] = Moneydata.GoldValue
        data['CashValue'] = Moneydata.CashValue
    if len(MoenyList) > 0:
        SendData['MoneyData'] = data

    if len(RewardList) > 0:
        SendData['RewardData'] = RewardList[0].Score

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 캐릭터 구매처리.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
CharacterSN = 캐릭터SN.

리턴값
SendData['CharacterSN'] = 캐릭터SN
SendData['CostType'] = 구매타입 (1 : 코인, 2 : 캐쉬)
SendData['Cost'] = 구매가.
SendData['Count'] = 수량.

"""
@csrf_exempt
def BuyCharacter(request):
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

    elif not request.POST.get('CharacterSN'):
        data = {
            'ErrorCode' : '103',
            'Message' : 'CharacterSN does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    user = list(UserData.objects.filter(id = request.POST.get('SN')))
    if len(user) == 0:
        data = {
            'ErrorCode' : '105',
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
    # 가격 비교.
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    CharData = list(Shop_CharacterData.objects.filter(id = request.POST.get('CharacterSN')))[0]
    if (CharData.CostType == 1 and CharData.Cost <= moneyData.GoldValue) or (CharData.CostType == 2 and CharData.Cost <= moneyData.CashValue):
        # 캐릭터 생성.
        chardata = CharacterData()
        chardata.CharacterSN = CharData.id
        chardata.Level_HP = 1
        chardata.Level_MP = 1
        chardata.Level_Magnet = 1
        chardata.Level_GodDash = 1
        chardata.Level_Shield = 1
        chardata.Level_Big = 1
        chardata.Level_Small = 1
        chardata.UserSN = request.POST.get('SN')
        chardata.save()

        recordData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if CharData.CostType == 1:
            moneyData.GoldValue = moneyData.GoldValue - CharData.Cost
            moneyData.save()
            # record에 기록...
            recordData.TotalUseGold = recordData.TotalUseGold + CharData.Cost
            recordData.save()
        elif CharData.CostType == 2:
            moneyData.CashValue = moneyData.CashValue - CharData.Cost
            moneyData.save()

        SendData = {}
        SendData['CharacterSN'] = CharData.id
        SendData['CostType'] = CharData.CostType
        SendData['Cost'] = CharData.Cost
        SendData['Count'] = CharData.Value

        return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    else:
        data = {
            'ErrorCode' : '106',
            'Message' : 'Lack of Cost',
            'CostType' : CharData.CostType,
            'Gold' : moneyData.GoldValue,
            'Cash' : moneyData.CashValue,
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


#-------------------------------------------------------------------------------

# 펫 뽑기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
Type = 1 : 슈퍼, 2 : 레어, 3 : 노말.

리턴값
SendData['CostType'] = 구매타입 (1 : 코인, 2 : 캐쉬)
SendData['Cost'] = 구매가.
SendData['RewardType'] = 1 : 펫, 2 : 골드.
SendData['RewardValue'] = RewardType = 1 이면 펫SN, 아니면 골드.
SendData['RewardGrade'] = 등급.
"""
@csrf_exempt
def GetPetResponse(request):
    import random
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
            'ErrorCode' : '105',
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

    # 가격 비교.
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    petCostData = list(Shop_PetData.objects.filter(Type = request.POST.get('Type')))[0]

    if (petCostData.CostType == 1 and petCostData.CostValue <= moneyData.GoldValue) or (petCostData.CostType == 2 and petCostData.CostValue <= moneyData.CashValue):
        ChooseData = ''
        Grade = int(request.POST.get('Type'))
        if int(request.POST.get('Type')) == 1:
            ChooseData = list(Pet_SuperRewardData.objects.all())
        elif int(request.POST.get('Type')) == 2:
            ChooseData = list(Pet_RareRewardData.objects.all())
        else:
            ChooseData = list(Pet_NormalRewardData.objects.all())

        # 랜덤으로 하나 추출.
        selectData = random.choice(ChooseData)

        recordData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if petCostData.CostType == 1:
            moneyData.GoldValue = moneyData.GoldValue - petCostData.CostValue
            moneyData.save()
            # record에 기록...
            recordData.TotalUseGold = recordData.TotalUseGold + petCostData.CostValue
            recordData.save()
        elif petCostData.CostType == 2:
            moneyData.CashValue = moneyData.CashValue - petCostData.CostValue
            moneyData.save()
        SendData = {}
        if selectData.Type == 1:
            # 뽑은 펫을 가지구있는지 체크해서 없으면 펙 생성 있으면, 골드로 보상.
            if PetData.objects.filter(UserSN = request.POST.get('SN'), PetSN = selectData.Value).count() == 0:
                # 펫 생성.
                pet = PetData()
                pet.PetSN = selectData.Value
                pet.UserSN = request.POST.get('SN')
                pet.Grade = Grade
                pet.save()

                SendData['CostType'] = petCostData.CostType
                SendData['Cost'] = petCostData.CostValue
                SendData['RewardType'] = selectData.Type
                SendData['RewardValue'] = selectData.Value
                SendData['RewardGrade'] = Grade

                return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
            else:
                # 같은 펫이 존재하여 골드로 보상.
                if int(request.POST.get('Type')) == 1:
                    ChooseData = list(Pet_SuperRewardData.objects.filter(Type = 2).order_by('-Value'))
                elif int(request.POST.get('Type')) == 2:
                    ChooseData = list(Pet_RareRewardData.objects.filter(Type = 2).order_by('-Value'))
                else:
                    ChooseData = list(Pet_NormalRewardData.objects.filter(Type = 2).order_by('-Value'))

                gold = ChooseData[0].Value

                moneyData.GoldValue = moneyData.GoldValue + gold
                moneyData.save()

                SendData['CostType'] = petCostData.CostType
                SendData['Cost'] = petCostData.CostValue
                SendData['RewardType'] = 2
                SendData['RewardValue'] = gold
                return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
        else:
            # 골드로 보상.
            moneyData.GoldValue = moneyData.GoldValue + selectData.Value
            moneyData.save()

            SendData['CostType'] = petCostData.CostType
            SendData['Cost'] = petCostData.CostValue
            SendData['RewardType'] = selectData.Type
            SendData['RewardValue'] = selectData.Value
            return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    else:
        data = {
            'ErrorCode' : '106',
            'Message' : 'Lack of Cost',
            'CostType' : petCostData.CostType,
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

#-------------------------------------------------------------------------------

# 탈것 구매처리.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
VehicleSN = 탈것SN.

리턴값
SendData['VehicleSN'] = Vehicle SN
SendData['CostType'] = 구매타입 (1 : 코인, 2 : 캐쉬)
SendData['Cost'] = 구매가.
SendData['Count'] = 수량.

"""
@csrf_exempt
def BuyVehicle(request):
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

    elif not request.POST.get('VehicleSN'):
        data = {
            'ErrorCode' : '103',
            'Message' : 'VehicleSN does not exist',
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

    # 가격 비교.
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    vehicleData = list(Shop_VehicleData.objects.filter(id = request.POST.get('VehicleSN')))[0]
    if (vehicleData.CostType == 1 and vehicleData.Cost <= moneyData.GoldValue) or (vehicleData.CostType == 2 and vehicleData.Cost <= moneyData.CashValue):
        # 탈것 생성.
        Vehicle = VehicleData()
        Vehicle.VehicleSN = vehicleData.id
        Vehicle.UserSN = request.POST.get('SN')
        Vehicle.Level = 1
        Vehicle.save()

        recordData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if vehicleData.CostType == 1:
            moneyData.GoldValue = moneyData.GoldValue - vehicleData.Cost
            moneyData.save()
            # record에 기록...
            recordData.TotalUseGold = recordData.TotalUseGold + vehicleData.Cost
            recordData.save()
        elif vehicleData.CostType == 2:
            moneyData.CashValue = moneyData.CashValue - vehicleData.Cost
            moneyData.save()

        SendData = {}
        SendData['VehicleSN'] = vehicleData.id
        SendData['CostType'] = vehicleData.CostType
        SendData['Cost'] = vehicleData.Cost
        SendData['Count'] = vehicleData.Value

        return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    else:
        data = {
            'ErrorCode' : '106',
            'Message' : 'Lack of Cost',
            'CostType' : vehicleData.CostType,
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


#-------------------------------------------------------------------------------

# 아이템 구매처리.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
ItemSN = ItemSN.

리턴값
SendData['ItemSN'] = ItemSN
SendData['CostType'] = 구매타입 (1 : 코인, 2 : 캐쉬)
SendData['Cost'] = 구매가.
SendData['Count'] = 수량.

"""
@csrf_exempt
def BuyItem(request):
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

    elif not request.POST.get('ItemSN'):
        data = {
            'ErrorCode' : '105',
            'Message' : 'ItemSN does not exist',
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

    # 가격 비교.
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    itemData = list(Shop_ItemData.objects.filter(id = request.POST.get('ItemSN')))[0]
    if (itemData.CostType == 1 and itemData.Cost <= moneyData.GoldValue) or (itemData.CostType == 2 and itemData.Cost <= moneyData.CashValue):

        item = ''
        value = 0
        itemList = list(ItemData.objects.filter(UserSN = request.POST.get('SN')))
        IsBuy = True
        if len(itemList) > 0:
            # 아이템이 존재하면 수량 증가.
            for data in itemList:
                if data.ItemSN == itemData.id:
                    item = data
                    item.Value = item.Value + itemData.Value
                    item.save()
                    IsBuy = False
                    value = item.Value
                    break

        if IsBuy == True:
            # 아이템 생성.
            item = ItemData()
            item.ItemSN = request.POST.get('ItemSN')
            item.UserSN = request.POST.get('SN')
            item.Value = itemData.Value
            item.save()
            value = item.Value

        recordData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if itemData.CostType == 1:
            moneyData.GoldValue = moneyData.GoldValue - itemData.Cost
            moneyData.save()
            # record에 기록...
            recordData.TotalUseGold = recordData.TotalUseGold + itemData.Cost
            if item.ItemSN == 1:
                recordData.Item_1 = recordData.Item_1 + 1
            elif item.ItemSN == 2:
                recordData.Item_2 = recordData.Item_2 + 1
            elif item.ItemSN == 3:
                recordData.Item_3 = recordData.Item_3 + 1
            elif item.ItemSN == 4:
                recordData.Item_4 = recordData.Item_4 + 1
            elif item.ItemSN == 5:
                recordData.Item_5 = recordData.Item_5 + 1
            recordData.save()
        elif itemData.CostType == 2:
            moneyData.CashValue = moneyData.CashValue - itemData.Cost
            moneyData.save()

        SendData = {}
        SendData['ItemSN'] = itemData.id
        SendData['CostType'] = itemData.CostType
        SendData['Cost'] = itemData.Cost
        SendData['Count'] = value

        return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    else:
        data = {
            'ErrorCode' : '106',
            'Message' : 'Lack of Cost',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


#-------------------------------------------------------------------------------

# 토큰 구매처리.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
TokenSN = 토큰SN.

리턴값
SendData['TokenSN'] = TokenSN
SendData['CostType'] = 구매타입 (1 : 코인, 2 : 캐쉬)
SendData['Cost'] = 구매가.
SendData['Count'] = 수량.

"""
@csrf_exempt
def BuyToken(request):
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

    elif not request.POST.get('TokenSN'):
        data = {
            'ErrorCode' : '103',
            'Message' : 'TokenSN does not exist',
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

    # 가격 비교.
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    tokenData = list(Shop_TokenData.objects.filter(id = request.POST.get('TokenSN')))[0]
    if (tokenData.CostType == 1 and tokenData.Cost <= moneyData.GoldValue) or (tokenData.CostType == 2 and tokenData.Cost <= moneyData.CashValue):
        # 토큰 수량 증가.
        tokenList = list(TokenData.objects.filter(UserSN = request.POST.get('SN')))
        if len(tokenList) > 0:
            token = tokenList[0]
            token.ToeknValue = token.ToeknValue + tokenData.Value
            token.save()

        recordData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if tokenData.CostType == 1:
            moneyData.GoldValue = moneyData.GoldValue - tokenData.Cost
            moneyData.save()
            # record에 기록...
            recordData.TotalUseGold = recordData.TotalUseGold + tokenData.Cost
            recordData.save()
        elif tokenData.CostType == 2:
            moneyData.CashValue = moneyData.CashValue - tokenData.Cost
            moneyData.save()

        SendData = {}
        SendData['TokenSN'] = tokenData.id
        SendData['CostType'] = tokenData.CostType
        SendData['Cost'] = tokenData.Cost
        SendData['Count'] = tokenList[0].ToeknValue

        return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    else:
        data = {
            'ErrorCode' : '106',
            'Message' : 'Lack of Cost',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


#-------------------------------------------------------------------------------

# 골드 구매처리.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
GoldSN = GoldSN.

리턴값
SendData['Cost'] = 구매가.
SendData['Value'] = 수량.

"""
@csrf_exempt
def BuyGold(request):
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

    elif not request.POST.get('GoldSN'):
        data = {
            'ErrorCode' : '103',
            'Message' : 'GoldSN does not exist',
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

    # 가격 비교.
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    goldData = list(Shop_GoldData.objects.filter(id = request.POST.get('GoldSN')))[0]
    if (goldData.Cost <= moneyData.CashValue):

        # record에 기록...
        recordData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
        recordData.TotalGold = recordData.TotalGold + goldData.Value
        recordData.save()
        moneyData.GoldValue = moneyData.GoldValue + goldData.Value
        moneyData.CashValue = moneyData.CashValue - goldData.Cost
        moneyData.save()

        SendData = {}
        SendData['Cost'] = goldData.Cost
        SendData['Value'] = goldData.Value

        return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    else:
        data = {
            'ErrorCode' : '106',
            'Message' : 'Lack of Cost',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


#-------------------------------------------------------------------------------

# 캐쉬 구매처리.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
CashSN = CashSN.

리턴값
SendData['Value'] = 수량.

"""
@csrf_exempt
def BuyCash(request):
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

    elif not request.POST.get('CashSN'):
        data = {
            'ErrorCode' : '103',
            'Message' : 'CashSN does not exist',
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

    # 가격 비교.
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    cashData = list(Shop_CashData.objects.filter(id = request.POST.get('CashSN')))[0]

    moneyData.CashValue = moneyData.CashValue + cashData.Value
    moneyData.save()

    SendData = {}
    SendData['Value'] = cashData.Value

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 토큰 가져오기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
SendData['Value'] = 수량.
SendData['Time'] = 토큰 채울시간.
"""
@csrf_exempt
def TokenDataResponse(request):
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

    token = TokenData.objects.filter(UserSN = request.POST.get('SN'))[0]
    SendData = {}
    SendData['Value'] = token.ToeknValue
    SendData['Time'] = myUtil.ToLastSec(token.CreateTime)

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 토큰값 변경하기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
Token = 토큰수.
리턴값
SendData['Value'] = 수량.
SendData['Time'] = 토큰 채울시간.
"""
@csrf_exempt
def ChangeToken(request):
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

    token = TokenData.objects.filter(UserSN = request.POST.get('SN'))[0]
    token.ToeknValue = request.POST.get('Token')
    token.CreateTime = myUtil.NowTime()
    token.save()

    SendData = {}
    SendData['Value'] = token.ToeknValue
    SendData['Time'] = myUtil.ToLastSec(token.CreateTime)

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')



#-------------------------------------------------------------------------------

# 토큰사용.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
SendData['Value'] = 수량.
SendData['Time'] = 토큰 채울시간.
"""
@csrf_exempt
def UseToken(request):
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

    token = TokenData.objects.filter(UserSN = request.POST.get('SN'))[0]
    SendData = {}
    if token.ToeknValue > 0:
        token.ToeknValue = token.ToeknValue - 1
        token.CreateTime = myUtil.NowTime()
        token.save()

        SendData['Value'] = token.ToeknValue
        SendData['Time'] = myUtil.ToLastSec(token.CreateTime)
    else:
        SendData = {
            'ErrorCode' : '106',
            'Message' : 'Lack of tokens',
        }

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 아이템사용.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
ItemSN = 아이템sn.

리턴값
SendData['ItemSN'] = 아이템SN.
SendData['Value'] = 수량.
"""
@csrf_exempt
def UseItem(request):
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

    elif not request.POST.get('ItemSN'):
        data = {
            'ErrorCode' : '105',
            'Message' : 'ItemSN does not exist',
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

    itemList = list(ItemData.objects.filter(UserSN = request.POST.get('SN'), ItemSN = request.POST.get('ItemSN')))
    SendData = {}
    if len(itemList) > 0 and itemList[0].Value > 0:
        itemData = itemList[0]
        itemData.Value = itemData.Value - 1
        itemData.save()
        SendData['ItemSN'] = itemData.id
        SendData['Value'] = itemData.Value

        if itemData.Value <= 0:
            itemData.delete()
    else:
        SendData = {
            'ErrorCode' : '106',
            'Message' : 'Lack of item',
        }

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')

#-------------------------------------------------------------------------------

# 일일출석체크.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
Reward = 보상 받을 여부.
"""
@csrf_exempt
def DailyCheck(request):
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
    dataList = list(DailyCheckData.objects.filter(UserSN = request.POST.get('SN')))
    moneyData = MoneyData.objects.filter(UserSN = request.POST.get('SN'))[0]
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
        dayData.UserSN = request.POST.get('SN')
        dayData.CheckTime = date.today()
        dayData.save()
        SendData['Reward'] = False

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 결과 업데이트.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
GameMode = 게임모드 (1 : 무한, 2 : 타임어택)
Distance = 거리.
Score = 점수.
Coin = 코인수.
CharacterSN = 캐릭터
Pet1SN = 펫
Pet2SN = 펫
VehicleSN = 탈것.
IsGoldDouble = 골드더블 여부. (1 : true, 0 : false)

리턴값
SendData['Gold'] = 획득 골드.
SendData['Best'] = 베스트 점수 갱신 여부.
SendData['BestScore'] = 베스트 점수.
SendData['Rank'] = 변경된 랭킹.
"""
@csrf_exempt
def ResultUpdate(request):
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

    elif not request.POST.get('GameMode'):
        data = {
            'ErrorCode' : '103',
            'Message' : 'GameMode does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('Score'):
        data = {
            'ErrorCode' : '104',
            'Message' : 'Score does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('Coin'):
        data = {
            'ErrorCode' : '105',
            'Message' : 'Coin does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('Distance'):
        data = {
            'ErrorCode' : '106',
            'Message' : 'Distance does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('CharacterSN'):
        data = {
            'ErrorCode' : '109',
            'Message' : 'CharacterSN does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('Pet1SN'):
        data = {
            'ErrorCode' : '110',
            'Message' : 'Pet1SN does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('Pet2SN'):
        data = {
            'ErrorCode' : '111',
            'Message' : 'Pet2SN does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('VehicleSN'):
        data = {
            'ErrorCode' : '112',
            'Message' : 'VehicleSN does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('IsGoldDouble'):
        data = {
            'ErrorCode' : '113',
            'Message' : 'IsGoldDouble does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    user = list(UserData.objects.filter(id = request.POST.get('SN')))
    if len(user) == 0:
        data = {
            'ErrorCode' : '107',
            'Message' : 'UserData does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    user = user[0]
    if user.Auth != request.POST.get('Auth'):
        data = {
            'ErrorCode' : '108',
            'Message' : 'Auth is invalid.',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    # 결과 처리.
    IsGoldDouble = int(request.POST.get('IsGoldDouble'))
    playData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
    coin = int(request.POST.get('Coin'))
    dis = int(request.POST.get('Distance'))
    score = int(request.POST.get('Score'))
    playData.TotalGetCoin = playData.TotalGetCoin + coin
    if playData.BestGetCoin < coin:
        playData.BestGetCoin = coin
    playData.TotalDistance = playData.TotalDistance + dis
    if playData.BestDistance < dis:
        playData.BestDistance = dis
    playData.TotalScore = playData.TotalScore + score
    best = False
    if playData.BestScore < score:
        playData.BestScore = score
        best = True

    # 코인을 골드로 환산.
    goldValue = int(coin  / 1000)
    if IsGoldDouble == 1:
        goldValue = goldValue * 2

    playData.TotalGold = playData.TotalGold + goldValue

    playData.TotalPlay = playData.TotalPlay + 1
    playData.save()

    # 골드처리
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    moneyData.GoldValue = moneyData.GoldValue + goldValue
    moneyData.save()

    BestScore = 0
    Rank = 0
    ChickenScore = 0
    # 점수 셋팅.
    if int(request.POST.get('GameMode')) == 1:
        # 친구주간.
        rankData = list(InfiniteFriendWeekRankData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if rankData.Score < score:
            rankData.CharacterSN = int(request.POST.get('CharacterSN'))
            rankData.Pet1SN = int(request.POST.get('Pet1SN'))
            rankData.Pet2SN = int(request.POST.get('Pet2SN'))
            rankData.VehicleSN = int(request.POST.get('VehicleSN'))
            best = True
            rankData.Score = score
            rankData.save()
        BestScore = rankData.Score

        # 변경된 순위 찾기.
        friendList = []
        for friendData in list(FriendData.objects.filter(UserSN = request.POST.get('SN'))):
            friendList.append(friendData.FriendSN)

        for rankData in list(InfiniteFriendWeekRankData.objects.order_by('-Score')):
            if rankData.UserSN in friendList or rankData.UserSN == int(request.POST.get('SN')):
                Rank = Rank + 1
                if rankData.UserSN == int(request.POST.get('SN')):
                    break

        # 주간.
        rankData = list(InfiniteWeekRankData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if rankData.Score < score:
            rankData.CharacterSN = int(request.POST.get('CharacterSN'))
            rankData.Pet1SN = int(request.POST.get('Pet1SN'))
            rankData.Pet2SN = int(request.POST.get('Pet2SN'))
            rankData.VehicleSN = int(request.POST.get('VehicleSN'))
            best = True
            rankData.Score = score
            rankData.save()
        BestScore = rankData.Score
        # 월간...
        rankData = list(InfiniteMonthRankData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if rankData.Score < score:
            rankData.CharacterSN = int(request.POST.get('CharacterSN'))
            rankData.Pet1SN = int(request.POST.get('Pet1SN'))
            rankData.Pet2SN = int(request.POST.get('Pet2SN'))
            rankData.VehicleSN = int(request.POST.get('VehicleSN'))
            best = True
            rankData.Score = score
            rankData.save()
        BestScore = rankData.Score
    else:
        # 친구 주간.
        rankData = list(TimeAttackFriendWeekRankData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if rankData.Score < score:
            rankData.CharacterSN = int(request.POST.get('CharacterSN'))
            rankData.Pet1SN = int(request.POST.get('Pet1SN'))
            rankData.Pet2SN = int(request.POST.get('Pet2SN'))
            rankData.VehicleSN = int(request.POST.get('VehicleSN'))
            best = True
            rankData.Score = score
            rankData.save()
        BestScore = rankData.Score

        # 변경된 순위 찾기.
        friendList = []
        for friendData in list(FriendData.objects.filter(UserSN = request.POST.get('SN'))):
            friendList.append(friendData.FriendSN)

        for rankData in list(TimeAttackFriendWeekRankData.objects.order_by('-Score')):
            if rankData.UserSN in friendList or rankData.UserSN == int(request.POST.get('SN')):
                Rank = Rank + 1
                if rankData.UserSN == int(request.POST.get('SN')):
                    break

        # 주간.
        rankData = list(TimeAttackWeekRankData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if rankData.Score < score:
            rankData.CharacterSN = int(request.POST.get('CharacterSN'))
            rankData.Pet1SN = int(request.POST.get('Pet1SN'))
            rankData.Pet2SN = int(request.POST.get('Pet2SN'))
            rankData.VehicleSN = int(request.POST.get('VehicleSN'))
            best = True
            rankData.Score = score
            rankData.save()
        BestScore = rankData.Score
        # 월간...
        rankData = list(TimeAttackMonthRankData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if rankData.Score < score:
            rankData.CharacterSN = int(request.POST.get('CharacterSN'))
            rankData.Pet1SN = int(request.POST.get('Pet1SN'))
            rankData.Pet2SN = int(request.POST.get('Pet2SN'))
            rankData.VehicleSN = int(request.POST.get('VehicleSN'))
            best = True
            rankData.Score = score
            rankData.save()
        BestScore = rankData.Score

    SendData = {}
    SendData['Gold'] = goldValue
    SendData['Best'] = best
    SendData['BestScore'] = BestScore
    SendData['Rank'] = Rank

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 치킨 점수 보상.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
SendData['Type'] = 1 : 골드, 2 : 캐쉬, 3 : 아이템.
SendData['ItemSN'] = 아이템SN.
SendData['Value'] = 수량.

"""
@csrf_exempt
def ChickenScoreReward(request):
    import random
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
    moneyData = MoneyData.objects.filter(UserSN = request.POST.get('SN'))[0]
    dataList = list(ChickenScoreReward.objects.all())
    # 랜덤으로 하나 추출.
    selectData = random.choice(dataList)
    if selectData.Type == 1:
        moneyData.GoldValue = moneyData.GoldValue + selectData.Value
        moneyData.save()

        # record에 기록...
        recordData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
        recordData.TotalGold = recordData.TotalGold + selectData.Value
        recordData.save()

        SendData['Type'] = selectData.Type
        SendData['ItemSN'] = selectData.ItemSN
        SendData['Value'] = selectData.Value
    elif selectData.Type == 2:
        moneyData.CashValue = moneyData.CashValue + selectData.Value
        moneyData.save()
        SendData['Type'] = selectData.Type
        SendData['ItemSN'] = selectData.ItemSN
        SendData['Value'] = selectData.Value
    elif selectData.Type == 3:
        myItem = list(ItemData.objects.filter(UserSN = request.POST.get('SN'), ItemSN = selectData.ItemSN))
        if len(myItem) > 0:
            myItem[0].Value = myItem[0].Value + selectData.Value
            myItem[0].save()
        else:
            itemdata = ItemData(UserSN = request.POST.get('SN'), ItemSN = selectData.ItemSN, Value = selectData.Value)
            itemdata.save()

        data['Type'] = selectData.Type
        data['ItemSN'] = selectData.ItemSN
        data['Value'] = selectData.Value

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')



#-------------------------------------------------------------------------------

# 탈퇴 처리.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
Result = 결과.. true : 성공, false : 실패.

"""
@csrf_exempt
def WithdrawalResponse(request):
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
    SendData['Result'] = True

    UserData.objects.filter(id = request.POST.get('SN')).delete()
    CharacterData.objects.filter(UserSN = request.POST.get('SN')).delete()
    CurrPlayData.objects.filter(UserSN = request.POST.get('SN')).delete()
    PetData.objects.filter(UserSN = request.POST.get('SN')).delete()
    VehicleData.objects.filter(UserSN = request.POST.get('SN')).delete()
    PlayRecordData.objects.filter(UserSN = request.POST.get('SN')).delete()
    MoneyData.objects.filter(UserSN = request.POST.get('SN')).delete()
    ItemData.objects.filter(UserSN = request.POST.get('SN')).delete()
    TokenData.objects.filter(UserSN = request.POST.get('SN')).delete()
    DailyCheckData.objects.filter(UserSN = request.POST.get('SN')).delete()
    ChickenScoreRewardData.objects.filter(UserSN = request.POST.get('SN')).delete()
    BestRecodData.objects.filter(UserSN = request.POST.get('SN')).delete()
    ChickenRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    InfiniteFriendLastWeekRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    InfiniteFriendWeekRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    InfiniteLastWeekRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    InfiniteWeekRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    TimeAttackFriendLastWeekRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    TimeAttackFriendWeekRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    TimeAttackLastWeekRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    TimeAttackWeekRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    InfiniteLastMonthRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    InfiniteMonthRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    TimeAttackLastMonthRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    TimeAttackMonthRankData.objects.filter(UserSN = request.POST.get('SN')).delete()
    TokenMessage.objects.filter(UserSN = request.POST.get('SN')).delete()
    GiftMessage.objects.filter(UserSN = request.POST.get('SN')).delete()
    TokenReceiveData.objects.filter(UserSN = request.POST.get('SN')).delete()
    FriendData.objects.filter(UserSN = request.POST.get('SN')).delete()
    KakaoInviteData.objects.filter(UserSN = request.POST.get('SN')).delete()

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------

# 탈것 업그레이드.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
VehicleSN = 탈것 SN.

리턴값
SendData['VehicleSN'] = 탈것 SN.
SendData['Cost'] = 업그레이드 가격.
SendData['Level'] = 업글후 레벨.
"""
@csrf_exempt
def VehicleUpgrade(request):
    import random
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

    elif not request.POST.get('VehicleSN'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'VehicleSN does not exist',
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
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    vehicleData = list(VehicleData.objects.filter(UserSN = request.POST.get('SN'), VehicleSN = request.POST.get('VehicleSN')))[0]
    vehicleShopData = list(VehicleUpgradeData.objects.filter(id = request.POST.get('VehicleSN')))[0]
    costValue = (vehicleData.Level * vehicleShopData.Cost)
    IsMaxLevel = False

    if vehicleData.Level >= vehicleShopData.MaxLevel:
        IsMaxLevel = True

    if IsMaxLevel:
        data = {
            'ErrorCode' : '107',
            'Message' : 'Level limit',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    if costValue <= moneyData.GoldValue:
        moneyData.GoldValue = moneyData.GoldValue - costValue
        moneyData.save()
        # record에 기록...
        recordData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
        recordData.TotalUseGold = recordData.TotalUseGold + costValue
        recordData.save()

        vehicleData.Level = vehicleData.Level + 1
        vehicleData.save()

        SendData = {}
        SendData['VehicleSN'] = vehicleData.VehicleSN
        SendData['Cost'] = costValue
        SendData['Level'] = vehicleData.Level

        return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    else:
        data = {
            'ErrorCode' : '106',
            'Message' : 'Lack of Cost',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


#-------------------------------------------------------------------------------

# 캐릭터 업그레이드.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
CharSN = 캐릭터 SN.
Type = 업그레이드 타입.

리턴값
SendData['CharSN'] = 캐릭터 SN.
Type = 업그레이드 타입.
SendData['Cost'] = 업그레이드 가격.
SendData['Level'] = 업글후 레벨.
"""
@csrf_exempt
def CharacterUpgrade(request):
    import random
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

    elif not request.POST.get('CharSN'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'CharSN does not exist',
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
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    charData = list(CharacterData.objects.filter(UserSN = request.POST.get('SN'), CharacterSN = request.POST.get('CharSN')))[0]
    charShopData = list(CharacterUpgradeData.objects.filter(id = request.POST.get('CharSN')))[0]
    costValue = 0
    IsMaxLevel = False

    if int(request.POST.get('Type')) == 1:
        if charData.Level_HP >= charShopData.HPLevel:
            IsMaxLevel = True
        costValue = charData.Level_HP * charShopData.HPCost
    elif int(request.POST.get('Type')) == 2:
        if charData.Level_GodDash >= charShopData.GodDashLevel:
            IsMaxLevel = True
        costValue = charData.Level_GodDash * charShopData.GodDashCost
    elif int(request.POST.get('Type')) == 3:
        if charData.Level_Magnet >= charShopData.MagnetLevel:
            IsMaxLevel = True
        costValue = charData.Level_Magnet * charShopData.MagnetCost
    elif int(request.POST.get('Type')) == 4:
        if charData.Level_Shield >= charShopData.ShieldLevel:
            IsMaxLevel = True
        costValue = charData.Level_Shield * charShopData.ShieldCost
    elif int(request.POST.get('Type')) == 5:
        if charData.Level_Big >= charShopData.BigLevel:
            IsMaxLevel = True
        costValue = charData.Level_Big * charShopData.BigCost
    elif int(request.POST.get('Type')) == 6:
        if charData.Level_Small >= charShopData.SmallLevel:
            IsMaxLevel = True
        costValue = charData.Level_Small * charShopData.SmallCost

    if IsMaxLevel:
        data = {
            'ErrorCode' : '107',
            'Message' : 'Level limit',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    if costValue <= moneyData.GoldValue:
        moneyData.GoldValue = moneyData.GoldValue - costValue
        moneyData.save()
        # record에 기록...
        recordData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
        recordData.TotalUseGold = recordData.TotalUseGold + costValue
        recordData.save()
        Level = 0
        if int(request.POST.get('Type')) == 1:
            charData.Level_HP = charData.Level_HP + 1
            Level = charData.Level_HP
        elif int(request.POST.get('Type')) == 2:
            charData.Level_GodDash = charData.Level_GodDash + 1
            Level = charData.Level_GodDash
        elif int(request.POST.get('Type')) == 3:
            charData.Level_Magnet = charData.Level_Magnet + 1
            Level = charData.Level_Magnet
        elif int(request.POST.get('Type')) == 4:
            charData.Level_Shield = charData.Level_Shield + 1
            Level = charData.Level_Shield
        elif int(request.POST.get('Type')) == 5:
            charData.Level_Big = charData.Level_Big + 1
            Level = charData.Level_Big
        elif int(request.POST.get('Type')) == 6:
            charData.Level_Small = charData.Level_Small + 1
            Level = charData.Level_Small

        charData.save()

        SendData = {}
        SendData['CharSN'] = charData.CharacterSN
        SendData['Cost'] = costValue
        SendData['Type'] = request.POST.get('Type')
        SendData['Level'] = Level

        return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    else:
        data = {
            'ErrorCode' : '106',
            'Message' : 'Lack of Cost',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


#-------------------------------------------------------------------------------

# 펫 슬롯 구매.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
SendData['CostType'] = 구매타입 (1 : 코인, 2 : 캐쉬)
SendData['Cost'] = 구매가.
"""
@csrf_exempt
def BuyPetSlot(request):
    import random
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

    # 가격 비교.
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    # 타입 99는 펫슬롯 가격...
    petCostData = list(Shop_PetData.objects.filter(Type = '99'))[0]

    if (petCostData.CostType == 1 and petCostData.CostValue <= moneyData.GoldValue) or (petCostData.CostType == 2 and petCostData.CostValue <= moneyData.CashValue):
        recordData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
        if petCostData.CostType == 1:
            moneyData.GoldValue = moneyData.GoldValue - petCostData.CostValue
            moneyData.save()
            # record에 기록...
            recordData.TotalUseGold = recordData.TotalUseGold + petCostData.CostValue
            recordData.save()
        elif petCostData.CostType == 2:
            moneyData.CashValue = moneyData.CashValue - petCostData.CostValue
            moneyData.save()

        currData = list(CurrPlayData.objects.filter(UserSN = request.POST.get('SN')))[0]
        currData.Pet2SN = 0
        currData.save()

        SendData = {}
        SendData['CostType'] = petCostData.CostType
        SendData['Cost'] = petCostData.CostValue
        return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    else:
        data = {
            'ErrorCode' : '106',
            'Message' : 'Lack of Cost',
            'CostType' : petCostData.CostType,
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')


#-------------------------------------------------------------------------------

# 이어하기.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.

리턴값
SendData['Cost'] = 구매가.
"""
@csrf_exempt
def RelayCheck(request):
    import random
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

    # 가격 비교.
    moneyData = list(MoneyData.objects.filter(UserSN = request.POST.get('SN')))[0]
    # 이어하기 가격...
    costValue = 300
    if costValue <= moneyData.GoldValue:
        recordData = list(PlayRecordData.objects.filter(UserSN = request.POST.get('SN')))[0]
        moneyData.GoldValue = moneyData.GoldValue - costValue
        moneyData.save()
        # record에 기록...
        recordData.TotalUseGold = recordData.TotalUseGold + costValue
        recordData.save()

        SendData = {}
        SendData['Cost'] = costValue
        return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    else:
        data = {
            'ErrorCode' : '106',
            'Message' : 'Lack of Cost',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')



#-------------------------------------------------------------------------------

# 최근 상태 저장.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
GameMode = 1 : 멀리가기, 2 : 타임어택.
CharSN = 캐릭터SN.
VehicleSN = 탈것SN.
Pet1SN = 펫1 SN.
Pet2SN = 펫2 SN.

리턴값
SendData['Cost'] = 구매가.
"""
@csrf_exempt
def CurrDataUpdate(request):
    import random
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

    elif not request.POST.get('GameMode'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'GameMode does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('CharSN'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'CharSN does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('VehicleSN'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'VehicleSN does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('Pet1SN'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'Pet1SN does not exist',
        }
        return HttpResponse(myUtil.JsonPaser(data), content_type='application/json')

    elif not request.POST.get('Pet2SN'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'Pet2SN does not exist',
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

    currData = list(CurrPlayData.objects.filter(UserSN = request.POST.get('SN')))[0]
    currData.GameMode = request.POST.get('GameMode')
    currData.CharacterSN = request.POST.get('CharSN')
    currData.VehicleSN = request.POST.get('VehicleSN')
    currData.Pet1SN = request.POST.get('Pet1SN')
    currData.Pet2SN = request.POST.get('Pet2SN')
    currData.save()

    # SendData = {}
    # SendData['GameMode'] = currData.GameMode
    # SendData['CharSN'] = currData.CharSN
    # SendData['VehicleSN'] = currData.VehicleSN
    # SendData['Pet1SN'] = currData.Pet1SN
    # SendData['Pet2SN'] = currData.Pet2SN

    # return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
    return HttpResponse('', content_type='application/json')

#-------------------------------------------------------------------------------

# 치킨 점수 업데이트.
"""
호출 값
SN = 유저SN.
Auth = 인증 토큰.
ChickenScore = 획득한 치킨 점수.

리턴값
SendData['ChickenScore'] = 총 치킨 점수.
"""
@csrf_exempt
def ChickenScoreUpdate(request):
    import random
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

    elif not request.POST.get('ChickenScore'):
        data = {
            'ErrorCode' : '102',
            'Message' : 'ChickenScore does not exist',
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

    score = list(ChickenScoreRewardData.objects.filter(UserSN = request.POST.get('SN')))[0]
    score.Score = score.Score + int(request.POST.get('ChickenScore'))
    score.save()

    SendData = {}
    SendData['ChickenScore'] = score.Score

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')
