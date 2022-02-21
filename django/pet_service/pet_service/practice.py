import pandas as pd
import matplotlib.pyplot as plt
import folium
import json

def createMap():
    df = pd.read_csv('./scores.csv')
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

    # hospital_data = pd.read_csv(f'./csv/{input_file}',  sep=",")
    # medical = hospital_data.동물약국
    # hospital = hospital_data.병원수
    # local = hospital_data.지역명
    # total = hospital + medical
    #
    #
    # plt.figure(figsize=(15,10))
    #
    # ax = sns.barplot(data=hospital_data,x=local,y=hospital,color='r',alpha = 0.3,label='hospital')
    # ax = sns.barplot(data=hospital_data,x=local,y=medical,color = 'b',alpha=0.3,label='medical')

    json_json = pd.read_csv(f'./csv/{input_file}',  sep=",")
    local = json_json.지역명
    cafe = json_json['pet_cafe.json']
    together = json_json['together_cafe.json']
    diner = json_json['together_diner.json']

    ax = sns.barplot(data=json_json,x=local,y=cafe,color='r',alpha = 0.3,label='cafe')
    ax = sns.barplot(data=json_json,x=local,y=together,color = 'b',alpha=0.3,label='together_cafe')
    ax = sns.barplot(data=json_json,x=local,y=diner,color = 'g',alpha=0.3,label='diner')

    plt.legend(loc = 'upper right')
    ax.set_ylabel("Count", fontsize = 20)
    plt.xlim(-1,25)
    # plt.show()

    buf = io.BytesIO()
    ax_png = ax.get_figure()
    ax_png.savefig(buf, format='png')
    buf.seek(0)

    data = buf.getvalue()
    b64 = base64.b64encode(data).decode()
    
    return b64