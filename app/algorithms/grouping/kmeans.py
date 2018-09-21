from sklearn.cluster import KMeans

def getCentroids(X, clustersNumber):

    kmeans = KMeans(n_clusters = clustersNumber, init = 'random')

    kmeans.fit(X)
    return kmeans.cluster_centers_, kmeans.transform(X)