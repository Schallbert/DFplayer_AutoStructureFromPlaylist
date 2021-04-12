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


def playerFSnumbers(indx, maxCnt):
    """Returns a DFplayerMini-compatible way of numbering
    files which is 001, 002, ... 255"""
    if indx > maxCnt:
        quitWithMessage("Error: player cannot process more than 100 folders")
    return str(indx).zfill(len(str(maxCnt)))


def replace_special_chars_in_path(line_of_playlist):
    """Make sure .m3u file's special characters are converted
    Replace most common UTF8 special characters"""
    return unquote(line_of_playlist)


def quitWithMessage(messageString):
    """Quits script gracefully with message"""
    print(messageString)
    input("Press Enter to quit...")
    sys.exit()


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


def get_target_file_name(index):
    name = playerFSnumbers(index, MAXFILECNT)
    return os.sep + name + MP3FILEMARKER


print("\
Starting Conversion script for structuring files for DFplayerMini.\n\
This script analyzes .m3u playlists and restructures their contents to a format\n\
readable by the DFmini mp3 module.\n")

# get current working directory
myPath = os.getcwd()
# create directories for playlists and target folders
plPath = os.path.join(os.sep, myPath, PLAYLISTFLDRNAME)
crdPath = os.path.join(os.sep, myPath, CARDFLDRNAME)
listOfPlaylists = None

print("Hooked to current working directory: %s" % myPath)

# Check for playlist path
if not os.path.exists(PLAYLISTFLDRNAME):
    print("\
Did not find folder containing m3u playlists.\n\
Trying to create folder 'PlayListsM3U' for you.")
    try:
        os.makedirs(PLAYLISTFLDRNAME)
    except:
        quitWithMessage("Couldn't create folder. Is directory read-only?")
        quitWithMessage("\
Playlist folder successfully created: %s\n\
Please move your playlists to this place before restarting the script." % PLAYLISTFLDRNAME)
else:
    # if Playlist folder exists, print playlists to be evaluated.
    listOfPlaylists = os.listdir(PLAYLISTFLDRNAME)
    for line in listOfPlaylists:
        if (line.lower()).find(M3UFILETYPE) == -1:
            msg = "--- ERROR --- PlayListM3U folder contains other file types than .m3u Playlists: %s\n\
make sure you only place .m3u files here! Aborting." % line
            quitWithMessage(msg)
    listOfPlaylists.sort()
    print("Folder containing playlists found. Will try creating DFplayer folders and files for:")
    print(listOfPlaylists)

# Check for album(folder) path
if os.path.exists(CARDFLDRNAME):
    # if Playlist folder exists, print playlists to be evaluated.
    listOfCardFolders = os.listdir(CARDFLDRNAME)
    print("Folder containing SDcard MP3 folders found. Will modify folder structure based on playlist input.")
    print("Existing folders: " + str(listOfCardFolders))
else:
    print("\
    Did not find folder containing SD card MP3 folders.\n\
    Trying to create folder 'SDcardFolders' for you.\n \
    You will find the files to transfer to your DFplayerMini's SD card in this folder.")
    try:
        os.makedirs(CARDFLDRNAME)
    except:
        quitWithMessage("--- ERROR --- Couldn't create folder. Is directory read-only?")

if not listOfPlaylists:
    quitWithMessage("--- ERROR --- No playlists found in folder. Place .m3u file(s) here, please. Aborting.")
# create folders with correct naming to contain mp3 files
folderIndex = 0
target_folder_name = ""
line_lower = ''
# Go through all .m3u files in .m3u folder
for playlist in listOfPlaylists:
    folderIndex += 1
    # get folderIndexes right according to player's needs
    target_folder_name = playerFSnumbers(folderIndex, MAXFLDRCNT)
    target_folder_path = os.sep.join([crdPath, target_folder_name])
    if os.path.exists(target_folder_name):
        print("Folder '%s' already exists. Will auto-overwrite contents." % target_folder_name)
    else:
        try:
            os.makedirs(target_folder_path)
        except:
            quitWithMessage("--- ERROR --- Couldn't create folder. Is directory read-only?")
    # playlist open and show
    # try to find out if playlist has been renamed already, returns -1 if not
    if playlist.find(target_folder_name, 0, 2) == -1:
        try:
            # rename playlists to match folder numbers
            new_name = [target_folder_name, "_", playlist]
            os.rename(os.sep.join([plPath, playlist], os.sep.join([plPath, new_name])))
            playlist = new_name
        except:
            quitWithMessage(" --- ERROR --- Couldn't rename playlist " + str(playlist) + ". Aborting.")
    playlistFile = open(os.sep.join([plPath, playlist]), "r")
    file_index = 0
    for line in playlistFile.readlines():
        line = find_m3u_filemarker(line.lower())
        if line is not None:
            file_index += 1
            target_file_name = get_target_file_name(file_index)
            # copies file from playlist to tgt folder
            try:
                shutil.copy2(line, os.sep.join([target_folder_path, target_file_name]))
            except:
                quitWithMessage(
                    "--- ERROR --- Couldn't copy file\n" + str(line) + " to:\n" + str(
                        target_folder_path) + "\nAborting.")
    print(
        "...completed for folder %d of %d: %s with %d files" % (
            folderIndex, len(listOfPlaylists), playlist, file_index))
quitWithMessage("--- SUCCESS --- All actions completed successfully.")
