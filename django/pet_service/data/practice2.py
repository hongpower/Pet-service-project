import pandas as pd
import matplotlib.pyplot as plt
import folium
import json
import io
import urllib, base64
from io import BytesIO
import seaborn as sns
import numpy as np

def scatterplot():
    plt.rcParams['font.family'] = 'Malgun Gothic'

    df = pd.read_csv("whole_merged_data2.csv", sep=",")
    df2 = df.sort_values('구별 총 생산')
    # print(df)
    # print(df2)
    gus = df2['지역명'].tolist()
    df_facility = df2.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
    list_GRDP = df2['구별 총 생산'].tolist()
    list_population = df2['인구'].tolist()
    # print(list_GRDP)
    # print(list_population)

    list_facility_tot = df_facility.sum(axis=1).tolist()
    # print(list_facility_tot)

    # df1=pd.concat([df_GRDP,df_population,df_facility_tot], axis=1)
    # print(df1)

    size = np.array(list_population) / 300  # 마커 사이즈 (인구)

    plt.figure(figsize=(15, 8))
    n = len(list_GRDP)
    r = 2 * np.random.rand(n)
    theta = 2 * np.pi * np.random.rand(n)
    area = 200 * r ** 2 * np.random.rand(n)
    colors = theta

    sns.regplot(x=list_GRDP, y=list_facility_tot, color='black')
    plt.scatter(x=list_GRDP, y=list_facility_tot, s=600, c='gray', cmap=plt.cm.cool, marker='o', alpha=1, linewidth=1,
                edgecolors='black')
    plt.ylabel('총 시설 개수')
    plt.xlabel('구별 총 생산')
    print(np.corrcoef(list_GRDP, list_facility_tot))
    for list_GRDP,list_facility_tot,gus in zip(list_GRDP,list_facility_tot,gus):
        plt.text(list_GRDP,list_facility_tot,gus)
    plt.show()
    fig2 = plt.gcf()
    buf = io.BytesIO()
    fig2.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    # return string

scatterplot()