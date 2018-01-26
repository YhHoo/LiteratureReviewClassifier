# from nltk.stem import WordNetLemmatizer
#
#
# wordnet_lemmatizer = WordNetLemmatizer()
#
# l = ['algorithms', 'bayes', 'auto-encoders', 'machines', 'splines']
#
# for words in l:
#     print(wordnet_lemmatizer.lemmatize(words))

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('percentage_table_of_categories.csv', index_col=0)
df['ROW_SUM'] = df.sum(axis=1)
df['ROW_SUM'] = df['ROW_SUM'].apply(lambda x: x/100)
print(df.head())
df.plot(y='ROW_SUM', use_index=True, kind='barh', grid=True)
plt.show()
