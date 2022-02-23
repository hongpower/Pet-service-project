# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import json

plt.rcParams['font.family'] = 'Malgun Gothic'

with open('pet_store.json', 'r', encoding='utf-8') as f:
    petstore_json = json.load(f)
gus = petstore_json.keys()
cnt_dict = {}
for gu in gus:
    cnt = len(petstore_json[gu])
    cnt_dict[gu] = cnt
df = pd.DataFrame.from_dict([cnt_dict])

tot = 0
for i in range(len(df.values[0])):
    tot += df.values[0][i]

pet_store = df.columns.values
pet_store_data = df.values
pet_store_score = pd.DataFrame(pet_store_data[0],index=pet_store, columns=['store'])
# print(pet_store_score)