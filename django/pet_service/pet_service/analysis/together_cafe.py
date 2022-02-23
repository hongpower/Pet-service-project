# -*- coding:utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import json

plt.rcParams['font.family'] = 'Malgun Gothic'

with open('pet_together_cafe.json', 'r', encoding='utf-8') as f:
    togethercafe_json = json.load(f)
gus = togethercafe_json.keys()
cnt_dict = {}
for gu in gus:
    cnt = len(togethercafe_json[gu])
    cnt_dict[gu] = cnt
df = pd.DataFrame.from_dict([cnt_dict])

tot = 0
for i in range(len(df.values[0])):
    tot += df.values[0][i]

pet_together_cafe = df.columns.values
pet_together_cafe_data = df.values
pet_together_cafe_score = pd.DataFrame(pet_together_cafe_data[0], index=pet_together_cafe, columns=['together_cafe'])
# print(pet_together_cafe_score)
