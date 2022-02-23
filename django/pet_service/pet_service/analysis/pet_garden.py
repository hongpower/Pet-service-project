# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import json

plt.rcParams['font.family'] = 'Malgun Gothic'

with open('pet_garden.json', 'r', encoding='utf-8') as f:
    petgarden_json = json.load(f)
gus = petgarden_json.keys()
cnt_dict = {}
for gu in gus:
    cnt = len(petgarden_json[gu])
    cnt_dict[gu] = cnt
df = pd.DataFrame.from_dict([cnt_dict])

tot = 0
for i in range(len(df.values[0])):
    tot += df.values[0][i]

pet_garden = df.columns.values
pet_garden_data = df.values
pet_garden_score = pd.DataFrame(pet_garden_data[0],index=pet_garden, columns=['garden'])
# print(pet_garden_score)