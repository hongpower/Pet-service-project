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
    hospital_data = hospital_data[['?????????????????????', '???????????????', '?????????????????????', '?????????????????????', '????????????', '????????????(x)', '????????????(y)']]
    hospital_data = hospital_data.loc[hospital_data['?????????????????????'] == '??????']
    hospital_data['?????????????????????'] = hospital_data['?????????????????????'].fillna(hospital_data['?????????????????????'])
    hospital_data = hospital_data.fillna(0)
    hospital_data = hospital_data[hospital_data['?????????????????????'].str.contains(f'??????????????? {input_gu}', na=False)]
    hospital_local = hospital_data.loc[:, '?????????????????????']
    center = addr_to_lat_lon2(input_gu)
    center_loc = folium.Map(location=[center[0], center[1]], zoom_start=12)
    for i in hospital_local:
        if i != "0" and i !=0 :
            try:
                local = addr_to_lat_lon2(i)
            except IndexError as e:
                pass
            doro_add = hospital_data[hospital_data.????????????????????? == i]
            hosp_name = doro_add['????????????'].values
            folium.Marker([local[0], local[1]], popup=folium.Popup(hosp_name[0], max_width=400),
                          icon=folium.Icon(icon=icon,prefix='fa',color='red')).add_to(center_loc)
        else:
            pass
            # print(i)
    # center_loc.save('pratice.html')
    return center_loc

def Location_Park2(input_file,input_gu):
    city_park = pd.read_csv(f'./data/pet_{input_file}', encoding='cp949')
    # print(city_park)
    city_park = city_park[['?????????', '????????????', '?????????????????????', '????????????', '??????', '??????', '????????????']]
    # city_park = city_park.loc[city_park['?????????????????????'] == '??????']
    city_park = city_park.fillna(0)
    city_park = city_park[city_park['?????????????????????'].str.contains(f'??????????????? {input_gu}', na=False)]
    # print(city_park)

    center = addr_to_lat_lon2(input_gu)
    center_loc = folium.Map(location=[center[0], center[1]], zoom_start=12)
    # ?????????????????? ???????????? ????????? ????????? ?????? ??????

    park_name = city_park['?????????']
    # print(park_name)
    # print(city_park[['??????','??????']])

    for i in park_name:
        # print(i)
        park_etc = city_park[city_park.????????? == i]
        park_addrss = park_etc.?????????????????????.values[0]
        # print(park_addrss)
        try:
            local = addr_to_lat_lon2(park_addrss)
        except IndexError as e:
            pass
        park_etc = city_park[city_park.????????? == i]
        park_width = park_etc.????????????.values
        # print(park_width)
        folium.Marker([local[0], local[1]], popup=folium.Popup(i + f' ????????????:{park_width}', max_width=200),
                      icon=folium.Icon(icon="tree", prefix='fa', color='green')).add_to(center_loc)
    # center_loc.save('pratice.html')

    return center_loc


api_key = 'b8b58dd6490543a58e8ab1ea5352a75f'

# ????????? ????????????
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
    # ????????? ???????????? ????????? ??????
    maps = my_loc._repr_html_()
    final_dict = {'my_loc' : maps}

    return maps