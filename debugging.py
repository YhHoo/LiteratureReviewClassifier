# from nltk.stem import WordNetLemmatizer
#
#
# wordnet_lemmatizer = WordNetLemmatizer()
#
# l = ['algorithms', 'bayes', 'auto-encoders', 'machines', 'splines']
#
# for words in l:
#     print(wordnet_lemmatizer.lemmatize(words))

# --------------------------------------------------------------------

# import pandas as pd
# import matplotlib.pyplot as plt
#
# df = pd.read_csv('percentage_table_of_categories.csv', index_col=0)
# df['ROW_SUM'] = df.sum(axis=1)
# df['ROW_SUM'] = df['ROW_SUM'].apply(lambda x: x/100)
# print(df.head())
# df.plot(y='ROW_SUM', use_index=True, kind='barh', grid=True)
# plt.show()

# --------------------------------------------------------------------
#
# from os import listdir
# from os.path import isfile, join
# import pandas as pd
#
# myPath = 'C://Users//YH//AppData//Local//Mendeley Ltd//Mendeley Desktop//Downloaded//'
# # the if statement check whether it is a file
# filename = [(myPath + f) for f in listdir(myPath) if isfile(join(myPath, f))]
# # print(filename)
# l = listdir(myPath)
# # create index for df
# index = ['PDF[{}]'.format(i+1) for i in range(len(l))]
# # put everything in df
# df = pd.DataFrame(data=l, index=index)
# df.to_csv('LRC_citation.csv')

import pandas as pd
import numpy as np

df_percentage = pd.read_csv('percentage_table_of_categories.csv', index_col=0)
df_percentage = df_percentage.drop('ROW_SUM', axis=1)
df_transpose = df_percentage.transpose()

# set the upper and lower bound as significant range
lower_bound = 40
upper_bound = 60

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

df_corr.to_csv('debugging_v1_result.csv')

# the score is equivalent to how many of the pdf contribute to the correlation btw 2 methods

