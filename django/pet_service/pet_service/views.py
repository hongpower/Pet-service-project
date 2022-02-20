from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import pprint
import pandas as pd
import numpy as np
import warnings
import folium
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import urllib, base64
from io import BytesIO
import base64
# from Open_Api.conversion import addr_to_lat_lon

warnings.filterwarnings('ignore')


def index(request):
    return render(request, 'index.html')


def getGu(request):
    with open(".\data\gulist.json", 'r', encoding="utf-8") as f:
        dict_gus = json.load(f)
    # pprint.pprint(dict_gus)
    return JsonResponse(dict_gus)


def getBusiness(request):
    with open(".\data/business.json", 'r', encoding="utf-8") as f:
        dict_business = json.load(f)
    # pprint.pprint(dict_business)
    return JsonResponse(dict_business)


def getInfo(request):
    pprint.pprint('!!!!!!!!!!!!!!!')
    gu_name = request.GET['gu_id']
    pprint.pprint(gu_name)
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
        pprint.pprint(final_dict)
    return JsonResponse(final_dict)


def index2(request):
    return render(request, 'index_jaewon.html')


def Geo(request):
    return render(request,'geo.html')

def my_loc(request):
    pprint.pprint('!!!!!!!!!!!!!!!')
    lat = request.GET['lat']
    lon = request.GET['lon']
    print(lat)
    print(lon)
    # lat_lon_to_addr()
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
    print(gu_data)
    # local = []
    for gu in gu_data:
        gu_address = gu["address"]
        print(gu_address)
        local = addr_to_lat_lon(gu_address)
        folium.Marker([local[0], local[1]], popup=folium.Popup(gu['s_name'], max_width=100),
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
        print(i)
        try:
            local = addr_to_lat_lon(i)
        except IndexError as e:
            pass
        doro_add = hospital_data[hospital_data.도로명전체주소 == i]
        hosp_name = doro_add['사업장명'].values
        folium.Marker([local[0], local[1]], popup=folium.Popup(hosp_name[0], max_width=100),
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
        park_x = park_etc.위도.values
        # print(park_x)
        park_etc = city_park[city_park.공원명 == i]
        park_y = park_etc.경도.values
        # print(park_y)
        park_etc = city_park[city_park.공원명 == i]
        park_width = park_etc.공원면적.values
        # print(park_width)
        folium.Marker([park_x, park_y], popup=folium.Popup(i + f' 공원면적:{park_width}', max_width=200),
                      icon=folium.Icon(icon="tree",prefix='fa',color='green')).add_to(center_loc)
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

def drawMap(request):
    file_name = request.GET['business_name']
    gu_name = '강남구'
    my_loc = Location_Map_Json(file_name, gu_name)
    # maphtml은 무엇인가?
    return my_loc


def Map(request):
    input_file = request.GET['bs_id']
    input_gu = request.GET['gu_id']
    print(input_file)
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

    pprint.pprint(final_dict)
    return HttpResponse(maps)

def practice(request):
    return render(request, 'menu_practice.html')

def score(request):
    # if request.method =='GET':
        return render(request, 'score.html')
    # else:
    #     plt.rcParams['font.family'] = 'Malgun Gothic'
    #
    #     file_name = request.POST['business']
    #     if file_name == 'pet_city_park' or file_name == 'pet_hospital' or file_name == 'pet_medical':
    #         pass
    #     else:
    #         with open(f'.\data\{file_name}.json', 'r', encoding='utf-8') as f:
    #             pet_business_info = json.load(f)
    #         # print(petcafe_json)
    #         gus = pet_business_info.keys()
    #         # print(gus)
    #         cnt_dict = {}
    #         for gu in gus:
    #             cnt = len(pet_business_info[gu])
    #             cnt_dict[gu] = cnt
    #         # print(cnt_dict)
    #         tot = sum(cnt_dict.values())
    #         avg = tot / len(cnt_dict)
    #         df = pd.DataFrame.from_dict([cnt_dict])
    #         # print(df)
    #         # b.cla()
    #         plt.cla()
    #         b = sns.barplot(data=df, color='blue')
    #         # b.cla()
    #         b.axhline(y=avg, color='red', linestyle='dashed', label="평균")
    #         b.set_xticklabels(b.get_xticklabels(), rotation=45)
    #         # b.set_title('애견 공원 갯수')
    #
    #         buf = io.BytesIO()
    #         b_png = b.get_figure()
    #
    #         # graph를 dtring buffer로 바꾼 후에 64비트 코드로 바꾸고 이미지로
    #         b_png.savefig(buf, formant='png')
    #         buf.seek(0)
    #         string = base64.b64encode(buf.read())
    #         uri = urllib.parse.quote(string)
    #
    #         return render(request, 'score.html', {'data': uri})

def getScore(request):
    file_name = request.GET['business_name']
    plt.rcParams['font.family'] = 'Malgun Gothic'

    if file_name == 'pet_city_park' or file_name == 'pet_hospital' or file_name == 'pet_medical':
        df = pd.read_csv(".\data\whole_merged_data2.csv", sep=",")
        gus = df['지역명'].tolist()

        if file_name =='pet_city_park':
            bs = df['공원 개수'].tolist()
            title = '공원 갯수'
        elif file_name =='pet_medical':
            bs = df['동물약국'].tolist()
            title = '동물 약국 갯수'
        else:
            bs = df['병원수'].tolist()
            title = '병원 갯수'
        cnt_dict= dict(zip(gus, bs))
        tot = sum(cnt_dict.values())
        avg = tot / len(cnt_dict)
        df_bs = pd.DataFrame.from_dict([cnt_dict])
        a = sns.barplot(data=df_bs, color='blue')
        a.set_title(title)
        a.axhline(y=avg, color='red', linestyle='dashed', label="평균")
        a.set_xticklabels(a.get_xticklabels(), rotation=45)
        a_png = a.get_figure()
        a_png.savefig(f'./static/img/graph{file_name}.png')
        imgurl = f"/static/img/graph{file_name}.png"
        return HttpResponse(imgurl)
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
        # print(df)
        # b.cla()
        plt.cla()
        b = sns.barplot(data=df, color='blue')
        # b.cla()
        b.axhline(y=avg, color='red', linestyle='dashed', label="평균")
        b.set_xticklabels(b.get_xticklabels(), rotation=45)
        # b.set_title('애견 공원 갯수')

        # graph를 dtring buffer로 바꾼 후에 64비트 코드로 바꾸고 이미지로
        # buf = io.BytesIO()
        b_png = b.get_figure()
        print(os.path.isfile(f'./static/img/graph{file_name}.png'))
        b_png.savefig(f'./static/img/graph{file_name}.png')
        # b_png.savefig(buf, formant='png')
        # buf.seek(0)
        # string = base64.b64encode(buf.read())
        # uri = urllib.parse.quote(string)
        imgurl = f"/static/img/graph{file_name}.png"
        return HttpResponse(imgurl)

def getPie(request):
    ## 여기 미완성입니다!
    df = pd.read_csv(".\data\whole_merged_data2.csv", sep=",")
    df_park = pd.DataFrame.from_dict([cnt_dict_park])
    df_park_sort = df_park.sort_values(by=0, axis=1, ascending=False)
    gus_sort = df_park_sort.columns.tolist()

    parks_sort = df_park_sort.T[0].tolist()

    colors = sns.color_palette('pastel')
    pie = plt.pie(x=parks_sort, labels=gus_sort, colors=colors, autopct='%0.0f%%')

    buf = io.BytesIO()
    pie_png = pie.get_figure()

    # graph를 dtring buffer로 바꾼 후에 64비트 코드로 바꾸고 이미지로
    pie.savefig(buf, formant='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'score.html', {'data': uri})