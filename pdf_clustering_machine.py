# -----------------------------[OVERALL]--------------------------------
# this py will first aspect a Table_of_all.csv to be completed by pdf_glossary_analyser.py that contains all
# keywords and respective frequency for every pdf analyzed. Then this py will read the csv and load onto
# a dataframe for testing on the kmean clustering , get ready to cluster the pdf in to k groups
# by their keywords features

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
# self library
from word_counter_utils import get_column_label


def kmean_clustering():
    # --------------[DATA GRABBING]----------------
    df = pd.read_csv('Table_of_all.csv', index_col=0)
    # use the row labels in column 0 as df index
    df_transpose = df.transpose()
    # convert only the data inside to matrix
    X = np.array(df_transpose.astype(int))
    # -----[KMEAN-CLUSTERING]-----
    cluster = 6  # [USER ONLY CHANGE THIS PARAMETER !!!]
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

    # -------[SAVING TO TXT]--------
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


def direct_classification():
    # --------------[DATA GRABBING]----------------
    result_df = pd.read_csv('Table_of_all.csv', index_col=0)
    cat_glossary_df = pd.read_csv('ml_glossary_all2.csv')
    f_array = []
    # for every pdf column in Table_of_all.csv..
    for col in result_df:
        # this list contains all row labels with non zero element
        non_zero_keywords = result_df.index[result_df[col] != 0].tolist()
        keywords_in_cat = []
        for keywords in non_zero_keywords:
            # this list contains all equivalent categories of non_zero_keywords
            keywords_in_cat.append(get_column_label(dataframe=cat_glossary_df,
                                                    search=keywords))
        # this list contain f of those non-zero keywords
        non_zero_f = [result_df[col][keywords] for keywords in non_zero_keywords]

        # -------[Sum according to categories]--------
        # create a zero list with len equal to no of categories
        f_list = np.zeros(len(cat_glossary_df.columns))
        # the individual f will accumulate on the f_list[] with index same as in df
        for i in range(len(non_zero_f)):
            cat_loc = cat_glossary_df.columns.get_loc(keywords_in_cat[i])
            f_list[cat_loc] += non_zero_f[i]
        # convert the f_list to percentage list
        total = sum(f_list)
        if total != 0:
            f_list = [int(round(f / total * 100)) for f in f_list]
        else:
            f_list = [int(f) for f in f_list]
        f_array.append(f_list)
    # covert itself to array
    f_array = np.array(f_array)
    # -------[CONCLUSION INTO DATAFRAME]--------
    column_label = [string[62:] for string in list(result_df.columns.values)]
    row_label = list(cat_glossary_df)
    percentage_table_df = pd.DataFrame(data=f_array.T, columns=column_label, index=row_label)
    # saving to csv
    percentage_table_df.to_csv('percentage_table_of_categories.csv')


direct_classification()
