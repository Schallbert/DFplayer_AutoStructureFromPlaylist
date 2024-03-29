import shutil
import os
import pytest

ROOTDIR = os.getcwd()
TARGET = 'AutoStructureFilesForDFplayer.py'
PLAYLISTFOLDER = 'PlayListsM3U'
SDCARDFOLDER = 'SDcardFolders'
TESTFOLDER = 'test'
DUMMYPLAYLISTS = os.sep.join([ROOTDIR, TESTFOLDER, 'm3u_source'])
DUMMYCONTENT = os.sep.join([ROOTDIR, TESTFOLDER, 'mp3_source'])


def execute_target(tmp_path):
    os.chdir(tmp_path)
    return os.system(TARGET)


@pytest.fixture
def copy_target_to_temp(tmp_path):
    """places SUT in temporary path to prepare for execution"""
    shutil.copyfile(TARGET, os.sep.join([str(tmp_path), TARGET]))


@pytest.fixture
def execute_happy_path(tmp_path, copy_target_to_temp):
    """Executes script under test, then copies test files into SUT folder structure.
    Finally, executes SUT again to get the file operations done."""
    execute_target(tmp_path)
    copy_dummy_content_to_temp(tmp_path)


def copy_dummy_content_to_temp(tmp_path):
    """after execute_target is run, this function copies the dummy contents to the playlists"""
    # Copy dummy m3u playlists
    target_playlist_path = os.sep.join([str(tmp_path), PLAYLISTFOLDER])
    target_content_path = os.sep.join([str(tmp_path), 'mp3_source'])
    for file in os.listdir(DUMMYPLAYLISTS):
        shutil.copyfile(os.sep.join([DUMMYPLAYLISTS, file]), os.sep.join([target_playlist_path, file]))
    # Copy dummy mp3 content
    shutil.copytree(DUMMYCONTENT, target_content_path)


def test_can_copy_to_temp(tmp_path, copy_target_to_temp):
    d = tmp_path / TARGET
    assert d.exists()


def test_can_execute_target(tmp_path, copy_target_to_temp):
    assert execute_target(tmp_path) == 0


def test_creates_playlist_folder(tmp_path, copy_target_to_temp):
    execute_target(tmp_path)
    d = tmp_path / PLAYLISTFOLDER
    assert d.exists()


def test_creates_sdcard_folder(tmp_path, copy_target_to_temp):
    execute_target(tmp_path)
    d = tmp_path / SDCARDFOLDER
    assert d.exists()


def test_copies_playlists_to_folder(tmp_path, copy_target_to_temp):
    execute_target(tmp_path)
    copy_dummy_content_to_temp(tmp_path)
    d = tmp_path / PLAYLISTFOLDER
    cpyfiles = os.listdir(d)
    srcfiles = os.listdir(DUMMYPLAYLISTS)
    assert len(cpyfiles) == len(srcfiles)


def test_creates_folders_from_dummy(tmp_path, execute_happy_path):
    execute_target(tmp_path)
    p = tmp_path / SDCARDFOLDER
    d = p / '01'
    assert d.exists()
    d = p / '02'
    assert d.exists()
    d = p / '03'
    assert d.exists()


def test_happy_path_success(tmp_path, execute_happy_path):
    assert execute_target(tmp_path) == 0


def test_creates_files_from_dummy(tmp_path, execute_happy_path):
    execute_target(tmp_path)
    p = tmp_path / SDCARDFOLDER
    d = p / '01'
    assert len(os.listdir(d)) == 7
    d = p / '02'
    assert len(os.listdir(d)) == 7
    d = p / '03'
    assert len(os.listdir(d)) == 7


def test_creates_correct_filenames(tmp_path, execute_happy_path):
    execute_target(tmp_path)
    # 3 test playlists
    for w in range(1, 4):
        path = tmp_path / SDCARDFOLDER / ('0' + str(w))
        # 7 tracks per test playlist
        for x in range(1, 8):
            filename = '00' + str(x) + '.mp3'
            file = path / filename
            assert file.exists()


def test_renames_playlists_align_folder_numbers(tmp_path, execute_happy_path):
    execute_target(tmp_path)
    playlists = os.listdir(PLAYLISTFOLDER)
    playlist_number = 0
    for playlist in playlists:
        playlist_number = playlist_number + 1
        assert playlist.find(str(playlist_number), 0, 2) != -1
