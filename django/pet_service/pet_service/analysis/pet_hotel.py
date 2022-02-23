# -*- coding:utf-8 -*-
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

plt.rcParams['font.family'] = 'Malgun Gothic'

with open('pet_hotel.json', 'r', encoding='utf-8') as f:
    pethotel_json = json.load(f)
# print(pethotel_json)
gus = pethotel_json.keys()
# print(gus)
cnt_dict = {}
for gu in gus:
    cnt = len(pethotel_json[gu])
    cnt_dict[gu] = cnt
df = pd.DataFrame.from_dict([cnt_dict])

tot = 0
for i in range(len(df.values[0])):
    tot += df.values[0][i]

pet_hotel = df.columns.values
pet_hotel_data = df.values
pet_hotel_score = pd.DataFrame(pet_hotel_data[0],index=pet_hotel, columns=['hotel'])
# print(pet_hotel_score)