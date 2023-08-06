# binoculars
A tiny, yet blazingly fast machine learning library written in Rust with Python interface.
This project was motivated by [polars](https://github.com/pola-rs/polars) and [sklearn](https://github.com/scikit-learn/scikit-learn). 
The goal is to learn Rust, have a better understanding of what is happening under the hood of classic ML models, and explore the pitfalls of building a Python package.

### Example usage

```python
>>> from binoculars.cluster import KMeans
>>> X = [[1, 1], [1, 2], [2, 1],[2, 2], [5, 5], [5, 6], [6, 5], [6, 6]]
>>> kmeans = KMeans(n_clusters=2, init="random", max_iter=100, random_state=0)
>>> kmeans.fit(X)
>>> kmeans.predict(X)
[0, 0, 0, 0, 1, 1, 1, 1]
>>> kmeans.get_centroids()
[[1.5, 1.5], [5.5, 5.5]]
```

