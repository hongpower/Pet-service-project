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

def Map(request):

    a = 37.5752205086784
    b = 127.010502773568

    my_loc = folium.Map(location=[37.5752205086784, 127.010502773568], zoom_start=18)
    folium.Marker([37.5752205086784, 127.010402773568], popup=folium.Popup('이쁜아이 공원면적:가능?', max_width=100),
                  icon=folium.Icon(color="green", icon='cloud'), ).add_to(my_loc)

    maps = my_loc._repr_html_()  # 지도를 템플릿에 iframe로 찍어줌
    return render(request,'map.html',{'my_loc' : maps})


def Busan(request):
    my_loc = folium.Map(location=[35.1799147675317, 129.07493824909042], zoom_start=18)
    folium.Marker([35.1799147675317, 129.07493824909042], popup=folium.Popup('이쁜아이 공원면적:가능?', max_width=100),
                  icon=folium.Icon(color="green", icon='cloud'), ).add_to(my_loc)

    maps = my_loc._repr_html_()  # 지도를 템플릿에 iframe로 찍어줌
    return render(request, 'busan.html', {'my_loc': maps})