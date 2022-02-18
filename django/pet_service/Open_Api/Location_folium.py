# -*- coding:utf-8 -*-
# 파일 공유시 한글파일 명 때문에 에러 발생 --> 임의로 영어로 바꿔줌
import requests
import pandas as pd
import numpy as np
import warnings
import json
import folium
from conversion import addr_to_lat_lon
warnings.filterwarnings('ignore')

path_json = '../Open_Api/json_total/'
def Location_Map_Json(path,input_file,input_gu):

    with open(f'{path}{input_file}.json', 'r', encoding='utf-8') as f:
        total_json = json.load(f)

    center = addr_to_lat_lon(input_gu)
    center_loc = folium.Map(location=[center[0],center[1]],zoom_start=14)
    # print(total_json)
    gu_data = total_json[input_gu]
    print(gu_data)
    # local = []
    for gu in gu_data:
        gu_address = gu["address"]
        print(gu_address)
        local = addr_to_lat_lon(gu_address)
        folium.Marker([local[0], local[1]], popup=folium.Popup(gu['s_name'], max_width=100)).add_to(center_loc)


    center_loc.save('pratice.html')

# 약국 medical 은  똑같은데 encoding를  cp949 로 해줘야함
path_csv = './csv/'
def Location_Medical_CSV(path,input_gu,num):
    if num == 1:
        hospital_data = pd.read_csv(f'{path}hospital.csv', encoding='euc-kr')
    elif num == 2:
        hospital_data = pd.read_csv(f'{path}medical.csv', encoding='cp949')
    # print(hospital_data)
    hospital_data
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
        print(i)
        try:
            local = addr_to_lat_lon(i)
        except IndexError as e:
            pass
        doro_add = hospital_data[hospital_data.도로명전체주소 == i]
        hosp_name = doro_add['사업장명'].values
        folium.Marker([local[0], local[1]], popup=folium.Popup(hosp_name[0], max_width=100),icon=folium.Icon(color="green",icon='cloud'),).add_to(center_loc)

    center_loc.save('pratice.html')

def Location_Park(path,input_gu):
    city_park = pd.read_csv(f'{path}city_park.csv', encoding='cp949')
    # print(city_park)
    city_park = city_park[['공원명', '전화번호', '소재지지번주소','공원구분', '위도', '경도','공원면적']]
    # city_park = city_park.loc[city_park['상세영업상태명'] == '정상']
    city_park = city_park.fillna(0)
    city_park = city_park[city_park['소재지지번주소'].str.contains(f'서울특별시 {input_gu}', na=False)]
    print(city_park)

    center = addr_to_lat_lon(input_gu)
    center_loc = folium.Map(location=[center[0], center[1]], zoom_start=12)
    # 공원면적하고 공원명이 돌면서 위도랑 경도 빼기

    park_name = city_park['공원명']
    # print(park_name)
    # print(city_park[['위도','경도']])

    for i in park_name:
        print(i)
        park_etc = city_park[city_park.공원명 == i]
        park_x = park_etc.위도.values
        # print(park_x)
        park_etc = city_park[city_park.공원명 == i]
        park_y = park_etc.경도.values
        # print(park_y)
        park_etc = city_park[city_park.공원명 == i]
        park_width = park_etc.공원면적.values
        # print(park_width)
        folium.Marker([park_x, park_y], popup=folium.Popup(i+f' 공원면적:{park_width}', max_width=200)).add_to(center_loc)

    center_loc.save('pratice.html')

# input_csv = input('csv 파일명 입력 : ')
# input_file = input('파일이름 입력 : ')
input_file = 'together_diner'
# input_gu = input('구 입력: ')
input_gu = '강남구'

# Location_Map_Json(path_json,input_file,input_gu)
Location_Medical_CSV(path_csv,input_gu,2)
# Location_Park(path_csv,input_gu)





