use pyo3::prelude::*;

mod linear {
    pub mod regression;
    mod utils;
    pub use crate::linear::regression::{LinearRegressionRust, LogisticRegressionRust};
}

mod cluster {
    mod dist;
    pub mod kmeans;
    pub use crate::cluster::kmeans::KMeansRust;
}

/// This module is implemented in Rust.
#[pymodule]
#[pyo3(name = "binoculars")]
fn my_extension(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<linear::LinearRegressionRust>()?;
    m.add_class::<linear::LogisticRegressionRust>()?;
    m.add_class::<cluster::KMeansRust>()?;
    Ok(())
}
