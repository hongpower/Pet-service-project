from matplotlib import pyplot as plt
from matplotlib import cm
from celluloid import Camera
import numpy as np
import pandas as pd
from time import sleep
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
## 2010년 자치구별 데이터 뽑기
lst = ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"]
xls = pd.read_excel('../data/1인가구_자치구별_2010-2020.xls')
y = xls['기간'].tolist()[1:]
gu = xls['자치구'].tolist()[1:80:3]
total = xls['합계'].tolist()[1:]
cnt = 0
cnt_fory = 0
th_year = 2015
for _ in range(5):
    th_year = int(th_year)
    th_year += 1
    th_year = str(th_year)
    print(th_year)
    if th_year =='2018':
        pass
    else:
        cnt += 1
        df = pd.DataFrame()
        df['총합'] = [total[i] for i in range(len(y)) if y[i] == th_year][::3]
        total_lst= df['총합'].tolist()
        final_dict =dict(zip(gu, total_lst))
        final_dict = dict(sorted(final_dict.items(), key=lambda x: x[0]))


        ## 영진님
        xls3 = pd.read_excel('./Report.xls', header=2)
        y3 = xls3['기간'].tolist()[0:]
        gu3 = xls3['자치구'].tolist()[1:26]
        total3 = xls3['계'].tolist()[1:]
        df2 = pd.DataFrame()
        df2['총합'] = [total3[i] for i in range(len(y3)) if y3[i] == int(th_year)]

        total_lst3 = df2['총합'].tolist()
        final_dict3 = dict(zip(gu3, total_lst3))
        final_dict3 = dict(sorted(final_dict3.items(), key=lambda x: x[0]))
        # label
        lbl = list(final_dict.keys())[:-1]
        # 1인가구 수
        one = list(final_dict.values())[:-1]
        # 총 인구수
        whole = list(final_dict3.values())
        # print('1인가구 수',final_dict)
        # print('총인구 수',final_dict3)
        final_list3 = [one[i] / whole[i] * 100 for i in range(len(one))]
        final_dict4 = dict(zip(lbl, final_list3))
        ### 1인가구 : one_person과 final_Dict4
        globals()['total_person_{}'.format(cnt)] = final_dict3
        globals()['one_person_{}'.format(cnt)] = final_dict4
        # print(final_dict4)

        ### 반려동물 가진 사람 비율
        xls2 = pd.read_excel('../data/자치구별_시계열_반려동물유무_서울공공데이터포털.xls')
        y2 = xls2['기간'].tolist()[1:]
        gu2 = xls2['대분류'].tolist()[1:62:3]
        yes = xls2['반려동물 여부'].tolist()[1:]
        xls3 = (xls2.loc[1:,['기간','대분류','반려동물 여부']])
        # 기간이 th_year이고 대분류가 xx구인 애의 대분류가 키 반려동물 여부가 값
        xlsx4 = xls3.loc[(xls3['기간'] == th_year)&(xls3['대분류'].str.get(i=-1) == '구'),:]
        # print(xlsx4)
        key = xlsx4['대분류'].tolist()
        val = xlsx4['반려동물 여부'].tolist()
        final_dict2 = dict(zip(key,val))
        globals()['yes_{}'.format(cnt)] = final_dict2
        print()
        ##### one_person = k, 반려인의 비율 = ye
        ## one_Person = x, 반려인의 비율 = y
        exec(f'k = one_person_{cnt}')
        exec(f'ye = yes_{cnt}')
        exec(f'tot_k = total_person_{cnt}')
        globals()['a_{}'.format(cnt)] = list(k.keys())
        globals()['x_{}'.format(cnt)] = list(k.values())
        globals()['y_{}'.format(cnt)] = list(ye.values())
        globals()['tot_{}'.format(cnt)] = list(tot_k.values())


plt.rcParams['font.family'] = 'Malgun Gothic'
numpoints = 10
points = np.random.random((2, numpoints))
colors = cm.rainbow(np.linspace(0, 1, numpoints))
camera = Camera(plt.figure())
cnt = 0
new_year = [2016,2017,2019,2020]
color_lst = ['#FF6A5A', '#FFBE59', '#CCCCFF', '#5EFF98', '#92EACF', '#5B52FF', '#E12EFF', '#FF81B5', '#d27979',
             '#ffccf2', '#e6ffcc', '#ffe0b3','#ff9999', '#e699ff', '#dfbf9f', '#99ffbb', '#99e6ff', '#a3a3c2', '#bf80ff', '#8080ff', '#80ffff',
             '#ffff4d', '#85e085', '#a366ff','#80ffdf']
cnt2 = -1
for i in range(20):
    cnt2 += 1
    if cnt2%5 == 0:
        cnt += 1
    exec(f'ass = a_{cnt}')
    exec(f'xss = x_{cnt}')
    exec(f'yss = y_{cnt}')
    exec(f'tss = tot_{cnt}')
    # print(tss)
    size=np.array(tss)/800
    # print(size)
    plt.scatter(xss,yss,s=300,alpha=1, color=color_lst, edgecolor='black')
    plt.text(14,27,new_year[cnt-1],fontsize=40,fontweight='bold',color='gray')
    # plt.rc('font', size=8)
    plt.grid(True)
    # plt.xlim((19000, 1200000))
    plt.xlim((6,28))
    plt.ylim((8, 33))
    # plt.xlim(())
    plt.xlabel('1인가구 비율(%)')
    plt.ylabel('반려인 비율(%)')
    # plt.scatter(x=final_dict[key], y=final_dict2[key],c=colors[i], s=10)

    # points += 0.1 * (np.random.random((2, numpoints)) - .5)
    # print(points)
    # plt.scatter(*points, c=colors, s=100)
    for li1, li2, li0 in zip(xss,yss,ass):
        plt.text(li1,li2,li0)
    # for _ in range(0x5000000):
    #     pass
    # sleep(5)
    camera.snap()
anim = camera.animate(blit=True)
plt.show()
anim.save('scatter_what.gif')