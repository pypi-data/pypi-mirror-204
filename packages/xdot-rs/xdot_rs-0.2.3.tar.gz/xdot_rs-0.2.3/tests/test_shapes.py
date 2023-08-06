from types import ModuleType

from xdot_rs import shapes


def test_import_structure():
    assert isinstance(shapes, ModuleType)
    # TODO: add superclass: assert isinstance(shapes.Shape, type)
    assert isinstance(shapes.Ellipse, type)
    assert shapes.Ellipse.__module__ == "xdot_rs.shapes"
    assert isinstance(shapes.PointsType, type)
    assert isinstance(shapes.Points, type)
    assert isinstance(shapes.TextAlign, type)
    assert isinstance(shapes.Text, type)
    assert isinstance(shapes.ExternalImage, type)
