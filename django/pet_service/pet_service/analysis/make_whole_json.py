import json
import pandas as pd
my_gu = '강남구'

with open('whole_total.json', 'r', encoding='utf-8') as f:
    dict_total = json.load(f)
gu_list = list(dict_total.keys())[1:]
bs_list = ["반려견놀이터", "반려동물교육센터", "애견동반카페", "애견미용실", "애견유치원", "애견카페", "애견호텔", "애완용품점","애견동반식당","동물병원","동물약국","산책가능공원"]

total_seoul_lst = dict_total['서울시 총 개수']

## 비즈니스 별 시설 비교:
# 1) seoul_avg_dict : 비즈니스 별 서울시 평균 시설 개수,
# - seoul_avg_vals : 값들
seoul_avg_dict = {}
for i in range(len(total_seoul_lst)):
    seoul_avg_dict[bs_list[i]] = int(total_seoul_lst[i][bs_list[i]])/len(gu_list)

seoul_avg_vals = list(seoul_avg_dict.values())
for i in range(len(seoul_avg_vals)):
    print(f'서울시 자치구별 {bs_list[i]}의 평균 수는 {seoul_avg_vals[i]}개입니다',end="\n")

# 2) (우리구 개수 - 서울시 평균)/ 서울시 평균
gu_info = dict_total[my_gu]
cnt_lst = list()
comp_lst = list()
for i in range(len(bs_list)):
    bs = bs_list[i]
    cnt = int(gu_info[i][bs])
    cnt_lst.append(cnt)
    # comp = round(cnt/seoul_avg_vals[i],2)
    comp = round((cnt - seoul_avg_vals[i])/seoul_avg_vals[i] + 1, 2)
    comp_lst.append(comp)
    print(f'우리 동네 {my_gu}의 {bs}의 수는 {cnt}개입니다', end=", ")
    if cnt == 0:
        print()
    else:
        if comp == 1:
            print(f'우리 동네의 {bs} 수는 서울시 평균과 같습니다', end="\n")
        elif comp > 1:
            print(f'우리 동네의 {bs} 수는 서울시 평균 {bs} 수의 {comp}배로, {round(comp-1, 2)}% 많습니다', end="\n")
        else:
            print(f'우리 동네의 {bs} 수는 서울시 평균 {bs} 수의 {comp}배로 {round((comp-1) * -1, 2)}% 작습니다', end="\n")

## 3) 인구고려, 면적별
# 우리구 자치구 비즈니스별 뽑아내기
gu_info = dict_total[my_gu]
print('!!!!!!!!!!!',gu_info)
gu_dict = dict()
for i in range(len(bs_list)):
    bs = bs_list[i]
    cnt = int(gu_info[i][bs])
    gu_dict[bs] = cnt
print('gu dict', gu_dict)
df = pd.read_csv('whole_merged_data2.csv', sep=',')

gu_list = df['지역명'].tolist()
gagu_list = df['자치구 전체면적'].tolist()
house_list = df['세대'].tolist()
gagu_house_lst =list(zip(gagu_list, house_list))

## 서울시 총 면적은 605.23km^2
# 1km2, 1000세대당
# 키는 구, 값은 (가구수, 면적)
gagu_house_dict = dict(zip(gu_list,gagu_house_lst))
# print(gagu_house_dict)

seoul_val_list = list()
for i in range(len(bs_list)):
    temp = dict_total['서울시 총 개수']
    key_nm = bs_list[i]
    seoul_val_list.append(int(temp[i][key_nm]))

# seoul_val_list 는 서울의 총 비즈니스별 개수
print('서울의 비즈니스 별 총 개수:',seoul_val_list)
print('우리 구의 비즈니스 별 총 개수:',list(gu_dict.values()))

# 면적 당
area = gagu_house_dict[my_gu][0]
house = gagu_house_dict[my_gu][1]
seoul_area = sum(gagu_list)
print('서울 면적:',seoul_area)
print('우리 구 면적:',area)
seoul_house = sum(house_list)
print('서울 세대수:',seoul_house)
print('우리 구 세대수:',house)

# 우리구 계산
victory = ''
val_area_lst = list()
val_house_lst = list()

