//! Types reused for drawing things.
use std::str::FromStr;

use bitflags::bitflags;

/// RGBA color representation with 8 bit per channel.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
    feature = "pyo3",
    pyo3::pyclass(get_all, set_all, module = "xdot_rs.draw")
)]
pub struct Rgba {
    pub r: u8,
    pub g: u8,
    pub b: u8,
    pub a: u8,
}
impl Default for Rgba {
    fn default() -> Self {
        Rgba {
            r: 0,
            g: 0,
            b: 0,
            a: 0xff,
        }
    }
}
impl_richcmp_eq!(Rgba);

/// Line style for node borders and edges.
/// See [here](https://graphviz.org/docs/attr-types/style/).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
#[cfg_attr(
    feature = "pyo3",
    pyo3::pyclass(get_all, set_all, module = "xdot_rs.draw")
)]
pub enum Style {
    Dashed,
    Dotted,
    #[default]
    Solid,
    Invis,
    Bold,
    // TODO: "tapered" for edges only
}
impl FromStr for Style {
    type Err = String;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        use Style::*;
        Ok(match s {
            "dashed" => Dashed,
            "dotted" => Dotted,
            "solid" => Solid,
            "invis" => Invis,
            "bold" => Bold,
            s => return Err(s.to_owned()),
        })
    }
}
impl_richcmp_eq!(Style);

bitflags! {
    /// Font weight and decorations.
    /// Matches values defined [here](https://graphviz.org/docs/outputs/canon/#xdot).
    #[derive(Default)]
    #[cfg_attr(
        feature = "pyo3",
        pyo3::pyclass(get_all, set_all, module = "xdot_rs.draw")
    )]
    pub struct FontCharacteristics: u128 {
        const BOLD           = 0b00000001;
        const ITALIC         = 0b00000010;
        const UNDERLINE      = 0b00000100;
        const SUPERSCRIPT    = 0b00001000;
        const SUBSCRIPT      = 0b00010000;
        const STRIKE_THROUGH = 0b00100000;
        const OVERLINE       = 0b01000000;
    }
}
#[cfg(feature = "pyo3")]
#[pyo3::pymethods]
impl FontCharacteristics {
    #[new]
    #[pyo3(signature = (
        bold=false,
        italic=false,
        underline=false,
        superscript=false,
        subscript=false,
        strike_through=false,
        overline=false,
    ))]
    fn new(
        bold: bool,
        italic: bool,
        underline: bool,
        superscript: bool,
        subscript: bool,
        strike_through: bool,
        overline: bool,
    ) -> Self {
        let mut fc = FontCharacteristics::empty();
        fc.set_bold(bold);
        fc.set_italic(italic);
        fc.set_underline(underline);
        fc.set_superscript(superscript);
        fc.set_subscript(subscript);
        fc.set_strike_through(strike_through);
        fc.set_overline(overline);
        fc
    }
    fn __repr__(&self) -> String {
        format!("FontCharacteristics({:?})", self)
    }
}
impl_bitflags_accessors!(
    FontCharacteristics,
    bold,
    italic,
    underline,
    superscript,
    subscript,
    strike_through,
    overline,
);
impl_richcmp_eq!(FontCharacteristics);
