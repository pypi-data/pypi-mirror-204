use ndarray::{Array1, Array2};
use rand::prelude::*;

pub fn add_bias(mut x: Vec<Vec<f64>>, with_bias: bool) -> Vec<Vec<f64>> {
    if with_bias {
        for p in x.iter_mut() {
            p.push(1.0)
        }
    }
    x
}

pub fn sigmoid(x: f64) -> f64 {
    1.0 / (1.0 + (-x).exp())
}

pub fn compute_logistic_gradient(
    x: &Array2<f64>,
    y: &Array1<f64>,
    weights: &Array1<f64>,
) -> Array1<f64> {
    let mu = x.dot(weights);
    let mu = mu.mapv(sigmoid);
    x.t().dot(&(mu - y))
}

pub fn compute_logistic_loss(x: &Array2<f64>, y: &Array1<f64>, weights: &Array1<f64>) -> f64 {
    let mu = x.dot(weights);
    let mu = mu.mapv(sigmoid);
    let log_mu = y * mu.mapv(f64::ln);
    let n = x.nrows() as f64;
    -(1.0 / n) * y.t().dot(&log_mu) - (1.0 - y).t().dot(&(1.0 - mu).mapv(f64::ln))
}

pub fn init_vector(n: usize) -> Array1<f64> {
    let mut rng = thread_rng();
    let v: Vec<f64> = (0..n).map(|_| rng.gen_range(0.0..1.0)).collect();
    Array1::from(v)
}
