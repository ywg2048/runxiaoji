# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.

# 최근 플레이 데이터.
class CurrPlayData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 캐릭터.
    CharacterSN = models.IntegerField()
    # 최근 플레이모드(1 :무한, 2 : 타임어택).
    GameMode = models.IntegerField()
    # 사용중인 펫 (0 : 없음).
    Pet1SN = models.IntegerField()
    Pet2SN = models.IntegerField()
    # 사용중인 탈것 (0 : 없음).
    VehicleSN = models.IntegerField()

# 캐릭터 데이터.
class CharacterData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 캐릭터SN
    CharacterSN = models.IntegerField()
    # 업그레이드.
    # HP
    Level_HP = models.IntegerField()
    # MP
    Level_MP = models.IntegerField()
    # Magnet
    Level_Magnet = models.IntegerField()
    # GodMod
    Level_GodDash = models.IntegerField()
    # Shield
    Level_Shield = models.IntegerField()
    # ActorBig
    Level_Big = models.IntegerField()
    # ActorSmall
    Level_Small = models.IntegerField()

# 펫데이터.
class PetData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 펫SN.
    PetSN = models.IntegerField()
    # 등급.
    Grade = models.IntegerField()

# 탈것 데이터.
class VehicleData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 탈것SN.
    VehicleSN = models.IntegerField()
    # 레벨.
    Level = models.IntegerField()

# 플레이 깅보.
class PlayRecordData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 누적 친구 초대수.
    TotalInviteFriend = models.IntegerField()
    # 누적 플레이 수.
    TotalPlay = models.IntegerField()
    # 누적 이어하기 수.
    TotalRelayPlay = models.IntegerField()
    # 최고 점수.
    BestScore = models.IntegerField()
    # 누적 점수.
    TotalScore = models.IntegerField()
    # 제일 멀리간 거리.
    BestDistance = models.IntegerField()
    # 누적 거리.
    TotalDistance = models.IntegerField()
    # 최고 코인획득.
    BestGetCoin = models.IntegerField()
    # 누적 코인 획득.
    TotalGetCoin = models.IntegerField()
    # 누적 골드.
    TotalGold = models.IntegerField()
    # 사용한 골드.
    TotalUseGold = models.IntegerField()
    # 최고 대쉬 점수.
    BestDashScore = models.IntegerField()
    # 누적 대쉬 사용 횟수.
    TotalUseDash = models.IntegerField()
    # 시작 질주 아이템 구입 횟수.
    Item_1 = models.IntegerField()
    # 자석아이템 구입횟수.
    Item_2 = models.IntegerField()
    # 보호막 아이템 구입횟수.
    Item_3 = models.IntegerField()
    # 코인더블 아이템 구입횟수.
    Item_4 = models.IntegerField()
    # 대쉬게이지 아이템 구입횟수.
    Item_5 = models.IntegerField()

# 머니 데이터.
class MoneyData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 골드.
    GoldValue = models.IntegerField()
    # 캐쉬.
    CashValue = models.IntegerField()

    def __str__(self):
        return "%d-%d-%d" % (self.UserSN, self.GoldValue, self.CashValue)

# 보유 아이템.
class ItemData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 아이템SN.
    ItemSN = models.IntegerField()
    # 수량.
    Value = models.IntegerField()

# 토큰 데이터.
class TokenData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # Toekn갯수.
    ToeknValue = models.IntegerField()
    # 토큰생성 시간.
    CreateTime = models.DateTimeField()

# 출석데이터.
class DailyCheckData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 출석시간.
    CheckTime = models.DateField();

# 치킨 점수 보상데이터.
class ChickenScoreRewardData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()

# 탈퇴 유저 데이터.
class WithdrawalData(models.Model):
    # 유저ID.
    UserID = models.CharField(max_length=40, blank = True, null = True)
    # 탈퇴날.
    WithdrawTime = models.DateTimeField(blank = True, null = True)


admin.site.register(CurrPlayData)
admin.site.register(CharacterData)
admin.site.register(PetData)
admin.site.register(VehicleData)
admin.site.register(PlayRecordData)
admin.site.register(MoneyData)
admin.site.register(ItemData)
admin.site.register(TokenData)
admin.site.register(DailyCheckData)
admin.site.register(ChickenScoreRewardData)
admin.site.register(WithdrawalData)
