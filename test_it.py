import os
import shutil

TARGET = "AutoStructureFilesForDFplayer.py"


def execute_target(tmp_path):
    # Copy SUT to temp dir and execute
    shutil.copyfile(TARGET, tmp_path / TARGET)
    os.chdir(tmp_path)
    os.system(TARGET)


def test_copies_script(tmp_path):
    execute_target(tmp_path)
    d = tmp_path / TARGET
    assert d.exists()


def test_creates_playlist_folder(tmp_path):
    execute_target(tmp_path)
    d = tmp_path / 'PlayListsM3U'
    assert d.exists()


def test_creates_sdcard_folder(tmp_path):
    execute_target(tmp_path)
    d = tmp_path / 'SDcardFolders'
    assert d.exists()
