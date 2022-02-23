# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import json

plt.rcParams['font.family'] = 'Malgun Gothic'

with open('pet_salon.json', 'r', encoding='utf-8') as f:
    petsalon_json = json.load(f)
gus = petsalon_json.keys()
cnt_dict = {}
for gu in gus:
    cnt = len(petsalon_json[gu])
    cnt_dict[gu] = cnt
df = pd.DataFrame.from_dict([cnt_dict])

tot = 0
for i in range(len(df.values[0])):
    tot += df.values[0][i]

pet_salon = df.columns.values
pet_salon_data = df.values
pet_salon_score = pd.DataFrame(pet_salon_data[0],index=pet_salon, columns=['salon'])
# print(pet_salon_score)