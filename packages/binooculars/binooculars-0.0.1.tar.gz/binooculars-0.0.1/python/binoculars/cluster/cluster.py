"""Module for kmeans."""

from __future__ import annotations

from binoculars import KMeansRust


class KMeans:
    """KMeans clustering with Rust backend.

    K-means tries to find the centroids of the clusters by minimizing the
    the within-cluster sum-of-squares criterion. The algorithm can be stated
    as a MapReduce problem, where the map step is the assignment of each
    point to the nearest centroid, and the reduce step is the re-computation
    of the centroids based on the new assignments.

    Args:
        n_clusters (int): The number of clusters to form as well as the number
            of centroids to generate.
        init (str): Method for initialization, defaults to "random".
        max_iter (int): Maximum number of iterations of the k-means algorithm.
        random_state (int): Seed for the random number generator for centroid initialization.



    Examples:
    ---------
    >>> from binoculars.cluster import KMeans
    >>> X = [[1, 1], [1, 2], [2, 1],[2, 2], [5, 5], [5, 6], [6, 5], [6, 6]]
    >>> kmeans = KMeans(n_clusters=2, init="random", max_iter=100, random_state=0)
    >>> kmeans.fit(X)
    >>> kmeans.predict(X)
    [0, 0, 0, 0, 1, 1, 1, 1]
    >>> kmeans.get_centroids()
    [[1.5, 1.5], [5.5, 5.5]]

    Reference:
    [1] https://web.stanford.edu/~rezab/classes/cme323/S16/projects_reports/bodoia.pdf
    """

    def __init__(self, n_clusters: int, init: str = "random", max_iter: int = 100, random_state: int = 0) -> None:
        """Initialize the model."""
        self._rustobj = KMeansRust(n_clusters, init, max_iter, random_state)
        self.n_clusters = n_clusters

    def __str__(self) -> str:
        """Return a string representation of the model."""
        return f"KMeans(n_clusters={self.n_clusters})"

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"KMeans(n_clusters={self.n_clusters})"

    def fit(self, X: list[list[float]]) -> KMeans:
        """Fit the model using X as training data."""
        self._rustobj.fit(X)
        return self

    def predict(self, X: list[list[float]]) -> list[int]:
        """Predict cluster assignments for each point in X using the fitted centroids."""
        return self._rustobj.predict(X)

    def get_centroids(self) -> list[list[float]]:
        """Get the centrroids of the fitted model."""
        return self._rustobj.get_centroids()

    def set_centroids(self, centroids: list[list[float]]) -> KMeans:
        """Set the centroids of the fitted model."""
        self._rustobj.set_centroids(centroids)
        return self

    def with_k(self, n_clusters: int) -> KMeans:
        """Set the number of clusters."""
        self._rustobj.with_k(n_clusters)
        self.n_clusters = n_clusters
        return self

    def with_max_iter(self, max_iter: int) -> KMeans:
        """Set the number of iterations of Lloyd's algorithm."""
        self._rustobj.with_num_iter(max_iter)
        return self

    def with_random_state(self, random_state: int) -> KMeans:
        """Set the random state of the model."""
        self._rustobj.with_random_state(random_state)
        return self

    def with_init(self, init: str) -> KMeans:
        """Set the initialization of the centroids, either "random" or "kmeans++"."""
        assert init in ["random", "kmeans++"]
        self._rustobj.with_init(init)
        return self
