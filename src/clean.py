import shutil
from pathlib import Path
from typing import Union

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json


class OrganizerFiles:
    """
    This class is used to or organize files in a directory by
    moving files into directories based on extensions. 
    """
    def __init__(self):
        ext_dirs = read_json(DATA_DIR / "extentions.json")
        self.extentions_dest = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extentions_dest[ext] = dir_name

    def __call__(self, directory: Union[str, Path]):
        """ Organize files in a directory by moving them
        to sub directories based on extension.
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"{directory} dose not exist")

        logger.info(f"Organizing files in {directory}...")
        file_extentions = []
        for file_path in directory.iterdir():
            # ignore directories
            if file_path.is_dir():
                continue

            # ignore hidden files
            if file_path.name.startswith('.'):
                continue

            # move files
            file_extentions.append(file_path.suffix)
            if file_path.suffix not in self.extentions_dest:
                DEST_DIR = directory / 'other'
            else:
                DEST_DIR = directory / self.extentions_dest[file_path.suffix]

            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f"Moving {file_path} to {DEST_DIR}...")
            shutil.move(str(file_path), str(DEST_DIR))


if __name__ == "__main__":
    org_files = OrganizerFiles()
    org_files('/home/amir/Downloads')
    logger.info("Done!")
