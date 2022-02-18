from django.shortcuts import render
from django.http import JsonResponse
import json
import pprint
import pandas as pd
import numpy as np
import warnings
import folium
from Open_Api.conversion import addr_to_lat_lon
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
    with open(f"C:\workspaces\project_visualization\django\pet_service\data\pet_{file_name}", 'r', encoding="utf-8") as f:
        dict_info = json.load(f)
    final_dict = dict()
    final_dict['info'] = dict_info[gu_name]
    pprint.pprint(final_dict)
    return JsonResponse(final_dict)

def index2(request):
    return render(request, 'index_jaewon.html')

path_json = './data/'

def Map(request):
    if request.method == 'POST':
        input_file = request.POST['pet_cafe']
        input_gu = request.POST['강남구']
        my_loc = Location_Map_Json(path_json,input_file,input_gu)
        maps = my_loc._repr_html_()
        return render(request,'map.html',{'my_loc': maps})
    elif request.method == 'GET':
        a = 37.5752205086784
        b = 127.010502773568

        my_loc = folium.Map(location=[37.5752205086784, 127.010502773568], zoom_start=18)
        folium.Marker([37.5752205086784, 127.010402773568], popup=folium.Popup('이쁜아이 공원면적:가능?', max_width=100),
                      icon=folium.Icon(color="green", icon='cloud'), ).add_to(my_loc)

        maps = my_loc._repr_html_()  # 지도를 템플릿에 iframe로 찍어줌
        return render(request, 'map.html', {'my_loc': maps})

def Location_Map_Json(path,input_file,input_gu):

    with open(f'{path}{input_file}.json', 'r', encoding='utf-8') as f:
        total_json = json.load(f)

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
        folium.Marker([local[0], local[1]], popup=folium.Popup(gu['s_name'], max_width=100)).add_to(center_loc)

    center_loc.save('map.html')
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

