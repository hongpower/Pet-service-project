from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

def index(request):
    return render(request, 'index.html')

def getGu(request):
    with open("./data/pet_cafe.json", 'r', encoding="utf-8") as f:
        data = f.read()
    data_ = json.loads(data)
    print(data_)
    return JsonResponse(data_)