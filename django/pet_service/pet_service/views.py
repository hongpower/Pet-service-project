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
from .practice import createMap,drawgraph, drawpie

warnings.filterwarnings('ignore')

def mainpage(request):
    return render(request, 'main.html')

def index(request):
    return render(request, 'index.html')


def getGu(request):
    with open(".\data\gulist.json", 'r', encoding="utf-8") as f:
        dict_gus = json.load(f)
    return JsonResponse(dict_gus)


def getBusiness(request):
    with open(".\data/business.json", 'r', encoding="utf-8") as f:
        dict_business = json.load(f)
    return JsonResponse(dict_business)


def getInfo(request):
    gu_name = request.GET['gu_id']
    file_name = request.GET['bs_id']
    if file_name == 'hospital.csv' or file_name == 'medical.csv':
        hospital_data = pd.read_csv(f'./data/pet_{file_name}', encoding='cp949')
        hospital_data = hospital_data[['상세영업상태명', '소재지전화', '소재지전체주소', '도로명전체주소', '사업장명', '좌표정보(x)', '좌표정보(y)']]
        hospital_data = hospital_data.loc[hospital_data['상세영업상태명'] == '정상']
        hospital_data = hospital_data.fillna(0)
        hospital_data = hospital_data[hospital_data['소재지전체주소'].str.contains(f'서울특별시 {gu_name}', na=False)]
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



def Geo(request):
    return render(request,'geo.html')

def my_loc(request):
    lat = request.GET['lat']
    lon = request.GET['lon']
    my_loc = lat_lon_to_addr(lon,lat)
    gu_name = my_loc.split()[1]
    return HttpResponse(gu_name)

path_json = './data/'

def Location_Map_Json(input_file,input_gu):
    # with open(f'{path}{input_file}.json', 'r', encoding='utf-8') as f:
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
    center = addr_to_lat_lon(input_gu)
    # center_loc = folium.Map(location=[center[0],center[1]],zoom_start=14)
    center_loc = folium.Map(location=[center[0],center[1]],zoom_start=14)
    # print(total_json)
    gu_data = total_json[input_gu]
    # local = []
    for gu in gu_data:
        gu_address = gu["address"]
        local = addr_to_lat_lon(gu_address)
        folium.Marker([local[0], local[1]], popup=folium.Popup(gu['s_name'], max_width=400),
                      icon=folium.Icon(icon=icon,prefix=prefix,color=color)).add_to(center_loc)

    # center_loc.save('map.html')
    return center_loc

def Location_Medical_CSV(input_file ,input_gu):
    hospital_data = pd.read_csv(f'./data/pet_{input_file}', encoding='cp949')
    if input_file == 'hospital.csv':
        icon = 'plus'
    elif input_file == 'medical.csv':
        icon = 'cart-plus'
    hospital_data = hospital_data[['상세영업상태명', '소재지전화', '소재지전체주소', '도로명전체주소', '사업장명', '좌표정보(x)', '좌표정보(y)']]
    hospital_data = hospital_data.loc[hospital_data['상세영업상태명'] == '정상']

    hospital_data = hospital_data.fillna(0)
    hospital_data = hospital_data[hospital_data['소재지전체주소'].str.contains(f'서울특별시 {input_gu}', na=False)]

    # print(hospital_data)
    hospital_local = hospital_data.loc[:, '도로명전체주소']

    # print(hospital_local)
    center = addr_to_lat_lon(input_gu)
    center_loc = folium.Map(location=[center[0], center[1]], zoom_start=12)
    #
    for i in hospital_local:
        try:
            local = addr_to_lat_lon(i)
        except IndexError as e:
            pass
        doro_add = hospital_data[hospital_data.도로명전체주소 == i]
        hosp_name = doro_add['사업장명'].values
        folium.Marker([local[0], local[1]], popup=folium.Popup(hosp_name[0], max_width=400),
                      icon=folium.Icon(icon=icon,prefix='fa',color='red')).add_to(center_loc)

    # center_loc.save('pratice.html')
    return center_loc


def Location_Park(input_file,input_gu):
    city_park = pd.read_csv(f'./data/pet_{input_file}', encoding='cp949')
    # print(city_park)
    city_park = city_park[['공원명', '전화번호', '소재지지번주소', '공원구분', '위도', '경도', '공원면적']]
    # city_park = city_park.loc[city_park['상세영업상태명'] == '정상']
    city_park = city_park.fillna(0)
    city_park = city_park[city_park['소재지지번주소'].str.contains(f'서울특별시 {input_gu}', na=False)]
    # print(city_park)

    center = addr_to_lat_lon(input_gu)
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
            local = addr_to_lat_lon(park_addrss)
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
def addr_to_lat_lon(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=addr)
    api = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(str(requests.get(url, headers=api).text))
    found = result['documents'][0]['address']
    # return float(found['x']), float(found['y'])
    return float(found['y']), float(found['x'])

def lat_lon_to_addr(lon,lat):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={longitude}&y={latitude}'.format(longitude=lon,latitude=lat)
    api = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(str(requests.get(url, headers=api).text))
    found = result['documents'][0]['address_name']
    return str(found)

