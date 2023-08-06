from pathlib import Path
from typing import Generator
import re

def by_extension(folder_path:str, extension:str, search_subdir:bool=False) -> Generator[Path, None, None]:
    "Returns a list of files in the directory with matching extension"
    return Path(str(folder_path)).glob(f"{'**/' if search_subdir else ''}*.{extension}")

def by_regex(
    folder_path: str, 
    regex_pattern: str, 
    search_subdir:bool=False, 
    case_sensitive:bool=False) -> list[Path]:

    folder_path = Path(str(folder_path))

    if (not case_sensitive) and (not regex_pattern.startswith("(?i)")):
        regex_pattern = "(?i)" + regex_pattern
    
    regex = re.compile(regex_pattern)

    files = folder_path.glob(f"{'**/' if search_subdir else ''}*")
    return [ file for file in files if regex.search(file.name)]
