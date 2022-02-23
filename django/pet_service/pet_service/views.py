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
from .graphs import *
from .map import Location_Map_Json2, Location_Medical_CSV2, Location_Park2, addr_to_lat_lon2, lat_lon_to_addr2, Map2

warnings.filterwarnings('ignore')

def mainpage(request):
    return render(request, 'main.html')

def index(request):
    return render(request, 'index.html')

## index.html
def getGu(request):
    with open(".\data\gulist.json", 'r', encoding="utf-8") as f:
        dict_gus = json.load(f)
    return JsonResponse(dict_gus)


def getBusiness(request):
    with open(".\data/business.json", 'r', encoding="utf-8") as f:
        dict_business = json.load(f)
    return JsonResponse(dict_business)

# 테이블 생성
def getInfo(request):
    gu_name = request.GET['gu_id']
    file_name = request.GET['bs_id']
    if file_name == 'hospital.csv' or file_name == 'medical.csv':
        hospital_data = pd.read_csv(f'./data/pet_{file_name}', encoding='cp949')
        hospital_data = hospital_data[['상세영업상태명', '소재지전화', '소재지전체주소', '도로명전체주소', '사업장명', '좌표정보(x)', '좌표정보(y)']]
        hospital_data = hospital_data.loc[hospital_data['상세영업상태명'] == '정상']
        hospital_data['도로명전체주소'] = hospital_data['도로명전체주소'].fillna(hospital_data['소재지전체주소'])
        hospital_data = hospital_data.fillna(0)
        hospital_data = hospital_data[hospital_data['도로명전체주소'].str.contains(f'서울특별시 {gu_name}', na=False)]
        hospital_local = hospital_data.loc[:, '도로명전체주소']
        csv_list = []
        final_dict = {}
        for i in hospital_local:
            doro_add = hospital_data[hospital_data.도로명전체주소 == i]
            hosp_name = doro_add['사업장명'].values
            tmp = {}
            tmp["상업명"] = hosp_name[0]
            tmp["주소"] = i
            csv_list.append(tmp)
        # print(csv_list)
        final_dict['info'] = csv_list
    elif file_name == 'city_park.csv':
        city_park = pd.read_csv(f'./data/pet_{file_name}', encoding='cp949')
        city_park = city_park[['공원명', '전화번호', '소재지지번주소', '공원구분', '위도', '경도', '공원면적']]
        city_park = city_park.fillna(0)
        city_park = city_park[city_park['소재지지번주소'].str.contains(f'서울특별시 {gu_name}', na=False)]
        park_name = city_park['공원명']
        csv_list = []
        final_dict = {}
        for i in park_name:
            park_etc = city_park[city_park.공원명 == i]
            park_address = park_etc.소재지지번주소.values
            park_etc = city_park[city_park.공원명 == i]
            park_width = park_etc.공원면적.values
            tmp = {}
            tmp['공원명'] = i
            tmp['면적'] = park_width[0]
            tmp['주소'] = park_address[0]
            csv_list.append(tmp)
        final_dict['info'] = csv_list
    else:
        with open(f".\data\pet_{file_name}", 'r', encoding="utf-8") as f:
            dict_info = json.load(f)
        final_dict = dict()
        final_dict['info'] = dict_info[gu_name]
    return JsonResponse(final_dict)

def Location_Map_Json(input_file,input_gu):
    center_loc = Location_Map_Json2(input_file, input_gu)
    return center_loc

def Location_Medical_CSV(input_file ,input_gu):
    center_loc = Location_Medical_CSV2(input_file, input_gu)
    return center_loc

def Location_Park(input_file,input_gu):
    center_loc = Location_Park2(input_file, input_gu)
    return center_loc

api_key = 'b8b58dd6490543a58e8ab1ea5352a75f'

# 주소로 좌표변환
def addr_to_lat_lon(addr):
    y,x =addr_to_lat_lon2(addr)
    return y,x

# 좌표로 주소변환
def lat_lon_to_addr(lon,lat):
    string = lat_lon_to_addr2(lon,lat)
    return string

def Map(request):
    input_file = request.GET['bs_id']
    input_gu = request.GET['gu_id']
    maps = Map2(input_file, input_gu)
    return HttpResponse(maps)

## score.html
def score(request):
    map = createMap()
    my_loc = map._repr_html_()
    graph = drawgraph()
    uri = urllib.parse.quote(graph)
    pie = drawpie()
    uri2 = urllib.parse.quote(pie)
    box = drawbox()
    uri3 = urllib.parse.quote(box)
    scatter = scatterplot()
    uri4 = urllib.parse.quote(scatter)
    scatter_em = scatter_line_em()
    uri5 = urllib.parse.quote(scatter_em)
    return render(request, 'score.html', {'my_loc':my_loc, 'my_graph':uri, 'my_pie':uri2, 'my_box':uri3,'my_scatter':uri4,
                                          'my_scatter_line_em':uri5})

def getBargraph(request):
    file_name = request.GET['business_name']
    user_loc = request.GET['user_loc']
    b64 = drawbargraph(file_name, user_loc)
    return HttpResponse(b64)

# 내 위치 찾기
def my_loc(request):
    lat = request.GET['lat']
    lon = request.GET['lon']
    my_loc = lat_lon_to_addr(lon,lat)
    gu_name = my_loc.split()[1]
    return HttpResponse(gu_name)

## Geo.html ; 지도까지 띄움
def Geo(request):
    return render(request,'geo.html')