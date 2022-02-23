import pandas as pd

hospital_data = pd.read_csv("pet_hospital.csv", encoding='euc-kr')
hospital_data = hospital_data[['상세영업상태명','소재지전화','소재지전체주소','도로명전체주소','사업장명','좌표정보(x)','좌표정보(y)']]
hospital_data = hospital_data.loc[hospital_data['상세영업상태명']=='정상']

hospital_data = hospital_data.fillna(0)
hospital_data = hospital_data[hospital_data['소재지전체주소'].str.contains('서울', na=False)]

ani_hos = hospital_data[['사업장명', '도로명전체주소']]
ani_hos = ani_hos.fillna(0)
gu = ['강남구','강동구','강북구','강서구','관악구','광진구','구로구','금천구','노원구','도봉구','동대문구','동작구','마포구','서대문구','서초구','성동구','성북구','송파구','양천구','영등포구','용산구','은평구','종로구','중구','중랑구']

a=[]
for i in range(25):
    hospital = ani_hos[ani_hos['도로명전체주소'].str.contains(gu[i], na=False)]
    hospital = hospital.reset_index(drop=True)
    cnt = len(hospital)
    a.append(cnt)
# print(a)

hos_data = pd.DataFrame(a, index=gu, columns=['hospital'])
hos_data_tot=0
for i in range(25):
    hos_data_tot += a[i]
hos_data = [a[i] for i in range(25)]
hos_score = pd.DataFrame(hos_data, index=gu, columns=['hospital'])
# print(hos_score)