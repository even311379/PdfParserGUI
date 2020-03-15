import sys
import os
import jieba
import re
import numpy as np
import pandas as pd
import pdftotext

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.cluster.hierarchy import ward
from sklearn.cluster import AgglomerativeClustering
from shutil import copyfile

def CreateGroup(ODIR, N_Group):
    SS = []
    manual_files = eval(open('ManualFiles.log', 'r').read())

    columns = ['系所代碼','準考號碼','姓名','學校',
            '一上班排','一下班排','二上班排','二下班排','三上班排',
            '一上組排','一下組排','二上組排','二下組排','三上組排',
            '一上校排','一下校排','二上校排','二下校排','三上校排',
            'ParserPattern']

    for file in manual_files:
        with open(file, "rb") as f:
            pdf = pdftotext.PDF(f)    
            score_sheet = pdf[2]        
        SS.append(" ".join(jieba.cut(re.sub('\W|\d|[a-zA-Z]','',score_sheet),cut_all=False)))
    
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(SS)
    SS_sim_mat = (tfidf * tfidf.T).A
    linkage_matrix = ward(SS_sim_mat)

    cluster = AgglomerativeClustering(n_clusters=N_Group, affinity='euclidean', linkage='ward')
    cluster.fit_predict(SS_sim_mat)

    os.mkdir(f'{ODIR}/manual')
    for i in range(N_Group):
        os.mkdir(f'{ODIR}/manual/G{i}')

    for i,file in enumerate(manual_files):
        copyfile(file,f'{ODIR}/manual/G'+str(cluster.labels_[i])+'/'+file.split('/')[-1])

    # create template excel files to start manual work
    for i in range(N_Group):
        temp = [f for j,f in enumerate(manual_files) if cluster.labels_[j] == i]
        DL = []
        for f in temp:
            D = []
            D.append(f.split('/')[-3])
            D.append(f.split('/')[-2])
            D += [np.nan]*17
            D.append('手動處理！！加油！！')
            DL.append(D)
        pd.DataFrame(DL,columns=columns).to_excel(f'{ODIR}/manual/G{i}/template_G{i}.xlsx',index=False)


if __name__ == '__main__':
    ODIR = str(sys.argv[1])
    N_Group = int(sys.argv[2])
    CreateGroup(ODIR, N_Group)
