from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import pprint
import pandas as pd
import numpy as np
import warnings
import folium
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import urllib, base64
from io import BytesIO
import base64

# 점수, 등수, 각비즈니스별 (개수, 서울시 평균 배수, 10km제곱당 시설 개수, 만 세대당 시설 개수), 승수(서울 평균보다 점수가 높은 곳)
my_gu = '강남구'

with open(f'../data/whole_gu_analysis.json', 'r', encoding='utf-8') as f:
    last_json = json.load(f)

print(last_json)

# def load_score(mu_gu):

# print(last_json[my_gu][0]['점수'])
# print(last_json[my_gu][1]['등수'])
# print(last_json[my_gu][14]['면적 승수'].split()[0],last_json[my_gu][14]['면적 승수'].split()[-1])
# print(last_json[my_gu][15]['세대 승수'].split()[0],last_json[my_gu][15]['세대 승수'].split()[-1])

def load_score(my_gu):
    with open(f'../data/whole_gu_analysis.json', 'r', encoding='utf-8') as f:
        last_json = json.load(f)
    # print(last_json[my_gu][0])
    get_score = last_json[my_gu][0]['점수']
    print(get_score)
    return get_score

def load_rank(my_gu):
    with open(f'../data/whole_gu_analysis.json', 'r', encoding='utf-8') as f:
        last_json = json.load(f)
    get_ranking = last_json[my_gu][1]['등수']
    print(get_ranking)
    return get_ranking

bs = '반려견놀이터'
# bs = '반려동물교육센터'

def click_bs(my_gu,bs):
    cnt = 0
    count =0
    a = last_json[my_gu]
    for i in a:
        lst = list(i.keys())
        if lst[0] == bs:
            key = lst[0]
            cnt = count
            break
        else:
            print('모차즘')
        count += 1
    b = a[cnt]
    # print(b[key][0])
    if key == '반려동물교육센터':
        if b[key][0] == 1:
            print('우리 구에는 있어요!')
            content = '우리 구에는 있어요!'
            return content
        else:
            print('우리 구에는 없어요!')
            content = '우리 구에는 없어요!'
            return content
    print(b[key][0])
    print(f'{key}의 수는 {b[key][0]}개이며 서울시 평균의 {b[key][1]}배이다, 10km면적당 {key}개수는 {b[key][2]}개이고 만 가구당 우리 구의 {key} 개수는 {b[key][3]}개 이다')
    return key, b[key][0],b[key][1],b[key][2],b[key][3]


load_score(my_gu)
load_rank(my_gu)
click_bs(my_gu,bs)