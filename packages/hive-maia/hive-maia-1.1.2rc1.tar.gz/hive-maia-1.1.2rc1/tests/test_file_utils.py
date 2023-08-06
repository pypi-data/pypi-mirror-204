from Hive.utils.file_utils import subfolders, subfiles
import os


def test_subfiles_and_subfolders():
    subfiles( os.getcwd())
    subfolders(os.getcwd())