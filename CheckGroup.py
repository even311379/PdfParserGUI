import jieba
import re
import pdftotext
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.cluster.hierarchy import ward, dendrogram

def DrawCluster():
    SS = []

    manual_files = eval(open('ManualFiles.log', 'r').read())

    for file in manual_files:
        with open(file, "rb") as f:
            pdf = pdftotext.PDF(f)
            score_sheet = pdf[2]
        
        SS.append(" ".join(jieba.cut(re.sub('\W|\d|[a-zA-Z]','',score_sheet),cut_all=False)))
    

    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(SS)
    SS_sim_mat = (tfidf * tfidf.T).A
    linkage_matrix = ward(SS_sim_mat)

    plt.figure(figsize=(10, 3.5))  
    dd = dendrogram(linkage_matrix,  
                orientation='top',
                distance_sort='descending',
                show_leaf_counts=True,
                no_labels=True,
                color_threshold=4) # you can tune this value to deside how many group
    plt.savefig("Cluster.png", dpi=60)

if __name__ == "__main__":
    DrawCluster()
