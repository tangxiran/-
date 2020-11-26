import requests
import sys
import time
import pandas as pd
import numpy as np
import datetime

word_url = 'http://index.baidu.com/api/SearchApi/thumbnail?area=0&word={}'
# word_url1 = f'http://index.baidu.com/api/SearchApi/thumbnail?area=0&word=[[%7B%22name%22:%22{}%22,%22wordType%22:1%7D]]'
COOKIES = 'BIDUPSID=A7530C0DA77402D07186877613ED8DF4; PSTM=1572155429; BAIDUID=C7F0FD34DFA50C7A362AFE08364C495E:FG=1; BDUSS=2VrMnNDUzdOOW92SkJYRmZpYXhLRjhhODZTamNHampJZzgtajUyUVVPYlg0ZTFkRVFBQUFBJCQAAAAAAAAAAAEAAABBclexy-q2~squ09DT4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANdUxl3XVMZdU; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1463_33123_33059_31254_33098_33101_26350_22159; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1591187994,1591610816; bdindexid=rfj4nvkpb8il9sl3ii6sm40tv2; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1591610824; delPer=0; PSINO=2; BDRCVFR[1kRcOFa5hin]=mk3SLVN4HKm; RT="sl=0&ss=kb6da8yx&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&z=1&dm=baidu.com&si=9bzana5mhzs&ld=9qm&ul=9xgx"'
# COOKIES = 'BUDSS=2VrMnNDUzdOOW92SkJYRmZpYXhLRjhhODZTamNHampJZzgtajUyUVVPYlg0ZTFkRVFBQUFBJCQAAAAAAAAAAAEAAABBclexy-q2~squ09DT4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANdUxl3XVMZdU'

def decrypt(t, e):
    n = list(t)
    i = list(e)
    a = {}
    result = []
    ln = int(len(n) / 2)
    start = n[ln:]
    end = n[:ln]
    for j, k in zip(start, end):
        a.update({k: j})
    for j in e:
        result.append(a.get(j))
    return ''.join(result)


def get_index_home(keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'Cookie': COOKIES
    }

    word_url = f'http://index.baidu.com/api/SearchApi/thumbnail?area=0&word=[[%7B%22name%22:%22{keyword}%22,%22wordType%22:1%7D]]'
    resp = requests.get(word_url, headers=headers)
    j = resp.json()

    print(j)

    uniqid = j.get('data').get('uniqid')
    return get_ptbk(uniqid)


def get_ptbk(uniqid):
    url = 'http://index.baidu.com/Interface/ptbk?uniqid={}'
    ptbk_headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Cookie': COOKIES,
        'DNT': '1',
        'Host': 'index.baidu.com',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://index.baidu.com/v2/index.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    resp = requests.get(url.format(uniqid), headers=ptbk_headers)
    if resp.status_code != 200:
        print('获取uniqid失败')
        sys.exit(1)
    return resp.json().get('data')


def get_index_data(keyword, start='2012-01-01', end='2012-12-31'):
    url = f'http://index.baidu.com/api/SugApi/sug?inputword[]={keyword}&area=0&startDate={start}&endDate={end}'
    word_param = f'[[%7B"name":"{keyword}","wordType":1%7D]]'
    url1 = f'http://index.baidu.com/api/SearchApi/index?area=0&word={word_param}&startDate={start}&endDate={end}'
    print(url1 + "\n")
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Cookie': COOKIES,
        'DNT': '1',
        'Host': 'index.baidu.com',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://index.baidu.com/v2/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    resp = requests.get(url1, headers=headers)
    if resp.status_code != 200:
        print('获取指数失败')
        sys.exit(1)

    # print('\n======= json ======\n')
    # print(resp.json())

    data = resp.json().get('data').get('userIndexes')[0]
    uniqid = resp.json().get('data').get('uniqid')

    # print('\n======= data ======\n')
    # print(data)
    #
    # print('\n======= uniqid ======\n')
    # print(uniqid)


    ptbk = get_ptbk(uniqid)

    # print(ptbk)

    # while ptbk is None or ptbk == '':
    #     ptbk = get_index_home(uniqid)
    all_data = data.get('all').get('data')
    result = decrypt(ptbk, all_data)
    result = result.split(',')

    # print('\n======= result ======\n')
    # print(result)
    return result

def demo():
    data = get_index_data(keyword='疫情')
    print(data)

if __name__ == '__main__':
    demo()
