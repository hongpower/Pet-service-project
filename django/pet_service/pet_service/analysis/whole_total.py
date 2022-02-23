import pandas as pd
import together_cafe
import pet_cafe
import pet_edu
import pet_hospital
import pet_hotel
import pet_salon
import pet_store
import pet_garden
import pet_playground
import whole_merged_data
import json

tog_cafe = together_cafe.pet_together_cafe_score # 동반 카페
cafe = pet_cafe.pet_cafe_score # 애견카페
edu = pet_edu.pet_edu_score # 교육센터
hos = pet_hospital.hos_score # 병원
hotel = pet_hotel.pet_hotel_score # 호텔
salon = pet_salon.pet_salon_score # 미용실
store = pet_store.pet_store_score # 애완용품점
garden = pet_garden.pet_garden_score # 유치원
play = pet_playground.pet_playground_score # 놀이터
park = whole_merged_data.pet_parks_score # 공원
phar = whole_merged_data.pet_phar_score # 약국
restaurant = whole_merged_data.pet_together_restaurants_score # 동반식당

pd.options.display.max_columns = None
pd.options.display.max_rows = None
#"반려견놀이터", "반려동물교육센터", "애견동반카페", "애견미용실", "애견유치원", "애견카페", "애견호텔", "애완용품점","애견동반식당","동물병원","동물약국","산책가능공원"
df_whole = pd.concat([play, edu, tog_cafe,salon, garden, cafe, hotel, store, restaurant, hos,phar, park ], axis=1)

df_whole.loc['서울시 총 개수'] = df_whole.sum(axis=0)
print(df_whole)
col_lst = ["반려견놀이터", "반려동물교육센터", "애견동반카페", "애견미용실", "애견유치원", "애견카페", "애견호텔", "애완용품점","애견동반식당","동물병원","동물약국","산책가능공원"]
idx_lst = [idx for idx in df_whole.index]

# 26개 (서울시 총합까지) : 첫번째 딕셔너리
print(idx_lst)

# 12개 : 비즈니스 이름/ 두번째 딕셔너리
print(col_lst)

## json 파일 만들기
outer_dict = dict()
lst = list()
# 서울시 총합 맨 앞으로
for i in range(len(col_lst)):
    inner_dict = dict()
    inner_dict[col_lst[i]] = str(df_whole.iloc[-1][i])
    lst.append(inner_dict)
outer_dict[idx_lst[-1]]=lst
# 행 선택후 열선택
for i in range(len(idx_lst)-1):
    lst = list()
    for j in range(len(col_lst)):
        inner_dict = dict()
        inner_dict[col_lst[j]] = str(df_whole.iloc[i][j])
        lst.append(inner_dict)
    outer_dict[idx_lst[i]]=lst

print(outer_dict)
json_whole_total = json.dumps(outer_dict, ensure_ascii=False)
with open('whole_total.json', 'w', encoding='utf-8') as f:
    f.write(json_whole_total)
