# testing on the kmean clustering , get ready to cluster the pdf in to k groups by their keywords features
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# --------------[DATA GRABBING]----------------
df = pd.read_csv('Table_of_all.csv')
# df['TOTAL_F'] = df.sum(axis=1)
# use the row labels in column 0 as df index
df = df.set_index('glossary').transpose()
# convert only the data inside to matrix
X = np.array(df.astype(int))
print(X)


# X = np.array([[1, 2],
#               [1.5, 1.8],
#               [5, 8],
#               [8, 8],
#               [1, 0.6],
#               [9, 11]])
# #
# # plt.scatter(X[:, 0], X[:, 1], s=100)
# # plt.show()
#
n_cluster_trial = np.arange(1, 16, 1)
ssw_list = []
for n in n_cluster_trial:
    classifier = KMeans(n_clusters=n)
    classifier.fit(X)
    # access the attributes from the classifier
    centroids = classifier.cluster_centers_
    labels = classifier.labels_
    # sum squared error within cluster
    ssw = classifier.inertia_
    ssw_list.append(ssw)
    print('n_cluster = ', n)

# print('SSW= ', ssw)
# print('Centroids=\n', centroids)
# print('Labels=\n', labels)

plt.plot(n_cluster_trial, ssw_list)
plt.show()



#
# colors = ['g.', 'r.', 'c.']
#
# # plot out the six points with colour according to the cluster assigned
# for i in range(len(X)):
#     plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=25)
# plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', s=150, linewidths=5)
# plt.show()

