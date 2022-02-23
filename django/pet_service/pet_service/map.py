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


def Location_Map_Json2(input_file,input_gu):
    with open(f'./data/pet_{input_file}', 'r', encoding='utf-8') as f:
        total_json = json.load(f)
    if input_file == 'cafe.json':
        icon = 'paw'
        prefix = 'fa'
        color = 'gray'
    elif input_file == 'together_cafe.json':
        icon = 'paw'
        prefix = 'fa'
        color = 'blue'
    elif input_file == 'together_diner.json':
        icon = 'info'
        prefix = 'fa'
        color = 'blue'
    elif input_file == 'education_center.json':
        icon = 'graduation-cap'
        prefix = 'fa'
        color = 'blue'
    elif input_file == 'garden.json':
        icon = 'home'
        prefix = 'fa'
        color = 'blue'
    elif input_file == 'hotel.json':
        icon = 'hotel'
        prefix = 'fa'
        color = 'blue'
    elif input_file == 'playground.json':
        icon = 'gamepad'
        prefix = 'fa'
        color = 'blue'
    elif input_file == 'salon.json':
        icon = 'scissors'
        prefix = 'fa'
        color = 'blue'
    elif input_file == 'store.json':
        icon="shopping-cart"
        prefix='glyphicon'
        color = 'blue'
    center = addr_to_lat_lon2(input_gu)
    # center_loc = folium.Map(location=[center[0],center[1]],zoom_start=14)
    center_loc = folium.Map(location=[center[0],center[1]],zoom_start=13)
    # print(total_json)
    gu_data = total_json[input_gu]
    # local = []
    for gu in gu_data:
        gu_address = gu["address"].replace(',', '')
        local = addr_to_lat_lon2(gu_address)
        folium.Marker([local[0], local[1]], popup=folium.Popup(gu['s_name'], max_width=400),
                      icon=folium.Icon(icon=icon,prefix=prefix,color=color)).add_to(center_loc)

    # center_loc.save('map.html')
    return center_loc

def Location_Medical_CSV2(input_file ,input_gu):
    hospital_data = pd.read_csv(f'./data/pet_{input_file}', encoding='cp949')
    pd.set_option('display.max_rows',None)
    if input_file == 'hospital.csv':
        icon = 'plus'
    elif input_file == 'medical.csv':
        icon = 'cart-plus'
    hospital_data = hospital_data[['상세영업상태명', '소재지전화', '소재지전체주소', '도로명전체주소', '사업장명', '좌표정보(x)', '좌표정보(y)']]
    hospital_data = hospital_data.loc[hospital_data['상세영업상태명'] == '정상']
    hospital_data['도로명전체주소'] = hospital_data['도로명전체주소'].fillna(hospital_data['소재지전체주소'])
    hospital_data = hospital_data.fillna(0)
    hospital_data = hospital_data[hospital_data['도로명전체주소'].str.contains(f'서울특별시 {input_gu}', na=False)]
    hospital_local = hospital_data.loc[:, '도로명전체주소']
    center = addr_to_lat_lon2(input_gu)
    center_loc = folium.Map(location=[center[0], center[1]], zoom_start=12)
    for i in hospital_local:
        if i != "0" and i !=0 :
            try:
                local = addr_to_lat_lon2(i)
            except IndexError as e:
                pass
            doro_add = hospital_data[hospital_data.도로명전체주소 == i]
            hosp_name = doro_add['사업장명'].values
            folium.Marker([local[0], local[1]], popup=folium.Popup(hosp_name[0], max_width=400),
                          icon=folium.Icon(icon=icon,prefix='fa',color='red')).add_to(center_loc)
        else:
            print(i)
    # center_loc.save('pratice.html')
    return center_loc

def Location_Park2(input_file,input_gu):
    city_park = pd.read_csv(f'./data/pet_{input_file}', encoding='cp949')
    # print(city_park)
    city_park = city_park[['공원명', '전화번호', '소재지지번주소', '공원구분', '위도', '경도', '공원면적']]
    # city_park = city_park.loc[city_park['상세영업상태명'] == '정상']
    city_park = city_park.fillna(0)
    city_park = city_park[city_park['소재지지번주소'].str.contains(f'서울특별시 {input_gu}', na=False)]
    # print(city_park)

    center = addr_to_lat_lon2(input_gu)
    center_loc = folium.Map(location=[center[0], center[1]], zoom_start=12)
    # 공원면적하고 공원명이 돌면서 위도랑 경도 빼기

    park_name = city_park['공원명']
    # print(park_name)
    # print(city_park[['위도','경도']])

    for i in park_name:
        print(i)
        park_etc = city_park[city_park.공원명 == i]
        park_addrss = park_etc.소재지지번주소.values[0]
        # print(park_addrss)
        try:
            local = addr_to_lat_lon2(park_addrss)
        except IndexError as e:
            pass
        park_etc = city_park[city_park.공원명 == i]
        park_width = park_etc.공원면적.values
        # print(park_width)
        folium.Marker([local[0], local[1]], popup=folium.Popup(i + f' 공원면적:{park_width}', max_width=200),
                      icon=folium.Icon(icon="tree", prefix='fa', color='green')).add_to(center_loc)
    # center_loc.save('pratice.html')

    return center_loc


api_key = 'b8b58dd6490543a58e8ab1ea5352a75f'

# 주소로 좌표변환
def addr_to_lat_lon2(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=addr)
    api = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(str(requests.get(url, headers=api).text))
    try:
        found = result['documents'][0]['address']
    except:
        found = {'x': 0, 'y': 0}
    return float(found['y']), float(found['x'])


def lat_lon_to_addr2(lon,lat):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={longitude}&y={latitude}'.format(longitude=lon,latitude=lat)
    api = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(str(requests.get(url, headers=api).text))
    found = result['documents'][0]['address_name']
    return str(found)

def Map2(input_file, input_gu):
    if input_file == 'hospital.csv' or input_file == 'medical.csv':
        my_loc = Location_Medical_CSV2(input_file,input_gu)
    elif input_file == 'city_park.csv':
        my_loc = Location_Park2(input_file,input_gu)
    else:
        # my_loc: center data
        my_loc = Location_Map_Json2(input_file, input_gu)
    # 지도를 문자열로 바꾸는 함수
    maps = my_loc._repr_html_()
    final_dict = {'my_loc' : maps}

    return maps