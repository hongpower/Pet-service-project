import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

plt.rcParams['axes.unicode_minus'] = False
plt.rc('font', family='Malgun Gothic')


def drawpie():
    ## 파이 그래프 생성 함수:

    df = pd.read_csv("industry.csv", sep=",")
    name = df['시설 분류'].tolist()
    industry = df['비율'].tolist()
    cnt_dict_industry = dict(zip(name, industry))
    df_industry = pd.DataFrame.from_dict([cnt_dict_industry])
    df_industry_sort = df_industry.sort_values(by=0, axis=1, ascending=False)
    name_sort = df_industry_sort.columns.tolist()

    color_lst = ['#FF6A5A', '#FFBE59', '#CCCCFF', '#5EFF98', '#92EAFF', '#5B52FF', '#E12EFF', '#FF81B5', '#FF004E', '#85DF9D', '#FFB02C', '#E0B9ED']

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

    df2 = pd.read_csv("survey.csv", sep=",")
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
    plt.tight_layout()
    plt.show()


drawpie()
