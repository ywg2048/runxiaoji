# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
# Create your models here.

# 구매타입 ( 1 : 코인, 2 : 캐쉬)
# 토큰.
class Shop_TokenData(models.Model):
    # 구매타입.
    CostType = models.IntegerField()
    # 가격.
    Cost = models.IntegerField()
    # 수량.
    Value = models.IntegerField()

class Shop_GoldData(models.Model):
    # 구매타입.
    CostType = models.IntegerField()
    # 가격.
    Cost = models.IntegerField()
    # 수량.
    Value = models.IntegerField()

class Shop_CashData(models.Model):
    # 구매타입.
    CostType = models.IntegerField()
    # 가격.
    Cost = models.IntegerField()
    # 수량.
    Value = models.IntegerField()

    def __str__(self):
        return "%d %d-%d" % (self.id, self.Cost, self.Value)

class Shop_ItemData(models.Model):
    # 구매타입.
    CostType = models.IntegerField()
    # 가격.
    Cost = models.IntegerField()
    # 수량.
    Value = models.IntegerField()

class Shop_CharacterData(models.Model):
    # 구매타입.
    CostType = models.IntegerField()
    # 가격.
    Cost = models.IntegerField()
    # 수량.
    Value = models.IntegerField()

class Shop_VehicleData(models.Model):
    # 구매타입.
    CostType = models.IntegerField()
    # 가격.
    Cost = models.IntegerField()
    # 수량.
    Value = models.IntegerField()

class Shop_PetData(models.Model):
    #뽑기 타입. (1 : 슈퍼, 2 : 레어, 3 : 노멀).
    Type = models.IntegerField()
    # 구매타입.
    CostType = models.IntegerField()
    # 가격.
    CostValue = models.IntegerField()

class Pet_SuperRewardData(models.Model):
    #보상 타입. (1 : 펫, 2 : 골드)
    Type = models.IntegerField()
    #보상값.
    Value = models.IntegerField()

class Pet_RareRewardData(models.Model):
    #보상 타입. (1 : 펫, 2 : 골드)
    Type = models.IntegerField()
    #보상값.
    Value = models.IntegerField()

class Pet_NormalRewardData(models.Model):
    #보상 타입. (1 : 펫, 2 : 골드)
    Type = models.IntegerField()
    #보상값.
    Value = models.IntegerField()

class CharacterUpgradeData(models.Model):
    # 체력.
    HPCost = models.IntegerField()
    # 체력 레벨 제한.
    HPLevel = models.IntegerField()
    # 체력 증가 / 감소치.
    HPAddValue = models.FloatField()
    # 체력 최소 값.
    HPMinValue = models.FloatField()
    # 무적질주.
    GodDashCost = models.IntegerField()
    # 무적질주 레벨 제한.
    GodDashLevel = models.IntegerField()
    # 무적 증가 / 감소치.
    GodAddValue = models.FloatField()
    # 무적 최소 값.
    GodMinValue = models.FloatField()
    # 자석시간.
    MagnetCost = models.IntegerField()
    # 자석 레벨 제한.
    MagnetLevel = models.IntegerField()
    # 자석 증가 / 감소치.
    MagnetAddValue = models.FloatField()
    # 자석 최소 값.
    MagnetMinValue = models.FloatField()
    # 보호막시간.
    ShieldCost = models.IntegerField()
    # 보호막 레벨 제한.
    ShieldLevel = models.IntegerField()
    # 보호막 증가 / 감소치.
    ShieldAddValue = models.FloatField()
    # 보호막 최소 값.
    ShieldMinValue = models.FloatField()
    # 확대 시간.
    BigCost = models.IntegerField()
    # 확대 레벨 제한.
    BigLevel = models.IntegerField()
    # 확대 증가 / 감소치.
    BigAddValue = models.FloatField()
    # 확대 최소 값.
    BigMinValue = models.FloatField()
    # 축소시간.
    SmallCost = models.IntegerField()
    # 축소 레벨 제한.
    SmallLevel = models.IntegerField()
    # 축소 증가 / 감소치.
    SmallAddValue = models.FloatField()
    # 축소 최소 값.
    SmallMinValue = models.FloatField()

class VehicleUpgradeData(models.Model):
    # 가격
    Cost = models.IntegerField()
    # 제한 레벨.
    MaxLevel = models.IntegerField()
    # 증가 / 감소치.
    AddValue = models.FloatField()
    # 최소 값.
    MinValue = models.FloatField()

class FriendRankNo1Reward(models.Model):
    # 타입.
    Type = models.IntegerField()
    # 아이템SN.
    ItemSN = models.IntegerField()
    # 수량.
    Value = models.IntegerField()

class FriendRankNo2Reward(models.Model):
    # 타입.
    Type = models.IntegerField()
    # 아이템SN.
    ItemSN = models.IntegerField()
    # 수량.
    Value = models.IntegerField()

class FriendRankNo3Reward(models.Model):
    # 타입.
    Type = models.IntegerField()
    # 아이템SN.
    ItemSN = models.IntegerField()
    # 수량.
    Value = models.IntegerField()

class ChickenScoreReward(models.Model):
    # 타입.
    Type = models.IntegerField()
    # 아이템SN.
    ItemSN = models.IntegerField()
    # 수량.
    Value = models.IntegerField()

admin.site.register(Shop_TokenData)
admin.site.register(Shop_GoldData)
admin.site.register(Shop_CashData)
admin.site.register(Shop_ItemData)
admin.site.register(Shop_CharacterData)
admin.site.register(Shop_VehicleData)
admin.site.register(Shop_PetData)
admin.site.register(Pet_SuperRewardData)
admin.site.register(Pet_RareRewardData)
admin.site.register(Pet_NormalRewardData)
admin.site.register(CharacterUpgradeData)
admin.site.register(VehicleUpgradeData)
admin.site.register(FriendRankNo1Reward)
admin.site.register(FriendRankNo2Reward)
admin.site.register(FriendRankNo3Reward)
admin.site.register(ChickenScoreReward)