def Map(request):
    input_file = request.GET['bs_id']
    input_gu = request.GET['gu_id']
    if input_file == 'hospital.csv' or input_file == 'medical.csv':
        my_loc = Location_Medical_CSV(input_file,input_gu)
    elif input_file == 'city_park.csv':
        my_loc = Location_Park(input_file,input_gu)
    else:
        # my_loc: center data
        my_loc = Location_Map_Json(input_file, input_gu)
    # 지도를 문자열로 바꾸는 함수
    maps = my_loc._repr_html_()
    final_dict = {'my_loc' : maps}

    return HttpResponse(maps)

def practice(request):
    return render(request, 'menu_practice.html')

def score(request):
    map = createMap()
    my_loc = map._repr_html_()
    graph = drawgraph()
    uri = urllib.parse.quote(graph)
    pie = drawpie()
    uri2 = urllib.parse.quote(pie)
    return render(request, 'score.html', {'my_loc':my_loc, 'my_graph':uri, 'my_pie':uri2})

def getScore(request):
    file_name = request.GET['business_name']
    plt.rcParams['font.family'] = 'Malgun Gothic'

    if file_name == 'pet_city_park' or file_name == 'pet_hospital' or file_name == 'pet_medical':
        df = pd.read_csv(".\data\whole_merged_data2.csv", sep=",")
        gus = df['지역명'].tolist()

        if file_name =='pet_city_park':
            bs = df['공원 개수'].tolist()
            title = '공원 개수'
        elif file_name =='pet_medical':
            bs = df['동물약국'].tolist()
            title = '동물 약국 개수'
        else:
            bs = df['병원수'].tolist()
            title = '병원 개수'
        cnt_dict= dict(zip(gus, bs))
        tot = sum(cnt_dict.values())
        avg = tot / len(cnt_dict)
        df_bs = pd.DataFrame.from_dict([cnt_dict])
        plt.cla()

        # a 리셋되도록 넣어놈
        a = file_name
        plt.figure()
        a = sns.barplot(data=df_bs, color='blue')
        a.set_title(title)
        a.axhline(y=avg, color='red', linestyle='dashed', label="평균")
        a.set_xticklabels(a.get_xticklabels(), rotation=45)

        buf = io.BytesIO()
        a_png = a.get_figure()
        a_png.savefig(buf, format='png')
        buf.seek(0)

        data = buf.getvalue()
        b64 = base64.b64encode(data).decode()
        return HttpResponse(b64)

    else:
        with open(f'.\data\{file_name}.json', 'r', encoding='utf-8') as f:
            pet_business_info = json.load(f)
        # print(petcafe_json)
        gus = pet_business_info.keys()
        # print(gus)
        cnt_dict = {}
        for gu in gus:
            cnt = len(pet_business_info[gu])
            cnt_dict[gu] = cnt
        # print(cnt_dict)
        tot = sum(cnt_dict.values())
        avg = tot / len(cnt_dict)
        df = pd.DataFrame.from_dict([cnt_dict])
        with open(".\data/business.json", 'r', encoding="utf-8") as f:
            dict_business = json.load(f)
        title_lst = dict_business['business']
        bs_id_lst = dict_business['id']
        bs_id_lst = ['pet_'+bs for bs in bs_id_lst]
        title_dict = dict(zip(bs_id_lst, title_lst))
        plt.cla()
        plt.figure()
        b = sns.barplot(data=df, color='blue')
        b.axhline(y=avg, color='red', linestyle='dashed', label="평균")
        b.set_xticklabels(b.get_xticklabels(), rotation=45)
        b.set_title(title_dict[file_name+'.json']+' 개수')

        # graph를 dtring buffer로 바꾼 후에 64비트 코드로 바꾸고 이미지로
        buf = io.BytesIO()
        b_png = b.get_figure()
        b_png.savefig(buf, format='png')
        buf.seek(0)

        data = buf.getvalue()
        b64 = base64.b64encode(data).decode()
        return HttpResponse(b64)

def getPie(request):
    ## 파이 그래프 생성 함수:
    df = pd.read_csv(".\data\whole_merged_data2.csv", sep=",")
    gus = df['지역명'].tolist()
    parks = df['공원 개수'].tolist()
    cnt_dict_park = dict(zip(gus, parks))
    df_park = pd.DataFrame.from_dict([cnt_dict_park])
    df_park_sort = df_park.sort_values(by=0, axis=1, ascending=False)
    gus_sort = df_park_sort.columns.tolist()

    parks_sort = df_park_sort.T[0].tolist()
    plt.cla()
    colors = sns.color_palette('pastel')
    plt.pie(x=parks_sort, labels=gus_sort, colors=colors, autopct='%0.0f%%')

    ## 이미지 html로 변환:
    # graph를 메모리에 저장:
    img = io.BytesIO() # 메모리에 (디스크 말고) file-like object를 생성성
    plt.savefig(img, format='png') # file-like object로 이미지 save
    img.seek(0) # file-like object의 beginning으로 이동 to read it later

    # PNG data를 base 64 string으로 변환
    piedata = img.getvalue()
    pieb64 = base64.b64encode(piedata).decode()
    return HttpResponse(pieb64)
