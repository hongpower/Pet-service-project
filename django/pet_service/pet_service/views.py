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
    with open(f".\data\pet_{file_name}", 'r',
              encoding="utf-8") as f:
        dict_info = json.load(f)
    final_dict = dict()
    final_dict['info'] = dict_info[gu_name]
    pprint.pprint(final_dict)
    return JsonResponse(final_dict)


def index2(request):
    return render(request, 'index_jaewon.html')


path_json = './data/'


def Location_Map_Json(input_file, input_gu):
    # with open(f'{path}{input_file}.json', 'r', encoding='utf-8') as f:
    with open(f'./data/pet_{input_file}', 'r', encoding='utf-8') as f:
        total_json = json.load(f)

    center = addr_to_lat_lon(input_gu)
    # center_loc = folium.Map(location=[center[0],center[1]],zoom_start=14)
    center_loc = folium.Map(location=[center[0], center[1]], zoom_start=15, tiles='cartodbpositron')
    # print(total_json)
    gu_data = total_json[input_gu]
    print(gu_data)
    # local = []
    for gu in gu_data:
        gu_address = gu["address"]
        print(gu_address)
        local = addr_to_lat_lon(gu_address)
        folium.Marker([local[0], local[1]], popup=folium.Popup(gu['s_name'], max_width=100)).add_to(center_loc)

    center_loc.save('map.html')
    # ????
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

def drawMap(request):
    file_name = request.GET['business_name']
    gu_name = '강남구'
    my_loc = Location_Map_Json(file_name, gu_name)
    # maphtml은 무엇인가?
    return my_loc


def Map(request):
    input_file = request.GET['bs_id']
    input_gu = request.GET['gu_id']
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