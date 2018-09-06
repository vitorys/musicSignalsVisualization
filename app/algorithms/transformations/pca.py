from sklearn.decomposition import PCA

def reduceDimensionality(matrix):
    pca = PCA(n_components=2)
    pca.fit(matrix)
    return pca