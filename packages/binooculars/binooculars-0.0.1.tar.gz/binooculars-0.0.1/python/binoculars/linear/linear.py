"""Module for linear regression."""

from __future__ import annotations

from binoculars import LinearRegressionRust, LogisticRegressionRust


class LinearRegression:
    """Least squares linear regression with Rust backend."""

    def __init__(self) -> None:
        self._rustobj = LinearRegressionRust()
        self.weights = None
        self.method = None
        self.is_bias = False

    def __str__(self) -> str:
        """Return a string representation of the model."""
        return f"LinearModel(weights={self.weights})"

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"LinearModel(weights={self.weights})"

    def fit(self, X: list[list[float]], y: list[float]) -> LinearRegression:
        """Fit the model using X as training data and y as target values."""
        self._rustobj.fit(X, y)
        return self

    def predict(self, X: list[list[float]]) -> list[float]:
        """Predict using the linear model."""
        return self._rustobj.predict(X)

    def get_weights(self) -> list[float]:
        """Get parameters for this estimator."""
        return self._rustobj.get_weights()

    def set_weights(self, weights: list[float]) -> LinearRegression:
        """Set the parameters of this estimator."""
        self._rustobj.set_weights(weights)
        return self

    def with_bias(self, with_bias: bool) -> LinearRegression:
        """Set the parameters of this estimator."""
        self._rustobj.with_bias(with_bias)
        return self

    def with_solver(self, method: str) -> LinearRegression:
        """Set the parameters of this estimator."""
        assert method in ["normal", "ls"]
        self._rustobj.with_method(method)
        return self


class LogisticRegression:
    """Logistic regression with Rust backend."""

    def __init__(self) -> None:
        self._rustobj = LogisticRegressionRust()
        self.weights = None
        self.method = None
        self.is_bias = False

    def __str__(self) -> str:
        """Return a string representation of the model."""
        return f"LogisticModel(weights={self.weights})"

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"LogisticModel(weights={self.weights})"

    def fit(self, X: list[list[float]], y: list[float]) -> LogisticRegression:
        """Fit the model using X as training data and y as target values."""
        self._rustobj.fit(X, y)
        return self

    def predict(self, X: list[list[float]]) -> list[float]:
        """Predict using logistic regression."""
        return self._rustobj.predict(X)

    def get_weights(self) -> list[float]:
        """Get the weights of this estimator."""
        return self._rustobj.get_weights()

    def set_weights(self, weights: list[float]) -> LogisticRegression:
        """Set the weights of this estimator."""
        self._rustobj.set_weights(weights)
        return self

    def with_bias(self, with_bias: bool) -> LogisticRegression:
        """Set whether to include a bias term in the model."""
        self._rustobj.with_bias(with_bias)
        return self

    def with_solver(self, method: str) -> LogisticRegression:
        """Set the solver method, currently only gradient descent is supported."""
        assert method in ["gd"]
        self._rustobj.with_method(method)
        return self

    def with_learning_rate(self, learning_rate: float) -> LogisticRegression:
        """Set the learning rate for gradient descent."""
        self._rustobj.with_learning_rate(learning_rate)
        return self

    def with_epochs(self, epochs: int) -> LogisticRegression:
        """Set the number of epochs (passes on the training data) for gradient descent."""
        self._rustobj.with_epochs(epochs)
        return self

    def with_batch_size(self, batch_size: int) -> LogisticRegression:
        """Set batch size for gradient descent."""
        self._rustobj.with_batch_size(batch_size)
        return self
