from ak_file.search import *
from pathlib import Path

parent_dir = Path(__file__).parent.parent

def test_by_extension():
    assert len(list(by_extension(parent_dir, 'py', False))) == 0
    assert len(list(by_extension(parent_dir, 'toml', False))) == 1

def test_by_regex():
    assert len(by_regex(parent_dir, r'.*.PY$',True, True)) == 0
    assert len(by_regex(parent_dir, r'.*.PY$',True, False)) > 0