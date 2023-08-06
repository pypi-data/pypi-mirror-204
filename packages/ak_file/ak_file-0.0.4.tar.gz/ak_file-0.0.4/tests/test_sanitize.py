from ak_file.sanitize import *

def test_blacklist():
    assert sanitize("a\\b/c:d*e?f\"g<h>i|j\0k") == "abcdefghijk"

def test_reserved():
    for each in reserved:
        assert sanitize(each) != each

def test_length():
    assert len(sanitize("gradsf"*250)) == 255
    assert len(sanitize("gra:d\\sf"*250)) == 255

def test_special():
    assert sanitize("") == '__'