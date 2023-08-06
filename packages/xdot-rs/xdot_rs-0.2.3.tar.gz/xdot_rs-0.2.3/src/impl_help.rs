#[macro_export]
macro_rules! impl_richcmp_eq {
    ($cls: path) => {
        #[cfg(feature = "pyo3")]
        #[pyo3::pymethods]
        impl $cls {
            fn __richcmp__(
                &self,
                other: &Self,
                op: pyo3::pyclass::CompareOp,
                py: pyo3::Python,
            ) -> pyo3::PyObject {
                use pyo3::pyclass::CompareOp::*;
                use pyo3::IntoPy;

                return match op {
                    Eq => (self == other).into_py(py),
                    Ne => (self != other).into_py(py),
                    _ => py.NotImplemented(),
                };
            }
        }
    };
}

#[macro_export]
macro_rules! impl_bitflags_accessors {
    ($cls: path, $( $flag: ident ),+ $(,)?) => {
        paste::paste! {
            #[cfg(feature = "pyo3")]
            #[pyo3::pymethods]
            impl $cls {
                $(
                    #[getter]
                    fn [< get_ $flag >](&self) -> bool {
                        self.contains($cls::[< $flag:upper >])
                    }
                    #[setter]
                    fn [< set_ $flag >](&mut self, value: bool) {
                        self.set($cls::[< $flag:upper >], value);
                    }
                )+
            }
        }
    };
}
