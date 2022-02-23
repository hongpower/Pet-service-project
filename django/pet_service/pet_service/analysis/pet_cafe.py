# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

# 카페 가중치
import json
plt.rcParams['font.family'] = 'Malgun Gothic'

with open('pet_cafe.json', 'r', encoding='utf-8') as f:
    petcafe_json = json.load(f)

gus = petcafe_json.keys()

cnt_dict = {}
for gu in gus:
    cnt = len(petcafe_json[gu])
    cnt_dict[gu] = cnt

df = pd.DataFrame.from_dict([cnt_dict])
# print(df.values)

tot = 0
for i in range(len(df.values[0])):
    tot += df.values[0][i]
# print((df.values/tot).round(2))

pet_cafe = df.columns.values
pet_cafe_data = df.values
pet_cafe_score = pd.DataFrame(pet_cafe_data[0],index = pet_cafe, columns=['cafe'])
# print(pet_cafe_score)