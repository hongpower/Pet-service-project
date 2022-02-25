import pandas as pd
import matplotlib.pyplot as plt
from django.http import JsonResponse, HttpResponse
import folium
import json
import io
import urllib, base64
from io import BytesIO
import seaborn as sns
import numpy as np

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
                        zoom_start=12,
                        tiles='cartodbpositron'
                       )
    chro = folium.Choropleth(geo_data=geo_str,
                        data=df['score'],
                        columns=[df.index, df['score']],
                        fill_color='YlGnBu',
                        key_on='feature.properties.name',
                        legend_Name='서울 구별 점수',
                        fill_opacity=0.8,
                        line_opacity=0.9,
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
    ax.bar(x=local, height=cafe, color='r', alpha=0.3, label='애견카페')
    ax.bar(x=local, height=together, bottom=cafe, color='b', alpha=0.3, label='동반가능 카페')
    ax.bar(x=local, height=diner, bottom=cafe+together, color='g', alpha=0.3, label='동반가능 식당')

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
    # df = pd.read_csv(".\data\whole_merged_data2.csv", sep=",")
    # gus = df['지역명'].tolist()
    # parks = df['공원 개수'].tolist()
    # cnt_dict_park = dict(zip(gus, parks))
    # df_park = pd.DataFrame.from_dict([cnt_dict_park])
    # df_park_sort = df_park.sort_values(by=0, axis=1, ascending=False)
    # gus_sort = df_park_sort.columns.tolist()
    #
    # parks_sort = df_park_sort.T[0].tolist()
    # # plt.cla()
    # # figsize(가로길이, 세로길이)
    # plt.figure(figsize=(15,12))
    # fig, ax = plt.subplots(figsize=(13,10))
    # colors = sns.color_palette('Set3',12)
    # explode = [0.18 for _ in range(len(gus))]
    # wedgeprops = {'width' : 0.65, 'edgecolor': 'black', 'linewidth': 1}
    # ax.pie(x=parks_sort,
    #        labels=gus_sort,
    #        colors=colors,
    #        autopct='%0.00f%%',
    #        explode=explode,
    #        shadow=False,
    #        wedgeprops=wedgeprops,
    #        textprops={'fontsize':10},
    #        labeldistance=1.1
    #        )
    # ax.set_title('공원 개수 구별 현황', pad=35, fontsize=20)
    # plt.legend(gus_sort,title='ingredients',bbox_to_anchor=(1.27,1))
    # get current figure
    ### new!!!
    df = pd.read_csv("./data/industry.csv", sep=",")
    name = df['시설 분류'].tolist()
    industry = df['비율'].tolist()
    cnt_dict_industry = dict(zip(name, industry))
    df_industry = pd.DataFrame.from_dict([cnt_dict_industry])
    df_industry_sort = df_industry.sort_values(by=0, axis=1, ascending=False)
    name_sort = df_industry_sort.columns.tolist()

    color_lst = ['#FF6A5A', '#FFBE59', '#CCCCFF', '#5EFF98', '#92EAFF', '#5B52FF', '#E12EFF', '#FF81B5', '#FF004E',
                 '#85DF9D', '#FFB02C', '#E0B9ED']

    industry_sort = df_industry_sort.T[0].tolist()

    # plt.cla()
    # figsize(가로길이, 세로길이)
    # plt.figure(figsize=(15, 12))
    fig = plt.figure(figsize=(18, 12))
    ax01 = fig.add_subplot(1, 2, 1)
    colors = color_lst
    explode = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.3, 0.5]
    wedgeprops = {'width': 0.65, 'edgecolor': 'black', 'linewidth': 1}
    ax01.pie(x=industry_sort,
             labels=name_sort,
             colors=color_lst,
             autopct='%0.01f%%',
             explode=explode,
             shadow=False,
             wedgeprops=wedgeprops,
             textprops={'fontsize': 8},
             labeldistance=1.1
             )

    ax01.set_title('서울시 애견시설 현황', pad=35, fontsize=20)
    # get current figure
    # fig2 = plt.gcf()
    # buf = io.BytesIO()
    # fig2.savefig(buf, format='png')
    # buf.seek(0)
    # string = base64.b64encode(buf.read())
    # return string

    df2 = pd.read_csv("./data/survey.csv", sep=",")
    name2 = df2['시설 분류'].tolist()
    industry2 = df2['비율'].tolist()
    cnt_dict_industry2 = dict(zip(name2, industry2))
    df_survey = pd.DataFrame.from_dict([cnt_dict_industry2])
    df_bs_sort = df_survey.sort_values(by=0, axis=1, ascending=False)

    bs_sort = df_bs_sort.columns.tolist()
    survey_sort = df_bs_sort.T[0].tolist()

    color_dict_name = dict(zip(name_sort, color_lst))
    color_lst2 = list()
    for bs in bs_sort:
        color_lst2.append(color_dict_name[bs])

    # plt.cla()
    # figsize(가로길이, 세로길이)
    # plt.figure(figsize=(15, 12))
    ax02 = fig.add_subplot(1, 2, 2)
    colors = sns.color_palette('Set3', 12)
    explode = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.3, 0.5]
    wedgeprops = {'width': 0.65, 'edgecolor': 'black', 'linewidth': 1}
    ax02.pie(x=survey_sort,
             labels=bs_sort,
             colors=color_lst2,
             autopct='%0.01f%%',
             explode=explode,
             shadow=False,
             wedgeprops=wedgeprops,
             textprops={'fontsize': 8},
             labeldistance=1.1
             )

    ax02.set_title('반려인 시설이용 경험', pad=35, fontsize=20)
    fig2 = plt.gcf()
    buf = io.BytesIO()
    fig2.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return string

