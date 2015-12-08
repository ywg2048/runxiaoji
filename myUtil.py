# -*- coding: utf-8 -*-
from datetime import *
from django.utils.timezone import utc
import base64

# 딕셔너리를 json포멧으로 변환하여 문자열로 리턴.
def JsonPaser(data):

    # Array
    if type(data) == list:
        return ArrayPaser(data)
    # Table
    elif type(data) == dict:
        return DicPaser(data)
    else:
        return ''

def DicPaser(data):
    text = '{'
    keyList = data.keys()
    if len(keyList) == 0:
        return ''

    for key in keyList:
        text =  text + '\"' + key + '\"' + ':'
        # Array
        if type(data.get(key)) == list:
            text = text + ArrayPaser(data.get(key)) + ','
        # Table
        elif type(data.get(key)) == dict:
            text = text + DicPaser(data.get(key)) + ','
        else:
            text = text + typeToString(data.get(key))

    text = text[:-1]
    text = text + '}'

    return text

def ArrayPaser(data):

    if len(data) == 0:
        return ''

    text = '['
    for value in data:
        # Array
        if type(value) == list:
            text = text + ArrayPaser(value) + ','
        # Table
        elif type(value) == dict:
            text = text + DicPaser(value) + ','
        else:
            text = text + typeToString(value)

    text = text[:-1]
    text = text + ']'

    return text

def typeToString(data):
    text = ''
    # bool
    if type(data) == bool:
        if str(data) == 'True':
            text = text + 'true,'
        else:
            text = text + 'false,'
    # int
    elif type(data) == int:
        text = text + str(data) + ','
    # string
    else:
        text = text + '\"' + str(data) + '\",'

    return text


# 랜덤으로 문자열 리턴.
def random_char(n):
    import random
    items = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    c = ''
    for i in range(n):
        c += random.choice(items)
    return c

# 문자열 인코딩.
def encodeStr(str):
    return base64.encodebytes(bytes(str, 'utf-8')).decode('ascii')[:-1].replace('+','%2B').replace('&','%26')

# 현재시간 반환.
def NowTime():
    return datetime.utcnow().replace(tzinfo=utc)
# 남은 초를 반환.
def ToSecRemaining(dt):
    return TimedeltaToSeconds(dt - datetime.utcnow().replace(tzinfo=utc))

# 지난 시간 초로 반환.
def ToLastSec(dt):
    return TimedeltaToSeconds(datetime.utcnow().replace(tzinfo=utc) - dt)

# 날짜를 초로 변환.
def TimedeltaToSeconds(td):
    return round(td.microseconds/float(1000000)) + (td.seconds + td.days * 24 * 3600)
