from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import pprint
import pandas as pd
import numpy as np
import warnings
import folium
import requests
# from Open_Api.conversion import addr_to_lat_lon

warnings.filterwarnings('ignore')


def index(request):
    return render(request, 'index.html')


def getGu(request):
    with open("C:\workspaces\project_visualization\django\pet_service\data\gulist.json", 'r', encoding="utf-8") as f:
        dict_gus = json.load(f)
    # pprint.pprint(dict_gus)
    return JsonResponse(dict_gus)


def getBusiness(request):
    with open("C:\workspaces\project_visualization\django\pet_service\data/business.json", 'r', encoding="utf-8") as f:
        dict_business = json.load(f)
    # pprint.pprint(dict_business)
    return JsonResponse(dict_business)


def getInfo(request):
    pprint.pprint('!!!!!!!!!!!!!!!')
    gu_name = request.GET['gu_id']
    pprint.pprint(gu_name)
    file_name = request.GET['bs_id']
    with open(f"C:\workspaces\project_visualization\django\pet_service\data\pet_{file_name}", 'r',
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

