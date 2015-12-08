# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChickenWing.views.home', name='home'),
    # url(r'^ChickenWing/', include('ChickenWing.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # 서버체크.
    url(r'^ServerCheck/$', 'ServerInfo.views.ServerCheck'),
    # 공지 호출.
    url(r'^NoticeResponse/$', 'ServerInfo.views.NoticeResponse'),
    # 이벤트URL 호출.
    url(r'^EventURLResponse/$', 'ServerInfo.views.EventURLResponse'),
    # 로그인.
    url(r'^login/$', 'users.views.login'),
    url(r'^login2/$', 'users.views.login2'),
    # 상점가격데이터 가져오기.
    url(r'^ShopDataResponse/$', 'ShopData.views.ShopDataResponse'),

    # 최근플레이데이터 가져오기.
    url(r'^CurrPlayDataResponse/$', 'GameData.views.CurrPlayDataResponse'),
    # 플레이 기록데이터 가져오기.
    url(r'^PlayRecordDataResponse/$', 'GameData.views.PlayRecordDataResponse'),
    # 내가 보유하고잇는 데이터 가져오기.
    url(r'^InvenDataResponse/$', 'GameData.views.InvenDataResponse'),
    # 캐릭터 구매.
    url(r'^BuyCharacter/$', 'GameData.views.BuyCharacter'),
    # 캐릭터 업그레이드.
    url(r'^CharacterUpgrade/$', 'GameData.views.CharacterUpgrade'),
    # 탈것 구매.
    url(r'^BuyVehicle/$', 'GameData.views.BuyVehicle'),
    # 탈것 업그레이드.
    url(r'^VehicleUpgrade/$', 'GameData.views.VehicleUpgrade'),
    # 아이템 구매.
    url(r'^BuyItem/$', 'GameData.views.BuyItem'),
    # 아이템 사용.
    url(r'^UseItem/$', 'GameData.views.UseItem'),
    # 토큰 구매.
    url(r'^BuyToken/$', 'GameData.views.BuyToken'),
    # 골드 구매.
    url(r'^BuyGold/$', 'GameData.views.BuyGold'),
    # 캐쉬 구매.
    url(r'^BuyCash/$', 'GameData.views.BuyCash'),
    # Pet 뽑기.
    url(r'^GetPetResponse/$', 'GameData.views.GetPetResponse'),
    # Pet 슬롯 구매.
    url(r'^BuyPetSlot/$', 'GameData.views.BuyPetSlot'),
    # 토큰 가져오기.
    url(r'^TokenDataResponse/$', 'GameData.views.TokenDataResponse'),
    # 토큰값변경하기.
    url(r'^ChangeToken/$', 'GameData.views.ChangeToken'),
    # 토큰 사용.
    url(r'^UseToken/$', 'GameData.views.UseToken'),
    # 일일 출석체크.
    url(r'^DailyCheck/$', 'GameData.views.DailyCheck'),
    # 결과 업데이트.
    url(r'^ResultUpdate/$', 'GameData.views.ResultUpdate'),
    # 치킨 점수 업데이트.
    url(r'^ChickenScoreUpdate/$', 'GameData.views.ChickenScoreUpdate'),
    # 치킨 점수 보상.
    url(r'^ChickenScoreReward/$', 'GameData.views.ChickenScoreReward'),
    # 탈퇴 처리.
    url(r'^WithdrawalResponse/$', 'GameData.views.WithdrawalResponse'),
    # 이어하기 처리.
    url(r'^RelayCheck/$', 'GameData.views.RelayCheck'),
    # 최근 게임상태 업데이트.
    url(r'^CurrDataUpdate/$', 'GameData.views.CurrDataUpdate'),

    # 전적정보 가져오기.
    url(r'^BestRecodDataResponse/$', 'Ranking.views.BestRecodDataResponse'),
    # 랭킹초기화.
    url(r'^InitRankCheck/$', 'Ranking.views.InitRankCheck'),
    # 랭킹초기화까지 남은시간.
    url(r'^InitRankTimeResponse/$', 'Ranking.views.InitRankTimeResponse'),
    # 무한모드 친구 주간랭킹
    url(r'^FriendInfiniteWeekRankResponse/$', 'Ranking.views.FriendInfiniteWeekRankResponse'),
    # 타임어택 친구 주간랭킹
    url(r'^FriendTimeAttackWeekRankResponse/$', 'Ranking.views.FriendTimeAttackWeekRankResponse'),
    # 무한모드 주간랭킹
    url(r'^InfiniteWeekRankResponse/$', 'Ranking.views.InfiniteWeekRankResponse'),
    # 타임어택 주간랭킹
    url(r'^TimeAttackWeekRankResponse/$', 'Ranking.views.TimeAttackWeekRankResponse'),
    # 무한모드 월간랭킹
    url(r'^InfiniteMonthRankResponse/$', 'Ranking.views.InfiniteMonthRankResponse'),
    # 타임어택 월간랭킹
    url(r'^TimeAttackMonthRankResponse/$', 'Ranking.views.TimeAttackMonthRankResponse'),
    # 무한모드 친구 전주간랭킹
    url(r'^FriendInfiniteLastWeekRank/$', 'Ranking.views.FriendInfiniteLastWeekRankResponse'),
    # 타임어택 친구 전주간랭킹
    url(r'^FriendTimeAttackLastWeekRank/$', 'Ranking.views.FriendTimeAttackLastWeekRankResponse'),
    # 무한모드 전주간랭킹
    url(r'^InfiniteLastWeekRank/$', 'Ranking.views.InfiniteLastWeekRankResponse'),
    # 타임어택 전주간랭킹
    url(r'^TimeAttackLastWeekRank/$', 'Ranking.views.TimeAttackLastWeekRankResponse'),
    # 무한모드 전월간랭킹
    url(r'^InfiniteLastMonthRank/$', 'Ranking.views.InfiniteLastMonthRankResponse'),
    # 타임어택 전월간랭킹
    url(r'^TimeAttackLastMonthRank/$', 'Ranking.views.TimeAttackLastMonthRankResponse'),
    # 치킨 주간랭킹 초기화 여부.
    url(r'^IsChickenLastWeekRank/$', 'Ranking.views.IsChickenLastWeekRank'),
    # 치킨 월간랭킹 초기화 여부.
    url(r'^IsChickenLastMonthRank/$', 'Ranking.views.IsChickenLastMonthRank'),

    # 토큰메세지 가져오기.
    url(r'^TokenMessageResponse/$', 'MessageData.views.TokenMessageResponse'),
    # 캐쉬선물메세지 가져오기.
    url(r'^GiftMessageResponse/$', 'MessageData.views.GiftMessageResponse'),
    # 받은 선물 갯수 가져오기.
    url(r'^GiftAllMsgCount/$', 'MessageData.views.GiftAllMsgCount'),
    # 받은 선물 가져오기.
    url(r'^GiftAllMsgResponse/$', 'MessageData.views.GiftAllMsgResponse'),
    # 선물 받기.
    url(r'^GetGiftItem/$', 'MessageData.views.GetGiftItem'),
    # 모든선물 받기.
    url(r'^GetAllGiftItem/$', 'MessageData.views.GetAllGiftItem'),

    # 토큰 보내기.
    url(r'^SendTokenMessageResponse/$', 'MessageData.views.SendTokenMessageResponse'),
    # 캐쉬선물 보내기.
    url(r'^SendGiftMessageResponse/$', 'MessageData.views.SendGiftMessageResponse'),
    #토큰 수신 상태 변경.
    url(r'^TokenIsReceiveResponse/$', 'MessageData.views.TokenIsReceiveResponse'),

    # 카카오친구초대 등록.
    url(r'^InsertKakaoInviteResponse/$', 'Invite.views.InsertKakaoInviteResponse'),
    # 카카오 초대한친구리스트 가져오기.
    url(r'^KakaoInviteListResponse/$', 'Invite.views.KakaoInviteListResponse'),

    # 计费预留
    # url(r'^IAPCallBack/$', ''),
    url(r'^KuuBusCallback/$', 'PurchaseOrders.KuuBusViews.KuuBusCallback'),
    url(r'^XiaomiCallback/$', 'PurchaseOrders.XiaomiViews.XiaomiCallback'),
)
