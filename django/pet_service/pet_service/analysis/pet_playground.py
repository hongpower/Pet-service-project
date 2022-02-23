# -*- coding:utf-8 -*-

import folium
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

plt.rcParams['font.family'] = 'Malgun Gothic'

with open('pet_playground.json', 'r', encoding='utf-8') as f:
    petplayground_json = json.load(f)
# print(petcafe_json)
gus = petplayground_json.keys()
# print(gus)
cnt_dict = {}
for gu in gus:
    cnt = len(petplayground_json[gu])
    cnt_dict[gu] = cnt
df = pd.DataFrame.from_dict([cnt_dict])

tot = 0
for i in range(len(df.values[0])):
    tot += df.values[0][i]

pet_playground = df.columns.values
pet_playground_data = df.values
pet_playground_score = pd.DataFrame(pet_playground_data[0],index=pet_playground, columns=['playground'])
# print(pet_playground_score)