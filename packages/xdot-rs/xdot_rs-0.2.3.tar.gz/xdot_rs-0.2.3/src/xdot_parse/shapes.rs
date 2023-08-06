//! Drawable shapes included in [Shape].

/// A drawable shape including closed shapes, lines, and text.
#[derive(Debug, Clone, PartialEq)]
pub enum Shape {
    Ellipse(Ellipse),
    Points(Points),
    Text(Text),
}

/// A horizontal ellipse shape.
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(
    feature = "pyo3",
    pyo3::pyclass(get_all, set_all, module = "xdot_rs.shapes")
)]
pub struct Ellipse {
    pub filled: bool,
    pub x: f32,
    pub y: f32,
    pub w: f32,
    pub h: f32,
}
#[cfg(feature = "pyo3")]
#[pyo3::pymethods]
impl Ellipse {
    #[new]
    #[pyo3(signature = (x, y, w, h, filled=true))]
    fn new(x: f32, y: f32, w: f32, h: f32, filled: bool) -> Self {
        Ellipse { x, y, w, h, filled }
    }
}
impl_richcmp_eq!(Ellipse);
impl From<Ellipse> for Shape {
    fn from(val: Ellipse) -> Self {
        Shape::Ellipse(val)
    }
}

/// Type of shape defined by a sequence of points.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
    feature = "pyo3",
    pyo3::pyclass(get_all, set_all, module = "xdot_rs.shapes")
)]
pub enum PointsType {
    Polygon,
    Polyline,
    BSpline,
}
/// Shape defined by a sequence of points (line or closed shape).
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(
    feature = "pyo3",
    pyo3::pyclass(get_all, set_all, module = "xdot_rs.shapes")
)]
pub struct Points {
    pub filled: bool,
    pub r#type: PointsType,
    pub points: Vec<(f32, f32)>,
}
#[cfg(feature = "pyo3")]
#[pyo3::pymethods]
impl Points {
    #[new]
    #[pyo3(signature = (r#type, points, filled=true))]
    fn new(r#type: PointsType, points: Vec<(f32, f32)>, filled: bool) -> Self {
        Points {
            points,
            r#type,
            filled,
        }
    }
}
impl_richcmp_eq!(Points);
impl From<Points> for Shape {
    fn from(val: Points) -> Self {
        Shape::Points(val)
    }
}

/// Horizontal text alignment: left, center, or right.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
    feature = "pyo3",
    pyo3::pyclass(get_all, set_all, module = "xdot_rs.shapes")
)]
pub enum TextAlign {
    Left,
    Center,
    Right,
}
/// Multiline text for node or edge labels.
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(
    feature = "pyo3",
    pyo3::pyclass(get_all, set_all, module = "xdot_rs.shapes")
)]
pub struct Text {
    pub x: f32,
    pub y: f32,
    pub align: TextAlign,
    pub width: f32,
    pub text: String,
}
#[cfg(feature = "pyo3")]
#[pyo3::pymethods]
impl Text {
    #[new]
    fn new(x: f32, y: f32, align: TextAlign, width: f32, text: String) -> Self {
        Text {
            x,
            y,
            align,
            width,
            text,
        }
    }
}
impl_richcmp_eq!(Text);
impl From<Text> for Shape {
    fn from(val: Text) -> Self {
        Shape::Text(val)
    }
}

/// External image, currently unimplemented.
#[doc(hidden)]
#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq, PartialOrd, Ord)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(module = "xdot_rs.shapes"))]
pub struct ExternalImage;

#[cfg(feature = "pyo3")]
#[pyo3::pymodule]
#[pyo3(name = "shapes")]
pub fn pymodule(_py: pyo3::Python, m: &pyo3::types::PyModule) -> pyo3::PyResult<()> {
    m.add_class::<Ellipse>()?;
    m.add_class::<PointsType>()?;
    m.add_class::<Points>()?;
    m.add_class::<TextAlign>()?;
    m.add_class::<Text>()?;
    m.add_class::<ExternalImage>()?;
    Ok(())
}
