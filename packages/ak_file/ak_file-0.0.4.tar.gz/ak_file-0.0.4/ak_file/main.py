#!/usr/bin/env python
# coding: utf-8

from time import ctime
from pathlib import Path

class File:
    def __init__(self, filepath: str)-> None:
        self.filepath=Path(str(filepath))

    def __str__(self) -> str:
        file_prop = self.get_file_properties()
        if self.exists():
            return f"""
Name        : {self.name}
Directory   : {self.parent}
Exists          : True
Access Time     : {file_prop["Access Time"]}
Modified Time   : {file_prop["Modified Time"]}
Change Time     : {file_prop["Change Time"]}
Size            : {file_prop["Size_B"]/1024:.2f} KB
            """
        else:
            return f"""
Name        : {self.name}
Directory   : {self.parent}
Exists          : False
            """

    def __repr__(self) -> str:
        return f'File(filepath="{self.filepath}")'

    @property
    def name(self) -> str:
        "Returns the filename from the current self.filepath"
        return self.filepath.name

    @property
    def parent(self) -> Path:
        "Returns the file directory from the current self.filepath"
        return self.filepath.absolute().parent
    
    @property
    def abspath(self) -> Path:
        "Returns absolute path of the current file"
        return self.filepath.absolute()

    def update_filename(self, new_filename:str, rename_file: bool = False) -> str:
        "Updates the filepath of the stored file"
        new_filepath = self.filepath.parent / new_filename
        if rename_file and self.exists():
            self.filepath.rename(new_filepath)
        self.filepath = new_filepath
        return self.name
    
    def is_file(self) -> bool:
        return self.filepath.is_file()

    def is_dir(self) -> bool:
        return self.filepath.is_dir()

    def exists(self) -> bool:
        return self.filepath.is_file() or self.filepath.is_dir()

    def properties(self) -> dict:
        "Returns a dict of properties of the file"
        stat = self.filepath.stat() if self.exists() else None
        return {
            "name": self.name,
            "dir": self.parent,
            "exists": self.exists(),
            "Access Time": ctime(stat.st_atime) if stat else None,
            "Modified Time": ctime(stat.st_mtime) if stat else None,
            "Change Time" : ctime(stat.st_ctime) if stat else None,
            "Size_B": stat.st_size if stat else None
        }







