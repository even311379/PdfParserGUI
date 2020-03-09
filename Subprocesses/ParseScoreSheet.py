import os
import sys
import pandas as pd
import numpy as np
try:
    from Subprocesses.ScoreSheetParsers import complete_patterns, missing_patterns
except:
    from ScoreSheetParsers import complete_patterns, missing_patterns

import pdftotext
import jieba
import re
from multiprocessing import Pool

def ParseProcess(ListOfPath):

    DD = []
    Failed_files = []

    for f in ListOfPath:
        R = complete_patterns(f)
        if type(R) == list:
            if len(R) != 20:                
                Failed_files.append(f)
                continue            
            DD.append(R)
        
        elif R == 'skipped':
            RM = missing_patterns(f) # result of missing
            if RM:
                if len(RM) != 20:
                    Failed_files.append(f)
                    continue
                DD.append(RM)
            else:
                Failed_files.append(f)
        else:
            Failed_files.append(f)

    return DD, Failed_files

if __name__ == '__main__':
    WDIR = str(sys.argv[1])
    ODIR = str(sys.argv[2])

    upper_most = WDIR
    all_pdf_files = [ f'{upper_most}/{i}/{j}/{j}.pdf' for i in os.listdir(upper_most) for j in os.listdir(upper_most+'/'+i) ]
    subpath = []
    N = int(len(all_pdf_files)/15)
    for i in range(14):
        subpath.append(all_pdf_files[N*(i):N*(i+1)])
    subpath.append(all_pdf_files[N*(i+1):])

    p = Pool(processes = 15)
    data = p.map(ParseProcess,subpath)
    DD = []
    ManualFiles = []
    for d in data:
        DD += d[0]
        ManualFiles += d[1]

    N_All = len(all_pdf_files)
    N_Success = len(DD)
    R_Success = round((N_Success/N_All)*100, 2)
    with open('ParseResult.log', 'w+') as r:
        r.write('*********\n')
        r.write(f'共 {N_All} 筆檔案\n')
        r.write(f'成功解析: {N_Success}筆 ({R_Success}%)!\n')
        r.write(f'剩餘 {N_All - N_Success} 筆需手動處理!\n')
        r.write('*********')
    with open('ManualFiles.log', 'w+') as r:
        r.write(str(list(ManualFiles)))

    columns = ['系所代碼','準考號碼','姓名','學校',
               '一上班排','一下班排','二上班排','二下班排','三上班排',
               '一上組排','一下組排','二上組排','二下組排','三上組排',
               '一上校排','一下校排','二上校排','二下校排','三上校排',
               'ParserPattern']
    df = pd.DataFrame(DD,columns=columns)
    df_min = pd.concat([df.iloc[:,i*5+4:i*5+9].min(axis=1) for i in range(3)],axis=1)
    df_min.columns=['最佳班排','最佳組排','最佳校排']
    pd.concat([df,df_min],axis=1).to_excel(f'{ODIR}/Result.xlsx',index=False)