for i in range(len(bs_list)):
    bs = bs_list[i]
    bs_val = gu_dict[bs]
    seoul_bs_val = seoul_val_list[i]
    if bs_val == 0:
        val_area_lst.append(0)
        val_house_lst.append(0)
    else:
        val_area = round(bs_val/area * 10,2)
        val_house = round(bs_val/house * 10000,2)
        seoul_val_area = round(seoul_bs_val/seoul_area * 10,2)
        seoul_val_house = round(seoul_bs_val/seoul_house * 10000,2)
        val_area_lst.append(val_area)
        val_house_lst.append(val_house)
        print(f'10km제곱당 우리 구의 {bs} 수는 {val_area}개입니다',end=' ')
        print(f'10km제곱당 서울의 {bs} 수는 {seoul_val_area}개입니다')
        if val_area > seoul_val_area:
            victory += bs + ', '
            print(f'면적으로 비교시 {bs} 부문 우리 동네 승!')
        else:
            print(f'면적으로 비교시{bs} 부문 우리 동네 패!')
        print(f'만 가구당 우리 구의 {bs} 수는 {val_house}개입니다',end=' ')
        print(f'만 가구당 서울의 {bs} 수는 {seoul_val_house}개입니다')
        if val_house > seoul_val_house:
            print(f'세대 수로 비교시 {bs} 부문 우리 동네 승!')
        else:
            print(f'세대 수로 비교시 {bs} 부문 우리 동네 패!')

print(f'우리 동네는 {victory[:-2]} 부문에서 서울시 평균보다 뛰어나네요!')


### 파일 작업 시작!
final_json = dict()
# 스코어 csv dict으로 바꾸기
score_csv = pd.read_csv('score.csv')
gu_dic = score_csv.to_dict()['score']
lsta = list(gu_dic.values())
score_dict = dict(zip(gu_list,lsta))
seoul_val_list = list()
for i in range(len(bs_list)):
    temp = dict_total['서울시 총 개수']
    key_nm = bs_list[i]
    seoul_val_list.append(int(temp[i][key_nm]))
# 등수 뽑기
rank = score_csv.sort_values('score', ascending=False)
print(rank)
ranked_list = list(rank['id'])
print(ranked_list)
for i in range(len(gu_list)):
    victory = ""
    victory2 = ""
    final_list = list()
    my_area = gu_list[i]
    gu_info = dict_total[my_area]
    a = dict()
    a['점수'] = score_dict[my_area]
    final_list.append(a)
    b = dict()
    b['등수'] = (ranked_list.index(my_area)) + 1
    final_list.append(b)
    # gu_dict = dict()
    # 비즈니스 돌기
    area = gagu_house_dict[my_area][0]
    print('area', type(area))
    house = gagu_house_dict[my_area][1]
    print('house', type(house))
    for j in range(len(bs_list)):
        c = dict()
        temp_lst = list()
        bs_name = bs_list[j]
        gu_info = dict_total[my_area]
        bs = bs_list[j]
        cnt = int(gu_info[j][bs])
        temp_lst.append(cnt)
        comp = round((cnt - seoul_avg_vals[j]) / seoul_avg_vals[j] + 1, 2)
        temp_lst.append(comp)
        bs_val = cnt
        print('bs_val' , type(bs_val))
        seoul_bs_val = seoul_val_list[j]
        seoul_val_area = round(seoul_bs_val / seoul_area * 10, 2)
        seoul_val_house = round(seoul_bs_val / seoul_house * 10000, 2)
        if bs_val == 0:
            temp_lst.append(0)
            temp_lst.append(0)
        else:
            val_area = round(bs_val/area * 10,2)
            val_house = round(bs_val/house * 10000,2)
            temp_lst.append(val_area)
            temp_lst.append(val_house)
            if val_area > seoul_val_area:
                victory += bs_name + ' '
            if val_house > seoul_val_house:
                victory2 += bs_name + ' '
        c[bs_name] = temp_lst
        final_list.append(c)
    d = dict()
    d['면적 승수'] = victory
    e = dict()
    e['세대 승수'] = victory2
    final_list.append(d)
    final_list.append(e)
    final_json[my_area] = final_list
print(final_json)
with open('whole_gu_analysis.json', 'w', encoding='utf-8') as f:
    yes = json.dumps(final_json, ensure_ascii=False)
    f.write(yes)