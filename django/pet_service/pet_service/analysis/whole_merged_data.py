# -*- coding:utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'

df = pd.read_csv("whole_merged_data2.csv", sep=",")
# print(df)
gus = df['지역명'].tolist()
# print(gus)
together_restaurants = df['반려동물 동반 가능 식당'].tolist()
pharmacys = df['동물약국'].tolist()
parks = df['공원 개수'].tolist()

together_restaurants_tot = 0
phar_tot = 0
parks_tot = 0

for i in range(0, 25):
    together_restaurants_tot += together_restaurants[i]
    phar_tot += pharmacys[i]
    parks_tot += parks[i]

pet_together_restaurants = df['지역명'].values
pet_together_restaurants_data = [together_restaurants[i] for i in range(25)]
pet_together_restaurants_score = pd.DataFrame(pet_together_restaurants_data, index=pet_together_restaurants,
                                              columns=['together_restaurants'])
# print(pet_together_restaurants_score)

pet_phar = df['지역명'].values
pet_phar_data = [pharmacys[i] for i in range(25)]
pet_phar_score = pd.DataFrame(pet_phar_data, index=pet_phar, columns=['medical'])
# print(pet_phar_score)

pet_parks = df['지역명'].values
pet_parks_data = [parks[i] for i in range(25)]
pet_parks_score = pd.DataFrame(pet_parks_data, index=pet_parks, columns=['park'])
# print(pet_parks_score)

