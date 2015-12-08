# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import json
import base64
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from Crypto.Hash import SHA
import binascii

pripem = """-----BEGIN RSA PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAKTgGQKMQTE64bpoW+q3ngEEhC3w
cJNWNml54arx6MK+tzY/8vnHnrJqgPrqfMs42GmW8/CXhQsGRoRaa1PDcazsmZayOswb+6fo/IJd
SK6TulajQHNQ77clPmTgGtEMLDlp4HN5oKdVMA3fjhkTf4C54fR7rXcDEqCPVmEhRrw3AgMBAAEC
gYBVlCBHK0e3Zum9mOeE6HPx8UculSvJvikWDHZvBYucceOlHAJhVhTwZMm387h8v2/NNtY9nlgn
RcWac1hcLQk2MwO3FdO74JBQfEwmf5W7N7WN+273iMN9dpavL5saoTVE6WBdisAO0fl0llJHrpDD
wV+DrvpINrmW4y9cO6rX2QJBAOcYzuv4isw7WxRc580bcgWq+f7sJ5mroVA0UA+XNSaDzJcVZN4S
Vou7SvmMvu+yObCfzvDd50oJEdtO7NAFbI0CQQC2pHVup3J9SZUnq/ZgyyI4KAxfmRC9SUqUMJOi
con9wXwO2IVkQMB/V2g1YwcJB58V0RDZu4bVv8lSfMDl8FTTAkAkLOL/V1nK3KPGTUDP/7Lapkga
GrecO5y15Gp/9kiQreMR53xxsucvWnNDG0AsX3beajXHyMTS9xZ/gRxa9+5lAkBA78YE2qodG31Z
ho1pqq928d48WwqVkipe98p11m1zeEhoatk6ZL9MR0J4wMWukzQfqJ5qG398Hd0xY8OdvU4bAkEA
jrV7FC702OK3JbRDI5s6xdYHz0uEJG0zafwjtd22JPBTwzUfCeKYW+husvKcfpnIg52sIxGKbkaj
nur0cyDk3g==
-----END RSA PRIVATE KEY-----
"""


# Create your views here.
@csrf_exempt
def KuuBusCallback(request):
    if request.method == 'POST':
    	data = {'ErrorCode' : '99','Message' : 'error'}
    	return HttpResponse(json.dumps(data), content_type="application/json")

    if not request.GET.get('param_data'):
    	data = {'ErrorCode' : '101', 'Message' : 'param_data does not exist'}
    	return HttpResponse(json.dumps(data), content_type="application/json")
    elif not request.GET.get('sign'):
    	data = {'ErrorCode' : '101', 'Message' : 'sign does not exist'}
    	return HttpResponse(json.dumps(data), content_type="application/json")

    try:
        paramdata = request.GET.get('param_data')
        print('param_data is:', paramdata)
        #paramByte = base64.b64decode(paramdata)
        #print('paramByte byte is:', paramByte)
    except :
        data = {'ErrorCode' : '102', 'Message' : 'param_data is not available'}
        return HttpResponse(json.dumps(data), content_type="application/json")


    try:
        sign = request.GET.get('sign')
        print('sign is:', sign)
        #signByte = base64.b64decode(sign)
        #print('signByte byte is:', signByte)
    except:
        data = {'ErrorCode' : '102', 'Message' : 'sign is not available'}
        return HttpResponse(json.dumps(data), content_type="application/json")
 

    paramMD5 = hashlib.new("md5", base64.b64decode(paramdata)).hexdigest()
    print ('paramdata md5 is:', paramMD5)

    priKey = RSA.importKey(pripem)
    
    try:
        signDecod = rsa_base64_decrypt(sign, priKey)
        sSignDecod = binascii.hexlify(signDecod).decode("utf-8")
        print("Sign decode is:", signDecod)
        print("signDecod is:", sSignDecod)
        if paramMD5 != sSignDecod :
            data = {'ErrorCode' : '103','Message' : 'Signcode can not verified'}
            return HttpResponse(json.dumps(data), content_type="application/json")        
    except:
        data = {'ErrorCode' : '103','Message' : 'Signcode can not verified'}
        return HttpResponse(json.dumps(data), content_type="application/json")        


    deParamdata = rsa_base64_decrypt(paramdata, priKey)
    print("deParamdata decode is:", deParamdata)
    sDeParamdata = deParamdata.decode("utf-8")
    print("sDeParamdata is:", sDeParamdata)
    
    try:
        pass
    except:
        data = {'ErrorCode' : '104','Message' : 'Data can not decrypt'}
        return HttpResponse(json.dumps(data), content_type="application/json")        

    return HttpResponse("success")

def rsa_base64_decrypt(data,key):  
    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize)
    cipher = PKCS1_v1_5.new(key)  
    content = base64.b64decode(data)
    result = b''
    for i in range(0, int(len(content) / 128)):
        c = content[:128]
        result = result + cipher.decrypt(content[:128], sentinel)
        content = content[128:]
    return result
















