import os
import sys
import os.path
import shutil
# use urllib to escape special (UTF8) characters in filenames
from urllib.parse import quote

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
    return quote(line_of_playlist)


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

listOfPlaylists = None

# get current working directory
myPath = os.getcwd()
# create directories for playlists and target folders
plPath = os.path.join(os.sep, myPath, PLAYLISTFLDRNAME)
crdPath = os.path.join(os.sep, myPath, CARDFLDRNAME)
tgtFldrPath = -1
tgtFileName = -1

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
if not os.path.exists(CARDFLDRNAME):
    print("\
Did not find folder containing SD card MP3 folders.\n\
Trying to create folder 'SDcardFolders' for you.\n \
You will find the files to transfer to your DFplayerMini's SD card in this folder.")
    try:
        os.makedirs(CARDFLDRNAME)
    except:
        quitWithMessage("--- ERROR --- Couldn't create folder. Is directory read-only?")
else:
    # if Playlist folder exists, print playlists to be evaluated.
    listOfCardFolders = os.listdir(CARDFLDRNAME)
    print("Folder containing SDcard MP3 folders found. Will modify folder structure based on playlist input.")
    print("Existing folders: " + str(listOfCardFolders))

# create folders with correct naming to contain mp3 files
folderIndex = 0
tgt_folder_name = ""
line_lower = ''
if listOfPlaylists:
    # Go through all .m3u files in .m3u folder
    for item in listOfPlaylists:
        os.chdir(crdPath)
        folderIndex += 1
        # get folderIndexes right according to player's needs
        tgt_folder_name = playerFSnumbers(folderIndex, MAXFLDRCNT)
        if not os.path.exists(tgt_folder_name):
            try:
                os.makedirs(tgt_folder_name)
            except:
                quitWithMessage("--- ERROR --- Couldn't create folder. Is directory read-only?")
        else:
            # folder already exists. Auto-Overwrite.
            print("Folder '%s' exists. Will auto-overwrite contents." % tgt_folder_name)
        # go through all playlists in folder
        tgtFldrPath = os.path.join(os.sep, crdPath, tgt_folder_name)
        os.chdir(plPath)
        # playlist open and show
        if item.find(str(tgt_folder_name), 0,
                     4) == -1:  # tries to find out if playlist has  been used already, returns -1 if no duplicates
            try:
                os.rename(str(item), tgt_folder_name + " " + str(item))
                item = tgt_folder_name + " " + str(item)
            except:
                quitWithMessage(" --- ERROR --- Couldn't rename playlist " + str(item) + ". Aborting.")
        playlistFile = open(item, "r")
        file_index = 0
        for line in playlistFile.readlines():
            line = find_m3u_filemarker(line.lower())
            if line is not None:
                file_index += 1
                tgt_file_name = get_target_file_name(file_index)
                # copies & renames file from playlist to tgt folder
                #try:
                shutil.copy2(line, os.path.join(os.sep, tgtFldrPath, tgt_file_name))
                #except:
                #    quitWithMessage(
                #        "--- ERROR --- Couldn't copy file\n" + str(line) + " to:\n" + str(
                 #           tgtFldrPath) + "\nAborting.")
        print(
            "...completed for folder %d of %d: %s with %d files" % (
                folderIndex, len(listOfPlaylists), item, file_index))
    quitWithMessage("--- SUCCESS --- All actions completed successfully.")
else:
    quitWithMessage("--- ERROR --- No playlists found in folder. Place .m3u file(s) here, please. Aborting.")
