pub mod lca;
use exposure::TreeSet;
pub use lca::*;
pub mod exposure;
use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
fn table_fifth(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<TreeSet>()?;
    Ok(())
}
