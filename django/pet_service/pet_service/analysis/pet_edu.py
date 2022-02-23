# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

# 카페 가중치
import json

plt.rcParams['font.family'] = 'Malgun Gothic'

with open('pet_education_center.json', 'r', encoding='utf-8') as f:
    petedu_json = json.load(f)

gus = petedu_json.keys()

cnt_dict = {}
for gu in gus:
    cnt = len(petedu_json[gu])
    cnt_dict[gu] = cnt

df = pd.DataFrame.from_dict([cnt_dict])
# print(df.values)


tot = 0
for i in range(len(df.values[0])):
    tot += df.values[0][i]
# print((df.values / tot).round(2))


pet_edu = df.columns.values
pet_edu_data = df.values
pet_edu_score = pd.DataFrame(pet_edu_data[0], index=pet_edu, columns=['education_center'])
# print(pet_edu_score)
