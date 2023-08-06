//! Drawing attributes for lines, shapes, and text.

mod attrs;

pub use self::attrs::{FontCharacteristics, Rgba, Style};

/// Stores attributes for lines, shapes, and text, such as color and font.
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(
    feature = "pyo3",
    pyo3::pyclass(get_all, set_all, module = "xdot_rs.draw")
)]
pub struct Pen {
    pub color: Rgba,
    pub fill_color: Rgba,
    pub line_width: f32,
    pub line_style: Style,
    pub font_size: f32,
    pub font_name: String,
    pub font_characteristics: FontCharacteristics,
}
impl Default for Pen {
    fn default() -> Self {
        Pen {
            color: Default::default(),
            fill_color: Default::default(),
            line_width: 1.0,
            line_style: Default::default(),
            font_size: 14.0,
            font_name: "Times-Roman".to_owned(),
            font_characteristics: Default::default(),
        }
    }
}
#[cfg(feature = "pyo3")]
#[pyo3::pymethods]
impl Pen {
    #[new]
    #[pyo3(signature = (
        color=Default::default(),
        fill_color=Default::default(),
        line_width=1.0,
        line_style=Default::default(),
        font_size=14.0,
        font_name="Times-Roman".to_owned(),
        font_characteristics=Default::default(),
    ))]
    fn new(
        color: Rgba,
        fill_color: Rgba,
        line_width: f32,
        line_style: Style,
        font_size: f32,
        font_name: String,
        font_characteristics: FontCharacteristics,
    ) -> Self {
        Pen {
            color,
            fill_color,
            line_width,
            line_style,
            font_size,
            font_name,
            font_characteristics,
        }
    }
}
impl_richcmp_eq!(Pen);

#[cfg(feature = "pyo3")]
#[pyo3::pymodule]
#[pyo3(name = "draw")]
pub fn pymodule(_py: pyo3::Python, m: &pyo3::types::PyModule) -> pyo3::PyResult<()> {
    m.add_class::<FontCharacteristics>()?;
    m.add_class::<Rgba>()?;
    m.add_class::<Style>()?;
    m.add_class::<Pen>()?;
    Ok(())
}
