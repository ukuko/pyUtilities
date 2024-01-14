import os
import pytest
import shutil
from renamer import Renamer


TEST_FOLDER = os.path.join('tests', 'folder')


def test_rename_file_within_folder():
    renamer = Renamer({'--directory': TEST_FOLDER,
                       '--pattern': 'file_ABC',
                       '--replacement': 'new_filename',
                       '--recursive': 'True',
                       '--ignore-folders': ''})

    # Remove existing files to ensure clean tests
    shutil.rmtree(os.path.join(TEST_FOLDER, 'new_filename.ext'))

    renamer.rename_files()

    # Check for renamed file
    assert os.path.exists(os.path.join(TEST_FOLDER, 'new_filename.ext'))


def test_rename_file_in_subfolder():
    renamer = Renamer({'--directory': TEST_FOLDER,
                       '--pattern': 'file_ABCD',
                       '--replacement': 'new_filename',
                       '--recursive': 'True',
                       '--ignore-folders': ''})

    # Remove existing files to ensure clean tests
    shutil.rmtree(os.path.join(TEST_FOLDER, 'subfolder', 'new_filename.ext'))

    renamer.rename_files()

    # Check for renamed file in subfolder
    assert os.path.exists(os.path.join(TEST_FOLDER, 'subfolder', 'new_filename.ext'))


def test_rename_file_with_extension():
    renamer = Renamer({'--directory': TEST_FOLDER,
                       '--pattern': 'file2_BCD_test.ext',
                       '--replacement': 'new_filename.ext',
                       '--recursive': 'True',
                       '--ignore-folders': ''})

    # Remove existing files to ensure clean tests
    shutil.rmtree(os.path.join(TEST_FOLDER, 'new_filename.ext'))

    renamer.rename_files()

    # Check for renamed file with extension
    assert os.path.exists(os.path.join(TEST_FOLDER, 'new_filename.ext'))
