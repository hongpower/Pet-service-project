import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

xls = pd.read_excel('./Report.xls',header = 2)
print(xls.head())

th_year = 2016

y = xls['기간'].tolist()[0:]
print(y)
gu = xls['자치구'].tolist()[1:26]
print(gu)
total = xls['계'].tolist()[1:]
print(total)

df = pd.DataFrame()
df['총합'] = [total[i] for i in range(len(y)) if y[i] == th_year]
# lst = list()
# for i in range(len(y)):
#     if y[i] == th_year:
#         lst.append(total[i])
# df['총합'] = lst[::3]

total_lst= df['총합'].tolist()
final_dict =dict(zip(gu, total_lst))
final_dict = dict(sorted(final_dict.items(), key=lambda x: x[0]))
print(final_dict)

# xls = pd.readexcel('1인가구자치구별_2010-2020.xls')
#
# y = xls['기간'].tolist()[1:]
# gu = xls['자치구'].tolist()[1:80:3]
# total = xls['합계'].tolist()[1:]
#
# df = pd.DataFrame()
# df['총합'] = [total[i] for i in range(len(y)) if y[i] == th_year][::3]
# total_lst= df['총합'].tolist()
# final_dict =dict(zip(gu, total_lst))
# final_dict = dict(sorted(final_dict.items(), key=lambda x: x[0]))
# print(final_dict)