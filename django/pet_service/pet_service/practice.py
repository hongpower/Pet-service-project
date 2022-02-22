import pandas as pd
import matplotlib.pyplot as plt
import folium
import json
import io
import urllib, base64
from io import BytesIO
import seaborn as sns

def createMap():
    df = pd.read_csv('./score.csv')
    geo_path = './seoul_json.json'
    geo_str = json.load(open(geo_path, encoding='utf-8'))
    df=df.set_index('id')
    my_loc = folium.Map(location=[37.58,127.0],
                        zoom_start=11,
                        tiles='cartodbpositron'
                       )
    chro = folium.Choropleth(geo_data=geo_str,
                        data=df['score'],
                        columns=[df.index, df['score']],
                        fill_color='YlGnBu',
                        key_on='feature.properties.name',
                        legend_Name='서울 구별 점수',
                        fill_opacity=0.6,
                        line_opacity=0.8,
                        dash_array='5',
                        weight = 3,
                        ).add_to(my_loc)
    folium.LayerControl().add_to(my_loc)
    chro.geojson.add_child(folium.features.GeoJsonTooltip(['name','name_eng'], labels=False))

    my_loc.save('map4.html')
    return my_loc


def drawgraph():
    input_file = 'whole_merged_data2.csv'
    plt.rcParams['font.family'] = 'Malgun Gothic'

    json_json = pd.read_csv(f'./data/{input_file}',  sep=",")
    local = json_json.지역명
    cafe = json_json['pet_cafe.json']
    together = json_json['together_cafe.json']
    diner = json_json['together_diner.json']
    # plt.cla()
    plt.figure()
    fig, ax = plt.subplots()
    width = 0.35
    # ax = plt.bar(x=local, height=cafe, color='r', alpha=0.3, label='cafe', stacked=True)
    ax.bar(x=local, height=cafe, color='r', alpha=0.3, label='cafe')
    ax.bar(x=local, height=together, bottom=cafe, color='b', alpha=0.3, label='together_cafeeee')
    ax.bar(x=local, height=diner, bottom=cafe+together, color='g', alpha=0.3, label='diner')

    plt.legend(loc='upper right')
    plt.xticks(rotation=45)
    plt.ylabel("Count", fontsize=20)
    plt.xlim(-1, 25)
    plt.title('동반 가능한 식당 및 카페 구별 현황')

    fig = plt.gcf()
    buf = io.BytesIO()
    # ax_png = ax.get_figure()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    
    return string

def drawpie():
    ## 파이 그래프 생성 함수:
    df = pd.read_csv(".\data\whole_merged_data2.csv", sep=",")
    gus = df['지역명'].tolist()
    parks = df['공원 개수'].tolist()
    cnt_dict_park = dict(zip(gus, parks))
    df_park = pd.DataFrame.from_dict([cnt_dict_park])
    df_park_sort = df_park.sort_values(by=0, axis=1, ascending=False)
    gus_sort = df_park_sort.columns.tolist()

    parks_sort = df_park_sort.T[0].tolist()
    # plt.cla()
    plt.figure()
    fig, ax = plt.subplots()
    colors = sns.color_palette('pastel')
    ax.pie(x=parks_sort, labels=gus_sort, colors=colors, autopct='%0.0f%%')
    ax.set_title('공원 개수 구별 현황')
    # get current figure
    fig2 = plt.gcf()
    buf = io.BytesIO()
    fig2.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return string