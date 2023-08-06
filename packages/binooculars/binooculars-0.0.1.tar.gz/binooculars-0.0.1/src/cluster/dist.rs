pub fn euclidean_distance(x: Vec<f64>, y: Vec<f64>) -> f64 {
    let mut sum = 0.0;
    for i in 0..x.len() {
        sum += (x[i] - y[i]).powi(2);
    }
    sum.sqrt()
}
