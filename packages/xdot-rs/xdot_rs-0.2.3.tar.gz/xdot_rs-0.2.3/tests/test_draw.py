from types import ModuleType

from xdot_rs import draw


def test_import_structure():
    assert isinstance(draw, ModuleType)
    assert isinstance(draw.FontCharacteristics, type)
    assert draw.FontCharacteristics.__module__ == "xdot_rs.draw"
    assert isinstance(draw.Rgba, type)
    assert isinstance(draw.Style, type)
    assert isinstance(draw.Pen, type)


def test_font_characteristics():
    fc1 = draw.FontCharacteristics()
    fc2 = draw.FontCharacteristics(bold=True)
    assert fc1 != fc2
    assert not fc1.bold
    assert fc2.bold
    assert repr(fc2) == "FontCharacteristics(BOLD)"
