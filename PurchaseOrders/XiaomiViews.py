# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from PurchaseOrders.models import *
import json

# Create your views here.
@csrf_exempt
def XiaomiCallback(request):
    if request.method == 'POST':
    	data = {'ErrorCode' : '99','Message' : 'error'}
    	return HttpResponse(json.dumps(data), content_type="application/json")

    print('request full path:', request.get_full_path())

    if not request.GET.get('appId'):
        data = {'errcode' : '1515', 'errMsg' : 'appId 错误'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    elif not request.GET.get('cpOrderId'):
        data = {'errcode' : '1506', 'errMsg' : 'cpOrderId 错误'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    elif not request.GET.get('uid'):
        data = {'errcode' : '1516', 'errMsg' : 'uid 错误'}
        return HttpResponse(json.dumps(data), content_type="application/json")       
    elif not request.GET.get('signature'):
        data = {'errcode' : '1525', 'errMsg' : 'signature 错误'}
        return HttpResponse(json.dumps(data), content_type="application/json")  
    elif not request.GET.get('orderId'):
        data = {'errcode' : '99', 'errMsg' : 'orderId is must'}
        return HttpResponse(json.dumps(data), content_type="application/json")  
    elif not request.GET.get('orderStatus'):
        data = {'errcode' : '99', 'errMsg' : 'orderStatus is must '}
        return HttpResponse(json.dumps(data), content_type="application/json")  
    elif not request.GET.get('payFee'):
        data = {'errcode' : '99', 'errMsg' : 'payFee is must'}
        return HttpResponse(json.dumps(data), content_type="application/json")  
    elif not request.GET.get('productCode'):
        data = {'errcode' : '99', 'errMsg' : 'productCode is must'}
        return HttpResponse(json.dumps(data), content_type="application/json")  
    elif not request.GET.get('productName'):
        data = {'errcode' : '99', 'errMsg' : 'productName is must'}
        return HttpResponse(json.dumps(data), content_type="application/json")  
    elif not request.GET.get('productCount'):
        data = {'errcode' : '99', 'errMsg' : 'productCount is must'}
        return HttpResponse(json.dumps(data), content_type="application/json")  
    elif not request.GET.get('payTime'):
        data = {'errcode' : '99', 'errMsg' : 'payTime is must'}
        return HttpResponse(json.dumps(data), content_type="application/json")  

    appId = request.GET.get('appId')
    cpOrderId = request.GET.get('cpOrderId')
    uid = request.GET.get('uid')
    orderId = request.GET.get('orderId')
    orderStatus = request.GET.get('orderStatus')
    payFee = request.GET.get('payFee')
    productCode = request.GET.get('productCode')
    productName = request.GET.get('productName')
    productCount = request.GET.get('productCount')
    payTime = request.GET.get('payTime')
    signature = request.GET.get('signature')


    orderList = list(MiPurchaseOrderData.objects.filter(OrderId = orderId))
    if len(orderList) > 0 :
        data = {'errcode' : '200', 'errMsg' : 'success'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    order = MiPurchaseOrderData(AppId = appId, 
        CpOrderId = cpOrderId, 
        UId = uid, 
        OrderId = orderId, 
        OrderStatus = orderStatus, 
        PayFee = payFee, 
        ProductCode = productCode,
        ProductName = productName,
        ProductCount = productCount,
        PayTime = payTime,
        Signature = signature)

    if request.GET.get('cpUserInfo'):
        order.CpUserInfo = request.GET.get('cpUserInfo')
    if request.GET.get('orderConsumeType'):
        order.OrderConsumeType = request.GET.get('orderConsumeType')
    if request.GET.get('partnerGiftConsume'):
        order.PartnerGiftConsume = request.GET.get('partnerGiftConsume')

    order.save()

    data = {'errcode' : '200', 'errMsg' : 'success'}
    return HttpResponse(json.dumps(data), content_type="application/json")

def sign_request():
    from hashlib import sha1
    import hmac

    # key = CONSUMER_SECRET& #If you dont have a token yet
    key = "CONSUMER_SECRET&TOKEN_SECRET" 


    # The Base String as specified here: 
    raw = "BASE_STRING" # as specified by oauth

    hashed = hmac.new(key, raw, sha1)

    # The signature
    return hashed.digest().encode("base64").rstrip('\n')

    