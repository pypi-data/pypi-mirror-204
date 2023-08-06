import numpy as np

class PCA:
    def __init__(self, n_components=None):
        self.n_components = n_components

    def fit(self, X):
        n_samples, n_features = X.shape

        # Subtract mean from data
        self.mean_ = np.mean(X, axis=0)
        X_centered = X - self.mean_

        # Compute covariance matrix
        covariance = np.dot(X_centered.T, X_centered) / (n_samples - 1)

        # Compute eigendecomposition of covariance matrix
        eigenvalues, eigenvectors = np.linalg.eigh(covariance)

        # Sort eigenvectors in descending order of eigenvalues
        indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[indices]
        eigenvectors = eigenvectors[:, indices]

        # Truncate eigenvectors to desired number of components
        if self.n_components is not None:
            eigenvectors = eigenvectors[:, :self.n_components]

        self.components_ = eigenvectors
        self.explained_variance_ = eigenvalues
        self.explained_variance_ratio_ = eigenvalues / np.sum(eigenvalues)

        return self

    def fit_transform(self, X):
        self.fit(X)
        X_centered = X - self.mean_
        return np.dot(X_centered, self.components_)

    def transform(self, X):
        X_centered = X - self.mean_
        return np.dot(X_centered, self.components_)