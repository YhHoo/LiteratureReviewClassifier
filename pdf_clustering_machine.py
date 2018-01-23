# -----------------------------[OVERALL]--------------------------------
# this py will first aspect a Table_of_all.csv to be completed by pdf_glossary_analyser.py that contains all
# keywords and respective frequency for every pdf analyzed. Then this py will read the csv and load onto
# a dataframe for testing on the kmean clustering , get ready to cluster the pdf in to k groups
# by their keywords features

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# --------------[DATA GRABBING]----------------
df = pd.read_csv('Table_of_all.csv')
# use the row labels in column 0 as df index
df_transpose = df.set_index('glossary').transpose()
# convert only the data inside to matrix
X = np.array(df_transpose.astype(int))

# -----[KMEAN-CLUSTERING]-----
cluster = 6
classifier = KMeans(n_clusters=cluster)
classifier.fit(X)
# access the attributes from the classifier
centroids = classifier.cluster_centers_
labels = classifier.labels_
# sum squared error within cluster
ssw = classifier.inertia_
# result visualize
# print('SSW=', ssw)
# print('Centroids=\n', centroids)
print('Labels=\n', labels)

# -----[GROUPING PDF]-----
pdf_list = []
index_by_group = []
# take all pdf names and append into a list
for col in df:
    # ignore the first term 'glossary'
    if col.endswith('.pdf'):
        pdf_list.append(col[62:])
# convert labels from np.array to list
labels = list(labels)
# group the index of element of the same cluster into a same list
for group_no in range(cluster):
    temp = []
    for i in range(len(labels)):
        if labels[i] == group_no:
            temp.append(i)
    index_by_group.append(temp)
# save the pdf names of same cluster into same column in pandas
pdf_by_group = []
for index_list in index_by_group:
    pdf_by_group.append([pdf_list[index] for index in index_list])
# create a group names
group_name = [('[Group ' + str(n) + ']') for n in range(cluster)]
# save to txt
with open('Table_of_clustered_pdf.txt', 'w') as f:
    for i in range(cluster):
        f.write(group_name[i] + '\n')
        for pdf_name in pdf_by_group[i]:
            f.write(pdf_name + '\n')
        f.write('----'*25 + '\n')
    print('Clustered Data Saving Completed !')



