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