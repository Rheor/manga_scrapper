import os
from kissmanga.exceptions import FolderCreationError

def create_dir(path):
    try:
        os.mkdir(path)
    except OSError as exc:
        if "already exists" not in str(exc):
            raise FolderCreationError()
