# -----------------------------[OVERALL]--------------------------------
# this py will first aspect a Table_of_glossary_frequency.csv to be completed by pdf_glossary_analyser.py that
# contains all keywords and respective frequency for every pdf analyzed. Then this py will read the
# csv and load onto a dataframe for testing on the kmean clustering , get ready
#  to cluster the pdf in to k groups by their keywords features

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
# self library
from word_counter_utils import get_column_label


def kmean_clustering():
    # --------------[DATA GRABBING]----------------
    df = pd.read_csv('Table_of_glossary_frequency.csv', index_col=0)
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
    pdf_list = [pdf for pdf in df.columns]
    index_by_group = []
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


# this function is used in direct_classification() that take the percentage_table_df and find the correlation
# between the features through the data sets_analyzed by the pdf_glossary_analyzer.py
def connection_matrix(df_input, lo_bound=40, hi_bound=60, save_csv=True, return_df=False):
    df_percentage = df_input
    df_percentage = df_percentage.drop('ROW_SUM', axis=1)
    df_transpose = df_percentage.transpose()

    # set the upper and lower bound as significant range
    lower_bound = lo_bound
    upper_bound = hi_bound

    # create a square matrix of zero to contain the corr
    features = len(df_transpose.columns)
    data = np.zeros((features, features))
    labels = [feature for feature in df_transpose.columns]
    df_corr = pd.DataFrame(data=data, columns=labels, index=labels)

    # progress thru all columns of features, taking it as centre
    for col in df_transpose:
        # get all row values in [col] into a list
        vector_main = df_transpose[col].tolist()
        # initialize nex col no
        nex_col_no = df_transpose.columns.get_loc(col) + 1
        # do this for the rest of the columns on the right
        while nex_col_no < len(df_transpose.columns):
            # ----[CORRELATION FUNCTION]----
            # initialize corr_score
            corr_score = 0
            # do this for all rows under [nex_col_no]
            for row_no in range(len(df_transpose.index)):
                a = df_transpose.iloc[row_no, nex_col_no]
                b = vector_main[row_no]
                num = min(a, b)
                den = max(a, b)
                # significance test for percentages
                if num >= lower_bound and den <= upper_bound:
                    corr_score += (num / den)

            # ----[UPDATE CORR MATRIX WITH corr_score]----
            # update to the corr_score_matrix in df_corr, *hint: [row index][column index]
            df_corr.iloc[df_transpose.columns.get_loc(col), nex_col_no] = corr_score
            # increment the nex_col_no until it reaches the last column
            nex_col_no += 1

    # saving
    if save_csv:
        df_corr.to_csv('Table_of_connection.csv')
        print('[Table_of_connection.csv] saving completed !')
    # [SCORE EXPLAIN] - it can range from 0 to any +ve no. it is a sum of ratios of (small% / big%),we can
    # also think the score as average no. of papers have used these kind of connection

    # return df of correlation
    if return_df:
        return df_corr


def direct_classification(plot=False, corr_mat=False):
    # --------------[DATA GRABBING]----------------
    result_df = pd.read_csv('Table_of_glossary_frequency.csv', index_col=0)
    # Checker to eliminate column with 'x'
    for col in result_df:
        if result_df[col][0] == 'x':
            result_df.drop([col], axis=1, inplace=True)
    # grab the glossary categories
    cat_glossary_df = pd.read_csv('ml_glossary_all2.csv')
    f_array = []
    # for every pdf column in Table_of_glossary_frequency.csv..
    for col in result_df:
        # this list contains all row labels with non zero element
        non_zero_keywords = result_df.index[result_df[col] != 0].tolist()
        keywords_in_cat = []
        for keywords in non_zero_keywords:
            # this list contains all equivalent categories of non_zero_keywords
            keywords_in_cat.append(get_column_label(dataframe=cat_glossary_df,
                                                    search=keywords))
        # this list contain f of those non-zero keywords, hint: [column_label][row_label]
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
    column_label = [pdf for pdf in result_df.columns]
    row_label = list(cat_glossary_df)
    percentage_table_df = pd.DataFrame(data=f_array.T, columns=column_label, index=row_label)
    # adding a last column of summing across rows
    percentage_table_df['ROW_SUM'] = percentage_table_df.sum(axis=1)
    # divide by 100 for last column of row sum
    percentage_table_df['ROW_SUM'] = percentage_table_df['ROW_SUM'].apply(lambda x: x/100)

    # saving to csv
    percentage_table_df.to_csv('Table_of_percentage_categories.csv')
    print('[Table_of_percentage_categories.csv] saving completed !')
    # [SCORE EXPLAIN] - The score means the average no.of papers that have used this specific method

    # -------[CORRELATION MATRIX IN CSV]-----------
    if corr_mat:
        connection_matrix(df_input=percentage_table_df,
                          lo_bound=40,
                          hi_bound=60,
                          save_csv=True)

    # -------[VISUALIZATION]--------
    if plot:
        percentage_table_df.plot(y='ROW_SUM',
                                 use_index=True,
                                 kind='barh',
                                 grid=True,
                                 title='Heatmap of Machine Learning Methodology')
        plt.show()


# do the work
direct_classification(plot=True, corr_mat=True)
