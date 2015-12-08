# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
# Create your models here.

# 랭킹 초기화 정보.
class RankInfoData(models.Model):
    # 주간랭크 초기화 시간.
    WeekInitTime = models.DateTimeField()
    # 월간 랭크 초기화 시간.
    MonthInitTime = models.DateTimeField()
    # 친구 랭크 초기화 시간.
    FriendInitTime = models.DateTimeField()

# 전적 정보.
class BestRecodData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 무한모드 랭킹 1등 횟수.
    InfiniteModeRank_1 = models.IntegerField()
    # 무한모드 랭킹 2등 횟수.
    InfiniteModeRank_2 = models.IntegerField()
    # 무한모드 랭킹 3등 횟수.
    InfiniteModeRank_3 = models.IntegerField()
    # 타임어택 랭킹 1등 횟수.
    TimeAttackModeRank_1 = models.IntegerField()
    # 타임어택 랭킹 2등 횟수.
    TimeAttackModeRank_2 = models.IntegerField()
    # 타임어택 랭킹 3등 횟수.
    TimeAttackModeRank_3 = models.IntegerField()


# 치킨 랭킹 데이터.
class ChickenRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 보유 치킨쿠폰수.
    CouponCnt = models.IntegerField()
    # 누적 치킨쿠폰수.
    AccrueCouponCnt = models.IntegerField()
    # 조각치킨획득 누적횟수.
    PieceChickenGetCnt = models.IntegerField()
    # 한마리치킨 획득 누적 횟수.
    ChickenGetCnt = models.IntegerField()

# 무한모드 친구 전주간랭킹 데이터.
class InfiniteFriendLastWeekRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    #확인여부.
    Confirm = models.BooleanField(default=False)


# 무한모드 친구 주간랭킹 데이터.
class InfiniteFriendWeekRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    # 캐릭터.
    CharacterSN = models.IntegerField()
    # 펫
    Pet1SN = models.IntegerField()
    Pet2SN = models.IntegerField()
    # 탈것.
    VehicleSN = models.IntegerField()


# 무한모드 전주간랭킹 데이터.
class InfiniteLastWeekRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    #확인여부.
    Confirm = models.BooleanField(default=False)


# 무한모드 주간랭킹 데이터.
class InfiniteWeekRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    # 캐릭터.
    CharacterSN = models.IntegerField()
    # 펫
    Pet1SN = models.IntegerField()
    Pet2SN = models.IntegerField()
    # 탈것.
    VehicleSN = models.IntegerField()

# 타임어택 친구 전주간랭킹 데이터.
class TimeAttackFriendLastWeekRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    # 확인여부.
    Confirm = models.BooleanField(default=False)

# 타임어택 친구 주간랭킹 데이터.
class TimeAttackFriendWeekRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    # 캐릭터.
    CharacterSN = models.IntegerField()
    # 펫
    Pet1SN = models.IntegerField()
    Pet2SN = models.IntegerField()
    # 탈것.
    VehicleSN = models.IntegerField()

# 타임어택 전주간랭킹 데이터.
class TimeAttackLastWeekRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    # 확인여부.
    Confirm = models.BooleanField(default=False)

# 타임어택 주간랭킹 데이터.
class TimeAttackWeekRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    # 캐릭터.
    CharacterSN = models.IntegerField()
    # 펫
    Pet1SN = models.IntegerField()
    Pet2SN = models.IntegerField()
    # 탈것.
    VehicleSN = models.IntegerField()

# 무한모드 전월간랭킹 데이터.
class InfiniteLastMonthRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    # 확인여부.
    Confirm = models.BooleanField(default=False)

# 무한모드 월간랭킹 데이터.
class InfiniteMonthRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    # 캐릭터.
    CharacterSN = models.IntegerField()
    # 펫
    Pet1SN = models.IntegerField()
    Pet2SN = models.IntegerField()
    # 탈것.
    VehicleSN = models.IntegerField()

# 타임어택 전월간랭킹 데이터.
class TimeAttackLastMonthRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    # 확인여부.
    Confirm = models.BooleanField(default=False)

# 타임어택 월간랭킹 데이터.
class TimeAttackMonthRankData(models.Model):
    # 유저SN.
    UserSN = models.IntegerField()
    # 점수.
    Score = models.IntegerField()
    # 캐릭터.
    CharacterSN = models.IntegerField()
    # 펫
    Pet1SN = models.IntegerField()
    Pet2SN = models.IntegerField()
    # 탈것.
    VehicleSN = models.IntegerField()

admin.site.register(RankInfoData)
admin.site.register(BestRecodData)
admin.site.register(ChickenRankData)
admin.site.register(InfiniteLastWeekRankData)
admin.site.register(InfiniteWeekRankData)
admin.site.register(TimeAttackLastWeekRankData)
admin.site.register(TimeAttackWeekRankData)
admin.site.register(InfiniteLastMonthRankData)
admin.site.register(InfiniteMonthRankData)
admin.site.register(TimeAttackLastMonthRankData)
admin.site.register(TimeAttackMonthRankData)

admin.site.register(InfiniteFriendLastWeekRankData)
admin.site.register(InfiniteFriendWeekRankData)
admin.site.register(TimeAttackFriendLastWeekRankData)
admin.site.register(TimeAttackFriendWeekRankData)
