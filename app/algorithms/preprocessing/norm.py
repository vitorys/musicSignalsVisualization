from sklearn.preprocessing import StandardScaler

def normalize(matrix):
    scaler = StandardScaler()
    scaler.fit(matrix)
    return scaler.transform(matrix)