import numpy as np
import pandas as pd

xlsx_file = './excel/DT.xlsx'

df = pd.read_excel(xlsx_file,sheet_name='Sheet1')

'''####################### Function Read File #######################'''
def parseValue(x):
     print('x ::=='+x)
     try:
         if pd.isnull(x):
             return '-'
         return str(x).join((agent_contact, agent_telno)).encode('utf-8').strip()
     except NameError:
         print('exception::=='+NameError)

def getRowList(df):
    rows = {}
    for ind_row in df.index:
        datas = {}
        row_key = '';
        for col_name in df.columns:
            data = df[col_name][ind_row]
            #print(data)
            if col_name == 'Stub':
                row_key = data
            else:
                datas[col_name] = data
        rows[row_key] = datas
    return rows

def getColumnList(df):
    columns = {}
    for col_name in df.columns:
        datas = {}
        for ind_row in df.index:
            key_stub = df['Stub'][ind_row]
            if col_name != 'Stub':
                data = df[col_name][ind_row]
                datas[key_stub] = data
        if col_name != 'Stub':
            columns[col_name] = datas
    return columns
'''####################### Function Read File #######################'''

rows = getRowList(df)
for x in rows:
    #print('row=>x::=='+x)
    for x_d in sorted(rows[x]):
        #print('row=>x_d::==' + str(x_d)+' rows[x]::=='+str(rows[x][x_d]))
        print('')

columns = getColumnList(df)
for y in sorted(columns):
    print('column=>y::=='+y)
    for y_d in sorted(columns[y]):
        print('column=>y_d::==' + str(y_d)+' columns[y]::=='+str(columns[y][y_d]))
        print('')