use std::borrow::BorrowMut;
use std::collections::HashMap;
use std::hash::Hash;

use ndarray::parallel::prelude::{IntoParallelIterator, ParallelIterator};
use ndarray::{ArrayD, ArrayViewD, Array3, ArrayView2, Axis, Array1};
use pyo3::prelude::*;
use rayon::prelude::*;
use numpy::ndarray::Zip;
use numpy::{IntoPyArray, PyArray1, PyReadonlyArray1, PyReadonlyArray2, PyReadonlyArrayDyn, PyArrayDyn, PyArray3};
use pyo3::{pymodule, types::PyModule, PyResult, Python};

#[derive(Clone, Copy, Debug)]
struct HeightCell {
    pub height: f32,
    pub n_points: u32
}

impl HeightCell {
    fn new() -> Self {
        HeightCell { height: 0.0, n_points: 0 }
    }
    fn add_point(&mut self, n_height: f32) {
        self.height = self.height.max(n_height);
        self.n_points += 1;
    }
    fn merge(&mut self, hc: &HeightCell) {
        self.height = self.height.max(hc.height);
        self.n_points += hc.n_points;
    }
}



#[derive(PartialEq, Eq, Hash, Clone, Copy, Debug)]
struct Coordinate {
    x: u32,
    y: u32,
}

impl Coordinate {
    fn from_xy(x: f32, y: f32) -> Coordinate {
        Coordinate {
            x: x as u32,
            y: y as u32
        }
    }
}

type HFormat = f32;


// example using immutable borrows producing a new array
#[inline(always)]
fn build_hmap(points: ArrayView2<'_, f32>, map_size: usize, matrix_size: usize) -> Array3<HFormat> {
    let half_size = (map_size as f32) / 2.0;

    let k = points
     .axis_iter(ndarray::Axis(0))
     .into_par_iter()
     .with_min_len(4096)
     .filter(|point| {
         point[0].abs() < half_size && point[1].abs() < half_size
        })
     .fold(|| HashMap::new(),
        |mut acc, val| {
            let x = ((val[0] + half_size) / (map_size as f32)) * (matrix_size as f32);
            let y = ((val[1] + half_size) / (map_size as f32)) * (matrix_size as f32);
            acc.entry(Coordinate::from_xy(x, y)).or_insert(HeightCell::new()).add_point(-val[2]);
            acc
        })
    .reduce( || HashMap::new(),
    |m1, m2| {
        m2.iter().fold(m1, |mut acc, (&k, vs)| {
            acc.entry(k).or_insert(HeightCell::new()).merge(vs);
            acc
        })
    });

    // let k = points
    //  .axis_iter(ndarray::Axis(0))
    //  .into_par_iter()
    //  .filter(|point| {
    //      point[0].abs() < half_size && point[1].abs() < half_size
    //     })
    //  .fold(|| Array1::from_elem(matrix_size * matrix_size, HeightCell::new()),
    //     |mut acc, val| {
    //         let x = ((val[0] + half_size) / (map_size as f32)) * (matrix_size as f32);
    //         let y = ((val[1] + half_size) / (map_size as f32)) * (matrix_size as f32);
    //         acc[(x as usize) * matrix_size + (y as usize)].add_point(-val[2]);
    //         acc
    //     })
    // .reduce( || Array1::from_elem(matrix_size * matrix_size, HeightCell::new()),
    // |mut m1, m2| {
    //     Zip::from(&mut m1).and(&m2).par_for_each(|a, b| {
    //         a.merge(b);
    //     });
    //     m1
    // });

    let mut hm: Array3<HFormat> = Array3::zeros((matrix_size, matrix_size, 3));
    // if k.is_none() {
    //     return hm;
    // }
    // let arange = Array1::from_shape_fn(map_size, |i| i);
    // let mut hmv = hm.view_mut();
    // Zip::from(&arange).and(&arange).par_for_each(|x, y| {
    //     (&hmv)[[*x, *y, 0]] = 1.0;
    // });
    // hm.axis_iter_mut(Axis(0)).into_par_iter().enumerate().for_each(|(x, mut row)| {
    //     for (y, mut item) in row.axis_iter_mut(Axis(0)).enumerate() {
    //         if let Some(points) = k.get(&Coordinate { x: x as u32 + 1, y: y as u32  + 1}) {
    //             let maximum: f32 = points.height;
    //             // item[0] = maximum.trunc() as u32;
    //             // item[1] = (maximum.fract() * 255.0) as u32;
    //             // item[2] = (points.len() as f32).checked_ilog2().unwrap_or(0);
    //             item[0] = maximum.trunc();
    //             item[1] = (maximum.fract() * 255.0);
    //             item[2] = points.n_points.checked_ilog2().unwrap_or(0) as f32;

    //         }
    //     }
    // });
    // let heights = k.expect("Should not be empty");
    hm.axis_iter_mut(Axis(0)).into_par_iter().with_min_len(5).with_max_len(10).enumerate().for_each(|(x, mut row)| {
        row.axis_iter_mut(Axis(0)).enumerate().for_each(| (y, mut item)| {
            if let Some(points) = k.get(&Coordinate { x: x as u32 + 1, y: y as u32  + 1}) {
            // {
                // let points = k[x * matrix_size + y];
                let maximum: f32 = points.height;
                // item[0] = maximum.trunc() as u32;
                // item[1] = (maximum.fract() * 255.0) as u32;
                // item[2] = (points.len() as f32).checked_ilog2().unwrap_or(0);
                item[0] = maximum.trunc();
                item[1] = (maximum.fract() * 255.0);
                item[2] = points.n_points.checked_ilog2().unwrap_or(0) as f32;

            }
        })
    });
    hm
}

/// A Python module implemented in Rust.
#[pymodule]
fn hmap(_py: Python, m: &PyModule) -> PyResult<()> {

     // wrapper of `axpy`
    #[pyfn(m)]
    #[pyo3(name = "build_hmap")]
    fn build_hmap_py<'py>(
        py: Python<'py>,
        points: PyReadonlyArray2<'_, f32>,
        map_size: usize,
        matrix_size: usize,
    ) -> &'py PyArray3<HFormat> {
        let points = points.as_array();

        let z = build_hmap(points, map_size, matrix_size);
        z.into_pyarray(py)
    }

    Ok(())
}