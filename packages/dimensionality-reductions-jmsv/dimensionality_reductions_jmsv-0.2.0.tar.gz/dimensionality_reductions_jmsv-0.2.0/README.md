[![PyPI Version](https://img.shields.io/pypi/v/dimensionality_reductions_jmsv)](https://pypi.org/project/dimensionality_reductions_jmsv/)
[![Package Status](https://img.shields.io/pypi/status/dimensionality_reductions_jmsv)](https://pypi.org/project/dimensionality_reductions_jmsv/)
![Python Versions](https://img.shields.io/pypi/pyversions/dimensionality_reductions_jmsv)
[![License](https://img.shields.io/pypi/l/dimensionality_reductions_jmsv)](https://mit-license.org/)

### What is it?

**dimensionality_reductions_jmsv** is a Python package that provides three methods (PCA, SVD, t-SNE) to apply dimensionality reduction to any dataset. Aslo provides two methods (KMeans y KMedoids) to clustering. 

### Installing the package

1. Requests is available on PyPI:
    ```bash
    pip install dimensionality_reductions_jmsv
    ```

2. Try your first **_dimensionality reduction with PCA_**
    ```python
    from dimensionality_reductions_jmsv.decomposition import PCA
    import numpy as np
    
    X = (np.random.rand(10, 10) * 10).astype(int)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    print("Original Matrix:", '\n', X, '\n')
    print("Apply dimensionality reduction with PCA to Original Matrix:", '\n', X_pca)
    ```

3. Try your first **_KMeans cluster_**
   ```python
   from dimensionality_reductions_jmsv.cluster import KMeans
   from sklearn.datasets import make_blobs
   import matplotlib.pyplot as plt
   
   X, y = make_blobs(n_samples=500, n_features=2, centers=4, cluster_std=1, center_box=(-10.0, 10.0), shuffle=True,
                     random_state=1, )
   k = KMeans(n_clusters=4, init_method='kmeans++', random_state=32, n_init=10)
   m = k.fit_transform(X)
   
   plt.scatter(X[:, 0], X[:, 1], c=k._assign_clusters(X))
   plt.title('Cluster KMeans')
   plt.show();
   ```

