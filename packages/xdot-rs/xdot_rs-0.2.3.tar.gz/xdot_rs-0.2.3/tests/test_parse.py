import pytest
import xdot_rs
from xdot_rs.draw import Pen
from xdot_rs.shapes import Ellipse


def test_import_structure():
    assert callable(xdot_rs.parse)  # not a FunctionType?
    # TODO: assert xdot_rs.parse.__module__ == "xdot_rs"
    assert isinstance(xdot_rs.ShapeDraw, type)
    assert xdot_rs.ShapeDraw.__module__ == "xdot_rs"


@pytest.mark.parametrize("input", ["e 27 90 18 3"])
def test_parse(input):
    [sd] = xdot_rs.parse(input)
    ell = Ellipse(27.0, 90.0, 18.0, 3.0, filled=False)
    assert (sd.shape.x, sd.shape.y) == (ell.x, ell.y)
    assert (sd.shape.w, sd.shape.h) == (ell.w, ell.h)
    assert sd.shape.filled == ell.filled
    assert sd.shape == ell
    pen = Pen()
    assert sd.pen.color == pen.color
    assert sd.pen.fill_color == pen.fill_color
    assert sd.pen.line_width == pen.line_width
    assert sd.pen.line_style == pen.line_style
    assert sd.pen.font_size == pen.font_size
    assert sd.pen.font_name == pen.font_name
    assert sd.pen.font_characteristics == pen.font_characteristics
    assert sd.pen == pen
    assert sd == xdot_rs.ShapeDraw(ell, pen)
    assert sd == xdot_rs.ShapeDraw(Ellipse(27.0, 90.0, 18.0, 3.0, filled=False), pen)


def test_uneq():
    pen = Pen(font_size=1.0)
    assert pen != Pen()

    ell = Ellipse(0.0, 0.0, 0.0, 0.0)
    assert xdot_rs.ShapeDraw(ell, pen) != xdot_rs.ShapeDraw(ell, Pen())


def test_parse_error():
    with pytest.raises(ValueError, match=r"error Tag"):
        xdot_rs.parse("")
