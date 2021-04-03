import os
import sys
import os.path
import shutil
# urllib should do what you need in replaceSpecialCharactersInPlaylist
from urllib.parse import quote_plus


# Author: "Schallbert"

# this function pads leading zeros to a number, returning a string.
def playerFSnumbers(indx, maxCnt):
    """This function returns a DFplayerMini-compatible way of numbering
    files which is 001, 002, ... 255"""
    if indx > maxCnt:
        quitWithMessage("Error: player cannot process more than 100 folders")
    return str(indx).zfill(len(str(maxCnt)))


def replaceSpecialCharactersInPlaylist(line_of_playlist):
    """Make sure .m3u file's special characters are converted
    Replace most commont UTF8 special characters"""
    return quote_plus(line_of_playlist)


def quitWithMessage(messageString):
    """Quits script gracefully with message"""
    print(messageString)
    input("Press Enter to quit...")
    sys.exit()


print("\
Starting Conversion script for structuring files for DFplayerMini.\n\
This script analyzes .m3u playlists and restructures their contents to a format\n\
readable by the DFmini mp3 module.\n")

# folder names
PLAYLISTFLDRNAME = "PlayListsM3U"
CARDFLDRNAME = "SDcardFolders"
# player's maximum accepted file cnt
MAXFLDRCNT = 99
MAXFILECNT = 255
M3UFILETYPE = ".m3u"
M3UFILEMARKER = "file:///"
MP3FILEMARKER = ".mp3"
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
        if (line.lower()).find(M3UFILETYPE) > -1:
            listOfPlaylists.sort()
            print("Folder containing playlists found. Will try creating DFplayer folders and files for:")
            print(listOfPlaylists)
        else:
            msg = "--- ERROR --- PlayListM3U folder contains other file types than .m3u Playlists: %s\n\
make sure you only place .m3u files here! Aborting." % line
            quitWithMessage(msg)

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
fName = ""
lineLower = ''
if listOfPlaylists:
    # Go through all .m3u files in .m3u folder
    for item in listOfPlaylists:
        os.chdir(crdPath)
        folderIndex += 1
        # get folderIndexes right according to player's needs
        fName = playerFSnumbers(folderIndex, MAXFLDRCNT)
        if not os.path.exists(fName):
            try:
                os.makedirs(fName)
            except:
                quitWithMessage("--- ERROR --- Couldn't create folder. Is directory read-only?")
        else:
            # folder already exists. Auto-Overwrite.
            print("Folder '%s' exists. Will auto-overwrite contents." % fName)
        # go through all playlists in folder
        tgtFldrPath = os.path.join(os.sep, crdPath, fName)
        os.chdir(plPath)
        # playlist open and show
        if item.find(str(fName), 0,
                     4) == -1:  # tries to find out if playlist has  been used already, returns -1 if no duplicates
            try:
                os.rename(str(item), fName + " " + str(item))
                item = fName + " " + str(item)
            except:
                quitWithMessage(" --- ERROR --- Couldn't rename playlist " + str(item) + ". Aborting.")
        playlistFile = open(item, "r")
        fileIndex = 0
        for line in playlistFile.readlines():
            lineLower = line.lower()  # convert to lower case to also find .MP3
            if lineLower.find(M3UFILEMARKER) > -1:  # only list lines that describe MP3 file path
                fileIndex += 1
                fName = playerFSnumbers(fileIndex, MAXFILECNT)
                tgtFileName = os.sep + fName + MP3FILEMARKER
                line = line.strip()  # strip removes New Line markers \n
                line = line.split(M3UFILEMARKER)[-1]
                line = replaceSpecialCharactersInPlaylist(line)
                tgtFileName = fName + MP3FILEMARKER  # new target file name
                try:
                    shutil.copy2(line, os.path.join(os.sep, tgtFldrPath,
                                                    tgtFileName))  # copies & renames file from playlist to tgt folder
                except:
                    quitWithMessage(
                        "--- ERROR --- Couldn't copy file\n" + str(line) + " to:\n" + str(tgtFldrPath) + "\nAborting.")
        print(
            "...completed for folder %d of %d: %s with %d files" % (folderIndex, len(listOfPlaylists), item, fileIndex))
    quitWithMessage("--- SUCCESS --- All actions completed successfully.")
else:
    quitWithMessage("--- ERROR --- No playlists found in folder. Place .m3u file(s) here, please. Aborting.")
