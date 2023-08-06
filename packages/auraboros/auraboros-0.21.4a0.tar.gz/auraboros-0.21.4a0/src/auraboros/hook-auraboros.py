from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

SCRIPT_PARENT = Path(__file__).absolute().parent

datas = collect_data_files('auraboros') + [
    str(SCRIPT_PARENT / "default.frag"), str(SCRIPT_PARENT / "default.vert")]