def drawbox():
    ## 박스플롯
    plt.rcParams['font.family'] = 'Malgun Gothic'

    df = pd.read_csv("./data/whole_merged_data2.csv", sep=",")
    column_names = list(df.columns)
    gus = df['지역명'].tolist()

    train_a = df['Education_Center.json'].tolist()
    play_a = df['pet_cafe.json'].tolist()
    train_b = df['pet_garden.json'].tolist()
    train_c = df['pet_hotel.json'].tolist()
    play_b = df['Pet_playground.json'].tolist()
    beauty_a = df['pet_salon.json'].tolist()
    shop_a = df['pet_store.json'].tolist()
    together_a = df['together_cafe.json'].tolist()
    together_b = df['반려동물 동반 가능 식당'].tolist()
    hosp_a = df['동물약국'].tolist()
    play_c = df['공원 개수'].tolist()
    hosp_b = df['병원수'].tolist()
    group_size = 6

    label_lst = ['애견 교육 시설', '애견 유치원', '애견 호텔', '애견 카페', '반려견 놀이터', '공원', '동반가능 카페', '동반가능 식당', '동물약국', '동물병원',
                 '애견 미용실', '애견 스토어']
    y_lst = [train_a, train_b, train_c, play_a, play_b, play_c, together_a, together_b, hosp_a, hosp_b, beauty_a,
             shop_a]

    grp0 = list(zip(label_lst[0:3], y_lst[0:3]))
    grp_color0 = ['blue' for _ in range(len(grp0))]
    grp1 = list(zip(label_lst[3:6], y_lst[3:6]))
    grp_color1 = ['brown' for _ in range(len(grp1))]
    grp2 = list(zip(label_lst[6:8], y_lst[6:8]))
    grp_color2 = ['green' for _ in range(len(grp2))]
    grp3 = list(zip(label_lst[8:10], y_lst[8:10]))
    grp_color3 = ['red' for _ in range(len(grp3))]
    grp4 = list(zip(label_lst[10:11], y_lst[10:11]))
    grp_color4 = ['purple' for _ in range(len(grp4))]
    grp5 = list(zip(label_lst[11:12], y_lst[11:12]))
    grp_color5 = ['pink' for _ in range(len(grp5))]

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))
    plt.suptitle('서울시 애견 업종별 분포')
    totalcolor = grp_color0 + grp_color1 + grp_color2 + grp_color3 + grp_color4 + grp_color5

    violin = ax1.violinplot(y_lst, showmeans=True)
    ax1.set_xticklabels(label_lst, fontsize=8)
    ax1.set_xticks(np.arange(1, 13))
    for i in range(len(y_lst)):
        violin['bodies'][i].set_facecolor(totalcolor[i])
        violin['cbars'].set_edgecolor('gray')
        violin['cmaxes'].set_edgecolor('gray')
        violin['cmins'].set_edgecolor('gray')
        violin['cmeans'].set_edgecolor('gray')

    boxplot = ax2.boxplot(y_lst, patch_artist=True, whiskerprops={'color': 'gray'}, medianprops={'color': 'gray'})
    ax2.set_xticklabels(label_lst, fontsize=8)
    ax2.set_xticks(np.arange(1, 13))
    for patch, color in zip(boxplot['boxes'], totalcolor):
        patch.set_alpha(0.3)
        patch.set_edgecolor('gray')
        patch.set_facecolor(color)
        patch.set_linewidth(2)
    plt.setp(boxplot['fliers'], markeredgecolor='black')
    plt.tight_layout()
    # plt.show()
    fig2 = plt.gcf()
    buf = io.BytesIO()
    fig2.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return string

def scatterplot():
    plt.rcParams['font.family'] = 'Malgun Gothic'

    df = pd.read_csv("./data/whole_merged_data2.csv", sep=",")
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
    # for list_GRDP,list_facility_tot,gus in zip(list_GRDP,list_facility_tot,gus):
    #     plt.text(list_GRDP,list_facility_tot,gus)
    # plt.show()
    fig2 = plt.gcf()
    buf = io.BytesIO()
    fig2.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return string