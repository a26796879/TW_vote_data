import pandas as pd
df = pd.read_excel('不分區立委-A05-6-得票數一覽表(臺南市).xls',header = 1)
data_length = df.shape[0]
data_width = df.shape[1]
df.dropna(how='all',inplace=True)
df.drop(columns=['投票率H\nH=C÷G'],inplace=True)

for i in range(1,df.shape[0]):
    for j in range(3,df.shape[1]-6):
        df.iloc[i,j] = int(df.iloc[i,j].replace(",",""))

#重複的里名，進行累加
for i in range(2,df.shape[0]):
    if df.iloc[i,1] == df.iloc[i-1,1]:
        for j in range(3,df.shape[1]-6):
            df.iloc[i,j] = df.iloc[i,j] + df.iloc[i-1,j]
            
df['鄉(鎮、市、區)別'].fillna(method='ffill',  inplace=True)
df['村里別'].fillna(value="",  inplace=True)
for i in range(2,df.shape[0]):
    if df.iloc[i,1] == "":
        df.iloc[i,1] = str(df.iloc[i,0]) + "合計"
for partyName in range(3,df.shape[1]-7):
    df.iloc[0,partyName] = df.iloc[0,partyName].split('\n')[2]
df.iloc[1,0] = ""
df.iloc[1,1] = "總計"
df.iloc[0,1] = "政黨"
df.drop_duplicates(subset=['村里別'],keep='last',inplace=True)
df.to_excel('TEST_result.xlsx',sheet_name='sheet1')

import xlwings as xw
wb = xw.Book('TEST_result.xlsx').sheets[0]
wb.range('A:A').api.EntireColumn.Delete()
for i in range(4,df.shape[0]+3):
    try:
        wb.range(i,1).value = wb.range(i,1).value.split('\u3000')[1]
        wb.range(i,2).value = wb.range(i,2).value.split('\u3000')[1]
    except:
        continue
wb.range('C:C').api.EntireColumn.Delete()
for i in range(3,df.shape[1]-7):
    wb.range(1,i).value = wb.range(2,i).value
wb.range('2:2').api.EntireRow.Delete()
xw.Book('TEST_result.xlsx').save()
xw.Book('TEST_result.xlsx').close()
print('success!')
