import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

park_data = pd.read_csv("park.csv", encoding='utf-8')
plt.rcParams['axes.unicode_minus'] = False
plt.rc('font', family='Malgun Gothic')
print(park_data)
a = sns.barplot(data=park_data, x="제공기관명", y="공원면적")
a.set_xticklabels(a.get_xticklabels(), rotation=90)

plt.show()