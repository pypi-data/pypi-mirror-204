use std::{path::PathBuf, rc::Rc, sync::Arc};

use crate::TreeCollectionWithLCA;
use ogcat::ogtree::TreeCollection;
use pyo3::prelude::*;

#[pyclass]
pub struct TreeSet {
    data: Arc<TreeCollectionWithLCA>,
}

#[pymethods]
impl TreeSet {
    #[new]
    pub fn new(path: PathBuf) -> PyResult<Self> {
        let tc = TreeCollection::from_newick(path).expect("Failed to load tree collection");
        let wrapped = TreeCollectionWithLCA::from_tree_collection(tc);
        Ok(Self { data: Arc::new(wrapped) })
    }

    pub fn __len__(&self) -> usize {
        self.data.collection.trees.len()
    }

    pub fn tally_single_quintet(&self, names: (&str, &str, &str, &str, &str)) -> Vec<usize> {
        let mut res = vec![0usize; 15];
        let transl = self.data.translate_taxon_names(names);
        for (i, lca) in self.data.lca.iter().enumerate() {
            let quintet = [
                lca.rev[transl.0],
                lca.rev[transl.1],
                lca.rev[transl.2],
                lca.rev[transl.3],
                lca.rev[transl.4],
            ];
            if quintet.iter().any(|it| *it == 0) {
                continue;
            }
            if let Some(t) = lca.retrieve_topology(&quintet) {
                res[t as usize] += 1;
            }
        }
        res
    }

    pub fn coalesence_times_by_topology(&self, names: (&str, &str, &str, &str, &str)) -> Vec<f64> {
        let mut res = vec![0.0; 15 + 15 * 10];
        let transl = self.data.translate_taxon_names(names);
        for (i, lca) in self.data.lca.iter().enumerate() {
            let quintet = [
                lca.rev[transl.0],
                lca.rev[transl.1],
                lca.rev[transl.2],
                lca.rev[transl.3],
                lca.rev[transl.4],
            ];
            if quintet.iter().any(|it| *it == 0) {
                continue;
            }
            if let Some(t) = lca.retrieve_topology(&quintet) {
                res[t as usize] += 1.0;
                let start_ix = 15 + 10 * t as usize;
                let lca_extra = &self.data.lca_extras[i];
                let dists = lca_extra.retrieve_branch_length_distances(lca, &quintet);
                assert_eq!(dists.len(), 10);
                for (ix, d) in dists.iter().enumerate() {
                    res[start_ix + ix] += d;
                }
            }
        }
        let first_fifteen_sum = res[0..15].iter().sum::<f64>();
        if first_fifteen_sum > 0.0 {
            for i in 0..15 {
                res[i] /= first_fifteen_sum;
            }
        }
        for i in 0..15 {
            let start_ix = 15 + 10 * i;
            let sum = res[start_ix..start_ix + 10].iter().sum::<f64>();
            if sum > 0.0 {
                for j in 0..10 {
                    res[start_ix + j] /= sum;
                }
            }
        }
        res
    }

    pub fn __getitem__(&self, id: usize) -> PyResult<SingleTree> {
        Ok(SingleTree {
            treeset: self.data.clone(),
            id,
        })
    }
}

#[pyclass]
pub struct SingleTree {
    pub treeset : Arc<TreeCollectionWithLCA>,
    pub id : usize,
}

#[pymethods]
impl SingleTree {
    pub fn retrieve_quintet_type(&self, names: (&str, &str, &str, &str, &str)) -> Option<u8> {
        let transl = self.treeset.translate_taxon_names(names);
        let lca = &self.treeset.lca[self.id];
        let quintet = [
            lca.rev[transl.0],
            lca.rev[transl.1],
            lca.rev[transl.2],
            lca.rev[transl.3],
            lca.rev[transl.4],
        ];
        if quintet.iter().any(|it| *it == 0) {
            return None;
        }
        lca.retrieve_topology(&quintet)
    }

    pub fn retrieve_all_pairs_distance(&self, names: (&str, &str, &str, &str, &str)) -> Option<Vec<f64>> {
        let transl = self.treeset.translate_taxon_names(names);
        let lca = &self.treeset.lca[self.id];
        let lca_extra = &self.treeset.lca_extras[self.id];
        let quintet = [
            lca.rev[transl.0],
            lca.rev[transl.1],
            lca.rev[transl.2],
            lca.rev[transl.3],
            lca.rev[transl.4],
        ];
        if quintet.iter().any(|it| *it == 0) {
            return None;
        }
        Some(lca_extra.retrieve_branch_length_distances(lca, &quintet))
    }
}