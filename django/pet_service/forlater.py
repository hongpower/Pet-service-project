def getScore(request):
    plt.rcParams['font.family'] = 'Malgun Gothic'

    with open('.\data\pet_garden.json', 'r', encoding='utf-8') as f:
        petgarden_json = json.load(f)
    # print(petcafe_json)
    gus = petgarden_json.keys()
    # print(gus)
    cnt_dict = {}
    for gu in gus:
        cnt = len(petgarden_json[gu])
        cnt_dict[gu] = cnt
    # print(cnt_dict)
    tot = sum(cnt_dict.values())
    avg = tot / len(cnt_dict)
    df = pd.DataFrame.from_dict([cnt_dict])
    # print(df)

    b = sns.barplot(data=df, color='blue')
    b.axhline(y=avg, color='red', linestyle='dashed', label="평균")
    b.set_xticklabels(b.get_xticklabels(), rotation=45)
    b.set_title('애견 공원 갯수')

    buf = io.BytesIO()
    b_png = b.get_figure()
    # b_png.savefig('./foo.png')
    # graph를 dtring buffer로 바꾼 후에 64비트 코드로 바꾸고 이미지로
    b_png.savefig(buf, formant='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    pprint.pprint(string)
    uri = urllib.parse.quote(string)
    pprint.pprint(type(string))
    pprint.pprint(type(uri))
    # pprint.pprint(uri)
    return uri
    # sns.barplot(data=cnt_dict, x='gu')
    # plt.savefig('')
    # plt.show()

# 기존 산점도 관련 함수 2개 가져다 놓기
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

    sns.regplot(x=list_facility_tot, y=list_GRDP, color='black')
    plt.scatter(x=list_facility_tot, y=list_GRDP, s=size, c=colors, cmap=plt.cm.cool, marker='o', alpha=1, linewidth=1,
                edgecolors='black')
    plt.xlabel('총 시설 개수')
    plt.ylabel('구별 총 생산')

    # for list_facility_tot,list_GRDP,gus in zip(list_facility_tot,list_GRDP,gus):
    #     plt.text(list_facility_tot,list_GRDP,gus)
    # plt.show()
    fig2 = plt.gcf()
    buf = io.BytesIO()
    fig2.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return string

def scatter_line_em():
    plt.rcParams['font.family'] = 'Malgun Gothic'

    df = pd.read_csv("./data/whole_merged_data2.csv", sep=",")
    df2 = df.sort_values('구별 총 생산')
    # print(df)
    # print(df2)
    gus = df2['지역명'].tolist()
    df_facility = df2.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
    list_GRDP = df2['구별 총 생산'].tolist()
    list_population = df2['인구'].tolist()
    print(list_GRDP)
    print(list_population)

    list_facility_tot = df_facility.sum(axis=1).tolist()
    print(list_facility_tot)

    # df1=pd.concat([df_GRDP,df_population,df_facility_tot], axis=1)
    # print(df1)

    size = np.array(list_population) / 300  # 마커 사이즈 (인구)

    plt.figure(figsize=(15, 8))
    n = len(list_GRDP)
    r = 2 * np.random.rand(n)
    theta = 2 * np.pi * np.random.rand(n)
    area = 200 * r ** 2 * np.random.rand(n)
    colors = theta

    plt.scatter(x=list_facility_tot, y=list_GRDP, s=size, c=colors, cmap=plt.cm.cool, marker='o', alpha=1, linewidth=1,
                edgecolors='black')
    plt.xlabel('총 시설 개수')
    plt.ylabel('구별 총 생산')
    plt.rc('font', size=8)
    sns.regplot(x=list_facility_tot, y=list_GRDP, color='black')
    for list_facility_tot, list_GRDP, gus in zip(list_facility_tot, list_GRDP, gus):
        plt.text(list_facility_tot, list_GRDP, gus)

    # plt.show()
    fig2 = plt.gcf()
    buf = io.BytesIO()
    fig2.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return string