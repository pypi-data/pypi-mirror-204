from ak_file.main import *
from pathlib import Path

root = Path(__file__).parent.parent

class Test_File:
    file1 = File(root / "README.md")
    folder1 = File(root / "tests")
    file2 = File(root / "ak_file" / "__init__.py")
    folder2 = File(root / "ak_file")

    def test_name(self):
        assert self.file1.name == "README.md"
        assert self.folder1.name == "tests"
        assert self.file2.name == "__init__.py"
        assert self.folder2.name == "ak_file"

    def test_parent(self):
        assert self.file2.parent.name == "ak_file"
        assert self.file1.parent == self.folder1.parent
        assert self.file1.parent == self.folder2.parent
    
    def test_is_file(self):
        assert self.file1.is_file() == True
        assert self.folder1.is_file() == False
        assert self.file2.is_file() == True
        assert self.folder1.is_file() == False

    def test_is_dir(self):
        assert self.file1.is_dir() == False
        assert self.folder1.is_dir() == True
        assert self.file2.is_dir() == False
        assert self.folder1.is_dir() == True

    def test_exists(self):
        assert self.file1.exists() == True
        assert self.folder1.exists() == True
        assert self.file2.exists() == True
        assert self.folder1.exists() == True