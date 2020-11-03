import pandas as pd
import glob

#dirPath = r'D:\Python Codes\TW_vote_data\2020不分區\*.xls'
dirPath = r'D:\Python Codes\TW_vote_data\*.xlsx'
result = glob.glob(dirPath)
print (result)

for i in result:
    file = pd.read_excel(i)
    file.to_json(r'D:\Python Codes\TW_vote_data\2020不分區-' + i.replace('.xlsx',"")[-3:] + '(add 泛藍泛綠).json')
    print(i)
