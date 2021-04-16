import os
import sys
import os.path
import shutil
# use urllib to escape special (UTF8) characters in filenames
from urllib.parse import unquote

# Author: "Schallbert"

# folder names
PLAYLISTFLDRNAME = "PlayListsM3U"
CARDFLDRNAME = "SDcardFolders"
# player's maximum accepted file cnt
MAXFLDRCNT = 99
MAXFILECNT = 255
M3UFILETYPE = ".m3u"
M3UFILEMARKER = "file:///"
M3UINFOMARKER = "#"
MP3FILEMARKER = ".mp3"


def replace_special_chars_in_path(line_of_playlist):
    """Make sure .m3u file's special characters are converted
    Replace most common UTF8 special characters"""
    return unquote(line_of_playlist)


def find_m3u_filemarker(playlist_line):
    """relevant lines do not begin with # (sharp)
       relevant lines may begin with file:/// which has to be stripped"""
    if playlist_line.find(M3UINFOMARKER) == 0:
        return None

    if playlist_line.find(M3UFILEMARKER):
        # remove file marker
        playlist_line = playlist_line.split(M3UFILEMARKER)[-1]
    # condition line for usage
    playlist_line = playlist_line.strip()  # strip removes New Line markers \n
    playlist_line = replace_special_chars_in_path(playlist_line)
    return playlist_line


def get_name_from_id(indx, max_cnt):
    """Returns a DFplayerMini-compatible way of numbering
    files which is 001, 002, ... 255"""
    if indx > max_cnt:
        quit_with_message("Error: player cannot process more than %s items" % max_cnt)
    return str(indx).zfill(len(str(max_cnt)))


def get_target_file_name(index):
    name = get_name_from_id(index, MAXFILECNT)
    return os.sep + name + MP3FILEMARKER


def compile_list_of_playlists():
    """if Playlist folder exists, print playlists to be evaluated."""
    _list_of_playlists = os.listdir(PLAYLISTFLDRNAME)
    for _playlist in _list_of_playlists:
        if (_playlist.lower()).find(M3UFILETYPE) == -1:
            msg = "--- ERROR --- PlayListM3U folder contains unsupported file types:  %s\n\
    make sure you only place .m3u files here! Aborting." % _playlist
            quit_with_message(msg)
    _list_of_playlists.sort()
    print("Folder with playlists found. Trying to create DFplayer folders and files for: %s" % _list_of_playlists)
    return _list_of_playlists


def quit_with_message(message):
    """Quits script gracefully with message"""
    print(message)
    input("Press Enter to quit...\n")
    sys.exit()


def create_folder(path):
    """uses Operating System's function to create a directory. Politely exits if not successful."""
    try:
        os.makedirs(path)
    except:
        quit_with_message("Couldn't create folder %s. Is directory read-only?" % path)


def copy_mp3_to_target(pl_full_path, tgt_full_path):
    """Copies all files indicated by playlist file to target_full_path."""
    _playlist_file = open(pl_full_path, "r")
    file_index = 0
    for line in _playlist_file.readlines():
        line = find_m3u_filemarker(line.lower())
        if line is not None:
            file_index += 1
            target_file_name = get_target_file_name(file_index)
            # copies file from playlist to tgt folder
            try:
                shutil.copy2(line, os.sep.join([tgt_full_path, target_file_name]))
            except:
                quit_with_message(
                    "--- ERROR --- Couldn't copy file\n" + str(line) + " to:\n" + str(
                        target_full_path) + "\nAborting.")
    print("...completed for folder %d of %d: %s with %d files" % (
          folder_index, len(list_of_playlists), playlist, file_index))


def add_playlist_prefix(pl, pl_path, pl_prefix):
    """Renames a playlist file to indicate which target folder it links to"""
    if pl.find(pl_prefix, 0, 2) == -1:
        try:
            # rename playlists to match folder numbers
            new_name = [pl_prefix, "_", pl]
            os.rename(os.sep.join([pl_path, pl], os.sep.join([pl, new_name])))
        except:
            quit_with_message(" --- ERROR --- Couldn't rename playlist " + str(playlist) + ". Aborting.")
    return pl


print("Starting Conversion application for structuring files for DFplayerMini.\n\
This script analyzes .m3u playlists and restructures their contents to a format readable by the DFmini mp3 module.\n")

# Directory operations: Create required paths
current_path = os.getcwd()
playlist_path = os.path.join(os.sep, current_path, PLAYLISTFLDRNAME)
sd_card_path = os.path.join(os.sep, current_path, CARDFLDRNAME)

print("Hooked to current working directory: %s" % current_path)

# Handle SD card output folder
if os.path.exists(CARDFLDRNAME):
    print("SDcard MP3 folders found. Will modify contents based on playlist input.\n\
    Existing folders: %s\n" % str(os.listdir(CARDFLDRNAME)))
else:
    print("Did not find folder containing SD card MP3 folders.\n\
    Trying to create folder %s for you.\n\
    You will find the files to transfer to your DFplayerMini's SD card there" % CARDFLDRNAME)
    create_folder(CARDFLDRNAME)

# Handle playlist folder
list_of_playlists = None
if os.path.exists(PLAYLISTFLDRNAME):
    list_of_playlists = compile_list_of_playlists()
else:
    print("Did not find folder containing m3u playlists. Trying to create one for you...")
    create_folder(PLAYLISTFLDRNAME)
    quit_with_message("\
            SUCCESS: Created folder %s\n\
            Please move your playlists here and run the application again." % PLAYLISTFLDRNAME)

if not list_of_playlists:
    quit_with_message("--- ERROR --- No playlists found in %s.\n\
    Place .m3u file(s) here, please. Aborting." % PLAYLISTFLDRNAME)
# create folders with correct naming to contain mp3 files
folder_index = 0
# Go through all .m3u files in .m3u folder
for playlist in list_of_playlists:
    folder_index += 1
    # get folderIndexes right according to player's needs
    target_folder_name = get_name_from_id(folder_index, MAXFLDRCNT)
    target_full_path = os.sep.join([sd_card_path, target_folder_name])
    if os.path.exists(target_full_path):
        print("Target directory exists %s. Will auto-overwrite contents!" % target_folder_name)
    else:
        create_folder(target_full_path)
    # playlist open and show
    # try to find out if playlist has been renamed already, returns -1 if not
    playlist = add_playlist_prefix(playlist, playlist_path, target_folder_name)
    copy_mp3_to_target(os.sep.join([playlist_path, playlist]), target_full_path)
quit_with_message("--- SUCCESS --- All actions completed successfully.")
