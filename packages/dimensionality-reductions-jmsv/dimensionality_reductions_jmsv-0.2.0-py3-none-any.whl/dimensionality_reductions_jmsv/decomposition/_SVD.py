import numpy as np

class TruncatedSVD:
    def __init__(self, n_components=2):
        self.n_components = n_components

    def fit(self, X):
        U, s, Vt = np.linalg.svd(X)
        self.components_ = Vt[:self.n_components]
        return self

    def transform(self, X):
        return np.dot(X, self.components_.T)

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)