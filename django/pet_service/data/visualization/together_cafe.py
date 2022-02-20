# -*- coding:utf-8 -*-

import folium
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

plt.rcParams['font.family'] = 'Malgun Gothic'

with open('together_cafe.json', 'r', encoding='utf-8') as f:
    togethercafe_json = json.load(f)
# print(togethercafe_json)
gus = togethercafe_json.keys()
# print(gus)
cnt_dict = {}
for gu in gus:
    cnt = len(togethercafe_json[gu])
    cnt_dict[gu] = cnt
# print(cnt_dict)
tot = sum(cnt_dict.values())
avg = tot/len(cnt_dict)
df = pd.DataFrame.from_dict([cnt_dict])
# print(df)

b = sns.barplot(data=df,color='blue')
b.axhline(y=avg, color='red',linestyle='dashed', label="평균")
b.set_xticklabels(b.get_xticklabels(),rotation = 45)
b.set_title('애견 동반 카페 갯수')
plt.show()

# sns.barplot(data=cnt_dict, x='gu')
# plt.show()