import pandas as pd
import matplotlib.pyplot as plt
from django.http import JsonResponse, HttpResponse
import folium
import json
import io
import urllib, base64
from io import BytesIO
import seaborn as sns
def drawbargraph(file_name, user_loc):
    file_name = file_name
    plt.rcParams['font.family'] = 'Malgun Gothic'

    if file_name == 'pet_city_park' or file_name == 'pet_hospital' or file_name == 'pet_medical':
        df = pd.read_csv(".\data\whole_merged_data2.csv", sep=",")
        gus = df['지역명'].tolist()

        if file_name =='pet_city_park':
            bs = df['공원 개수'].tolist()
            title = '공원 개수'
        elif file_name =='pet_medical':
            bs = df['동물약국'].tolist()
            title = '동물 약국 개수'
        else:
            bs = df['병원수'].tolist()
            title = '병원 개수'
        cnt_dict= dict(zip(gus, bs))
        tot = sum(cnt_dict.values())
        avg = tot / len(cnt_dict)
        df_bs = pd.DataFrame.from_dict([cnt_dict])
        plt.cla()

        # a 리셋되도록 넣어놈
        a = file_name
        plt.figure()
        # lst: df의 컬럼명 list
        lst = list(df_bs.columns)
        # bs_index : 사용자 구(ex 강남구)의 lst내 인덱스
        bs_index = lst.index(user_loc)
        # 가장 큰 값
        maxCol = max(list(df_bs.loc[0]))
        clrs = ['grey' if x< maxCol else 'blue' for x in df_bs.loc[0]]
        # 사용자의 구는 초록색으로
        clrs[bs_index] = 'green'
        a = sns.barplot(data=df_bs, palette=clrs)
        a.set_title(title)
        a.axhline(y=avg, color='red', linestyle='dashed', label="평균")
        a.set_xticklabels(a.get_xticklabels(), rotation=45)

        buf = io.BytesIO()
        a_png = a.get_figure()
        a_png.savefig(buf, format='png')
        buf.seek(0)

        data = buf.getvalue()
        b64 = base64.b64encode(data).decode()
        return b64

    else:
        with open(f'.\data\{file_name}.json', 'r', encoding='utf-8') as f:
            pet_business_info = json.load(f)
        # print(petcafe_json)
        gus = pet_business_info.keys()
        # print(gus)
        cnt_dict = {}
        for gu in gus:
            cnt = len(pet_business_info[gu])
            cnt_dict[gu] = cnt
        # print(cnt_dict)
        tot = sum(cnt_dict.values())
        avg = tot / len(cnt_dict)
        df = pd.DataFrame.from_dict([cnt_dict])
        with open(".\data/business.json", 'r', encoding="utf-8") as f:
            dict_business = json.load(f)
        title_lst = dict_business['business']
        bs_id_lst = dict_business['id']
        bs_id_lst = ['pet_'+bs for bs in bs_id_lst]
        title_dict = dict(zip(bs_id_lst, title_lst))
        plt.cla()
        plt.figure()
        lst = list(df.columns)
        bs_index = lst.index(user_loc)
        maxCol = max(list(df.loc[0]))
        clrs = ['grey' if x< maxCol else 'blue' for x in df.loc[0]]
        clrs[bs_index] = 'green'
        b = sns.barplot(data=df, palette=clrs)
        b.axhline(y=avg, color='red', linestyle='dashed', label="평균")
        b.set_xticklabels(b.get_xticklabels(), rotation=45)
        b.set_title(title_dict[file_name+'.json']+' 개수')

        # graph를 dtring buffer로 바꾼 후에 64비트 코드로 바꾸고 이미지로
        buf = io.BytesIO()
        b_png = b.get_figure()
        b_png.savefig(buf, format='png')
        buf.seek(0)

        data = buf.getvalue()
        b64 = base64.b64encode(data).decode()
        return b64

def createMap():
    df = pd.read_csv('./data/score.csv')
    geo_path = './data/seoul_json.json'
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

    my_loc.save('./templates/map4.html')
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
    # figsize(가로길이, 세로길이)
    plt.figure(figsize=(15,12))
    fig, ax = plt.subplots(figsize=(13,10))
    colors = sns.color_palette('Set3',12)
    explode = [0.18 for _ in range(len(gus))]
    wedgeprops = {'width' : 0.65, 'edgecolor': 'black', 'linewidth': 1}
    ax.pie(x=parks_sort,
           labels=gus_sort,
           colors=colors,
           autopct='%0.00f%%',
           explode=explode,
           shadow=False,
           wedgeprops=wedgeprops,
           textprops={'fontsize':10},
           labeldistance=1.1
           )
    ax.set_title('공원 개수 구별 현황', pad=35, fontsize=20)
    plt.legend(gus_sort,title='ingredients',bbox_to_anchor=(1.27,1))
    # get current figure
    fig2 = plt.gcf()
    buf = io.BytesIO()
    fig2.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return string