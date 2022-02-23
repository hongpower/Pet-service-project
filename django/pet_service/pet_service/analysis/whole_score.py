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

tog_cafe = together_cafe.pet_together_cafe_score
cafe = pet_cafe.pet_cafe_score
edu = pet_edu.pet_edu_score
hos = pet_hospital.hos_score
hotel = pet_hotel.pet_hotel_score
salon = pet_salon.pet_salon_score
store = pet_store.pet_store_score
garden = pet_garden.pet_garden_score
play = pet_playground.pet_playground_score
park = whole_merged_data.pet_parks_score
phar = whole_merged_data.pet_phar_score
restaurant = whole_merged_data.pet_together_restaurants_score

pd.options.display.max_columns = None
pd.options.display.max_rows = None

df_whole = pd.concat([tog_cafe, cafe, edu, hos, hotel, salon, store, garden, play, park, phar, restaurant], axis=1)

# avg_data = ['together_cafe', 'cafe', '병원', 'hotel', 'salon', 'garden', 'park', 'pharmacy']
#
# avg = []
# for i in avg_data:
#     avg.append(df_whole[i].sum() // 25)
#
# for i in range(8):
#     for j in range(25):
#         if df_whole[avg_data[i]].values[j] < avg[i] * 0.5:
#             df_whole[avg_data[i]].values[j] = 25.0
#         elif df_whole[avg_data[i]].values[j] < avg[i]:
#             df_whole[avg_data[i]].values[j] = 50.0
#         elif df_whole[avg_data[i]].values[j] < avg[i] * 1.5:
#             df_whole[avg_data[i]].values[j] = 75.0
#         else:
#             df_whole[avg_data[i]].values[j] = 100.0
#
# for i in range(25):
#     if df_whole['store'].values[i] == 0:
#         df_whole['store'].values[i] = 25.0
#     elif df_whole['store'].values[i] == 1:
#         df_whole['store'].values[i] = 50.0
#     elif df_whole['store'].values[i] == 2:
#         df_whole['store'].values[i] = 75.0
#     else:
#         df_whole['store'].values[i] = 100.0
#
# for i in range(25):
#     if df_whole['playground'].values[i] == 0:
#         df_whole['playground'].values[i] = 0.0
#     elif df_whole['playground'].values[i] == 1:
#         df_whole['playground'].values[i] = 25.0
#     elif df_whole['playground'].values[i] == 2:
#         df_whole['playground'].values[i] = 50.0
#     elif df_whole['playground'].values[i] == 3:
#         df_whole['playground'].values[i] = 75.0
#     else:
#         df_whole['playground'].values[i] = 100
#
# for i in range(25):
#     if df_whole['together_restaurants'].values[i] < 10:
#         df_whole['together_restaurants'].values[i] = 20.0
#     elif df_whole['together_restaurants'].values[i] < 20:
#         df_whole['together_restaurants'].values[i] = 40.0
#     elif df_whole['together_restaurants'].values[i] < 30:
#         df_whole['together_restaurants'].values[i] = 60.0
#     elif df_whole['together_restaurants'].values[i] < 40:
#         df_whole['together_restaurants'].values[i] = 80.0
#     else:
#         df_whole['together_restaurants'].values[i] = 100.0
#
# for i in range(25):
#     if df_whole['edu'].values[i] == 1:
#         df_whole['edu'].values[i] = 100
#     else:
#         df_whole['edu'].values[i] = 0


df_whole['score'] = df_whole.sum(axis=1)
df_whole.loc['score'] = df_whole.sum(axis=0) // 25
print(df_whole) # 전제 점수

