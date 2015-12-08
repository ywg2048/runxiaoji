# -*- coding: utf-8 -*-
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from ShopData.models import *
from users.models import UserData
from datetime import *
import myUtil


# 상점가격 데이터 가져오기.
"""
호출 값

리턴값.
TokenData
    SN = 고유번호.
    CostType = 구매타입 (1 : 골드, 2 : 캐쉬).
    Cost = 가격.
    Value = 수량.
GoldData
    SN = 고유번호.
    CostType = 구매타입 (1 : 골드, 2 : 캐쉬).
    Cost = 가격.
    Value = 수량.
CashData
    SN = 고유번호.
    Value = 수량.
ItemData
    SN = 고유번호.
    CostType = 구매타입 (1 : 골드, 2 : 캐쉬).
    Cost = 가격.
    Value = 수량.
CharData
    SN = 고유번호.
    CostType = 구매타입 (1 : 골드, 2 : 캐쉬).
    Cost = 가격.
    Value = 수량.
VehicleData
    SN = 고유번호.
    CostType = 구매타입 (1 : 골드, 2 : 캐쉬).
    Cost = 가격.
    Value = 수량.
PetData
    SN = 고유번호.
    CostType = 구매타입 (1 : 골드, 2 : 캐쉬).
    Type = 뽑기 타입 (1 : 슈퍼, 2 : 레어, 3 : 노말).
    CostValue = 가격.

CharUpgradeData
    SN = 고유번호.
    HPCost = 체력가격.
    HPLevel = 체력 레벨 제한.
    GodDashCost = 무적질주 가격.
    GodDashLevel = 무적질주 레벨 제한.
    MagnetCost = 자석 가격.
    MagnetLevel = 자석 레벨 제한.
    ShieldCost = 쉴드 가격.
    ShieldLevel = 쉴드 레벨 제한.
    BigCost = 확대 가격.
    BigLevel = 확대 레벨 제한.
    SmallCost = 축소 가격.
    SmallLevel = 체력 레벨 제한.

VehicleUpgradeData
    SN = 고유번호.
    Cost = 가격.
    MaxLevel = 레벨 제한.

"""
@csrf_exempt
def ShopDataResponse(request):
    # 결과 처리.
    SendData = {}

    tokenList = list(Shop_TokenData.objects.all())
    tokenData = []
    for token in tokenList:
        data = {}
        data['SN'] = token.id
        data['CostType'] = token.CostType
        data['Cost'] = token.Cost
        data['Value'] = token.Value
        tokenData.append(data)

    SendData['TokenData'] = tokenData

    goldList = list(Shop_GoldData.objects.all())
    goldData = []
    for gold in goldList:
        data = {}
        data['SN'] = gold.id
        data['CostType'] = gold.CostType
        data['Cost'] = gold.Cost
        data['Value'] = gold.Value
        goldData.append(data)

    SendData['GoldData'] = goldData

    cashList = list(Shop_CashData.objects.all())
    cashData = []
    for cash in cashList:
        data = {}
        data['SN'] = cash.id
        data['Value'] = cash.Value
        cashData.append(data)

    SendData['CashData'] = cashData

    itemList = list(Shop_ItemData.objects.all())
    itemData = []
    for item in itemList:
        data = {}
        data['SN'] = item.id
        data['CostType'] = item.CostType
        data['Cost'] = item.Cost
        data['Value'] = item.Value
        itemData.append(data)

    SendData['ItemData'] = itemData

    charList = list(Shop_CharacterData.objects.all())
    charData = []
    for char in charList:
        data = {}
        data['SN'] = char.id
        data['CostType'] = char.CostType
        data['Cost'] = char.Cost
        data['Value'] = char.Value
        charData.append(data)

    SendData['CharData'] = charData

    vehicleList = list(Shop_VehicleData.objects.all())
    vehicleData = []
    for vehicle in vehicleList:
        data = {}
        data['SN'] = vehicle.id
        data['CostType'] = vehicle.CostType
        data['Cost'] = vehicle.Cost
        data['Value'] = vehicle.Value
        vehicleData.append(data)

    SendData['VehicleData'] = vehicleData

    petList = list(Shop_PetData.objects.all())
    petData = []
    for pet in petList:
        data = {}
        data['SN'] = pet.id
        data['CostType'] = pet.CostType
        data['Type'] = pet.Type
        data['CostValue'] = pet.CostValue
        petData.append(data)

    SendData['PetData'] = petData

    charUpgradeList = list(CharacterUpgradeData.objects.all())
    charUpgradeData = []
    for charUpgrade in charUpgradeList:
        data = {}
        data['SN'] = charUpgrade.id
        data['HPCost'] = charUpgrade.HPCost
        data['HPLevel'] = charUpgrade.HPLevel
        data['HPAddValue'] = charUpgrade.HPAddValue
        data['HPMinValue'] = charUpgrade.HPMinValue
        data['GodDashCost'] = charUpgrade.GodDashCost
        data['GodDashLevel'] = charUpgrade.GodDashLevel
        data['GodAddValue'] = charUpgrade.GodAddValue
        data['GodMinValue'] = charUpgrade.GodMinValue
        data['MagnetCost'] = charUpgrade.MagnetCost
        data['MagnetLevel'] = charUpgrade.MagnetLevel
        data['MagnetAddValue'] = charUpgrade.MagnetAddValue
        data['MagnetMinValue'] = charUpgrade.MagnetMinValue
        data['ShieldCost'] = charUpgrade.ShieldCost
        data['ShieldLevel'] = charUpgrade.ShieldLevel
        data['ShieldAddValue'] = charUpgrade.ShieldAddValue
        data['ShieldMinValue'] = charUpgrade.ShieldMinValue
        data['BigCost'] = charUpgrade.BigCost
        data['BigLevel'] = charUpgrade.BigLevel
        data['BigAddValue'] = charUpgrade.BigAddValue
        data['BigMinValue'] = charUpgrade.BigMinValue
        data['SmallCost'] = charUpgrade.SmallCost
        data['SmallLevel'] = charUpgrade.SmallLevel
        data['SmallAddValue'] = charUpgrade.SmallAddValue
        data['SmallMinValue'] = charUpgrade.SmallMinValue
        charUpgradeData.append(data)

    SendData['CharUpgradeData'] = charUpgradeData

    vehicleUpgradeList = list(VehicleUpgradeData.objects.all())
    vehicleUpgradeData = []
    for vehicleUpgrade in vehicleUpgradeList:
        data = {}
        data['SN'] = vehicleUpgrade.id
        data['Cost'] = vehicleUpgrade.Cost
        data['MaxLevel'] = vehicleUpgrade.MaxLevel
        data['AddValue'] = vehicleUpgrade.AddValue
        data['MinValue'] = vehicleUpgrade.MinValue
        vehicleUpgradeData.append(data)

    SendData['VehicleUpgradeData'] = vehicleUpgradeData

    return HttpResponse(myUtil.JsonPaser(SendData), content_type='application/json')


#-------------------------------------------------------------------------------
