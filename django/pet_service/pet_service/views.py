from django.shortcuts import render
from django.http import JsonResponse
import json
import pprint

def index(request):
    return render(request, 'index.html')

def getGu(request):
    with open("C:\workspaces\project_visualization\django\pet_service\pet_service\data\pet_salon.json", 'r', encoding="utf-8") as f:
        json_pet_cafe = json.load(f)

    pprint.pprint(json_pet_cafe)
    pprint.pprint(type(json_pet_cafe))

    # dict_pet_cafe = json.loads(json_pet_cafe)
    # 키 값을 가져와야함
    gu_list= [x for x in dict_pet_cafe]
    gus = ['gu' for x in range(20)]
    gu_dict = dict(zip(gus, gu_list))
    gu_dict2 = {'제발': '되어줘', '이것도':'될까'}
    return JsonResponse(gu_dict)