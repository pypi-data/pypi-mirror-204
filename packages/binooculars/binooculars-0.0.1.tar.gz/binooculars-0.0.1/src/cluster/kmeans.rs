use std::vec::IntoIter;

use crate::cluster::dist::euclidean_distance;
use itertools::Itertools;
use pyo3::prelude::*;
use rand::{Rng, SeedableRng};
use rand_chacha::ChaCha8Rng;

#[pyclass]
pub struct KMeansRust {
    k: usize,
    num_iter: usize,
    init: String,
    centroids: Vec<Vec<f64>>,
    rng: ChaCha8Rng,
    x: Vec<Vec<f64>>,
}

#[pymethods]
impl KMeansRust {
    #[new]
    fn new(k: usize, init: String, num_iter: usize, random_state: usize) -> Self {
        KMeansRust {
            k,
            num_iter,
            init,
            centroids: Vec::new(),
            rng: ChaCha8Rng::seed_from_u64(random_state as u64),
            x: Vec::new(),
        }
    }

    fn with_k(&mut self, k: usize) -> PyResult<()> {
        self.k = k;
        Ok(())
    }

    fn with_num_iter(&mut self, num_iter: usize) -> PyResult<()> {
        self.num_iter = num_iter;
        Ok(())
    }

    fn with_random_state(&mut self, random_state: usize) -> PyResult<()> {
        self.rng = ChaCha8Rng::seed_from_u64(random_state as u64);
        Ok(())
    }

    fn with_init(&mut self, init: String) -> PyResult<()> {
        self.init = init;
        Ok(())
    }

    fn get_centroids(&self) -> PyResult<Vec<Vec<f64>>> {
        Ok(self.centroids.to_vec())
    }

    fn set_centroids(&mut self, centroids: Vec<Vec<f64>>) -> PyResult<()> {
        self.centroids = centroids;
        Ok(())
    }

    fn kmeans_mapper(&self, x: Vec<f64>) -> (usize, (Vec<f64>, usize)) {
        let (_dist, idx) = self
            .centroids
            .iter()
            .enumerate()
            .map(|(e, c)| (euclidean_distance(x.to_vec(), c.to_vec()), e))
            .fold((std::f64::MAX, 0), |(min_dist, min_idx), (dist, idx)| {
                if dist < min_dist {
                    (dist, idx)
                } else {
                    (min_dist, min_idx)
                }
            });
        (idx, (x, 1))
    }

    fn kmeans_reducer(&self, xs: Vec<(Vec<f64>, usize)>) -> Vec<f64> {
        let (sum, count) = xs
            .iter()
            .fold((vec![0.0; xs[0].0.len()], 0), |(sum, count), (x, c)| {
                (
                    sum.iter().zip(x.iter()).map(|(a, b)| a + b).collect(),
                    count + c,
                )
            });
        sum.iter().map(|x| x / count as f64).collect_vec()
    }
    fn fit(&mut self, x: Vec<Vec<f64>>) -> PyResult<()> {
        self.x = x.to_vec();
        self.centroids = self.init_centroids();

        for _ in 0..self.num_iter {
            self.centroids = self
                .x
                .iter()
                .map(|x| self.kmeans_mapper(x.to_vec()))
                .sorted_by_key(|x| x.0)
                .group_by(|x| x.0)
                .into_iter()
                .map(|(_g, x)| self.kmeans_reducer(x.map(|x| x.1).collect()))
                .collect::<Vec<Vec<f64>>>();
        }
        Ok(())
    }

    fn init_centroids(&mut self) -> Vec<Vec<f64>> {
        let mut centroids = Vec::new();
        if self.init == "random" {
            for _ in 0..self.k {
                let idx = self.rng.gen_range(0..self.x.len());
                centroids.push(self.x[idx].to_vec());
            }
        } else if self.init == "kmeans++" {
            panic!("Not implemented yet");
        }
        centroids
    }

    fn predict(&self, x: Vec<Vec<f64>>) -> PyResult<Vec<usize>> {
        let y = x
            .iter()
            .map(|x| self.kmeans_mapper(x.to_vec()))
            .map(|x| x.0)
            .collect::<Vec<usize>>();
        Ok(y)
    }
}
