import csv
import urllib.request
from urllib.error import URLError, HTTPError
import pandas as pd
import numpy as np

fileDir = '주얼리공방.csv'

file = pd.read_csv(fileDir)
file.head()

file['홈페이지체크'] = np.nan

print(pd.isna(file.loc[3, '홈페이지']))

for index in file.index:
    if pd.isna(file.loc[index, '홈페이지']) == False:
        print(index)
        url = file.loc[index, '홈페이지']
        try:
            res = urllib.request.urlopen(url)
            file.loc[index, '홈페이지체크'] = str(res.status)
            print(res.status)
        except:
            file.loc[index, '홈페이지체크'] = '접속불가'
            print('접속불가')

# csv 저장
file.to_csv(fileDir, sep=',', index=False)