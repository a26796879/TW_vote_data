import pandas as pd
import glob

dirPath = r'D:\Python Codes\TW_vote_data\2020不分區\*.xls'

result = glob.glob(dirPath)

for file in result:
    print(file.split('(')[1].split(')')[0])

    df = pd.read_excel(file,header = 1)
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
    ###################################
    
    #加入計算泛藍、泛綠
    wb.range('V:V').insert() #wb.api.columns(22).insert
    wb.range('V:V').insert() #wb.api.columns(22).insert

    wb.range('V1').value = "泛藍"  #CDEIKT
    wb.range('W1').value = "泛綠"  #PGNHJULRS

    #從2到有資料的最後一列
    for i in range(2,wb.range('A' + str(wb.cells.last_cell.row)).end('up').row +1):
        wb.range('V' + str(i)).value = wb.range('C' + str(i)).value + wb.range('D' + str(i)).value + wb.range('E' + str(i)).value + wb.range('I' + str(i)).value + wb.range('K' + str(i)).value + wb.range('T' + str(i)).value
        wb.range('W' + str(i)).value = wb.range('P' + str(i)).value + wb.range('G' + str(i)).value + wb.range('N' + str(i)).value + wb.range('H' + str(i)).value + wb.range('J' + str(i)).value + wb.range('U' + str(i)).value + wb.range('L' + str(i)).value + wb.range('R' + str(i)).value + wb.range('S' + str(i)).value
    
    ###################################
    xw.Book('TEST_result.xlsx').save('D:\\Python Codes\\TW_vote_data\\' + file.split('(')[1].split(')')[0] +".xlsx")
    xw.Book('TEST_result.xlsx').close()
    print('success!')
