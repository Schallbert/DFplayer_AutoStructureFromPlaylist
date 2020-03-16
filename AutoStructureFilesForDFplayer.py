import os
from sys import exit
import os.path
import shutil

#Author: L. Preusser "Schallbert"

# this function pads leading zeros to a number, returning a string.
def playerFSnumbers(indx, maxCnt):
    """This function returns a DFplayerMini-compatible way of numbering
    files which is 001, 002, ... 255"""
    if indx > maxCnt:
        quitWithMessage("Error: player cannot process more than 100 folders")
    return str(indx).zfill(len(str(maxCnt)))

def replaceSpecialCharactersInPlaylist(lineOfPlaylist):
    """Make sure .m3u file's special characters are converted
    Replace most commont HTML exclamations"""
    lineOfPlaylist = lineOfPlaylist.replace("%20", " ")
    lineOfPlaylist = lineOfPlaylist.replace("%21", "!")
    lineOfPlaylist = lineOfPlaylist.replace("%22", '"')
    lineOfPlaylist = lineOfPlaylist.replace("%23", "#")
    lineOfPlaylist = lineOfPlaylist.replace("%24", "$")
    lineOfPlaylist = lineOfPlaylist.replace("%25", "%")
    lineOfPlaylist = lineOfPlaylist.replace("%26", "&")
    lineOfPlaylist = lineOfPlaylist.replace("%27", "'")
    lineOfPlaylist = lineOfPlaylist.replace("%28", "(")
    lineOfPlaylist = lineOfPlaylist.replace("%29", ")")
    lineOfPlaylist = lineOfPlaylist.replace("%2A", "*")
    lineOfPlaylist = lineOfPlaylist.replace("%2B", "+")
    lineOfPlaylist = lineOfPlaylist.replace("%2C", ",")
    lineOfPlaylist = lineOfPlaylist.replace("%2D", "-")
    lineOfPlaylist = lineOfPlaylist.replace("%2E", ".")
    lineOfPlaylist = lineOfPlaylist.replace("%2F", "/")
    lineOfPlaylist = lineOfPlaylist.replace("%3A", ":")
    lineOfPlaylist = lineOfPlaylist.replace("%3B", ";")
    lineOfPlaylist = lineOfPlaylist.replace("%3C", "<")
    lineOfPlaylist = lineOfPlaylist.replace("%3D", "=")
    lineOfPlaylist = lineOfPlaylist.replace("%3E", ">")
    lineOfPlaylist = lineOfPlaylist.replace("%3F", "?")
    return lineOfPlaylist

def quitWithMessage(messageString):
    """Quits script gracefully with message"""
    print(messageString)
    input("Press Enter to quit...")
    sys.exit()

print("\
Starting Conversion script for structuring files for DFplayerMini.\n\
This script analyzes .m3u playlists and restructures their contents to a format\n\
readable by the DFmini mp3 module.\n\n")

# folder names
plFldrName = "PlayListsM3U"
crdFldrName = "SDcardFolders"
# player's maximum accepted file cnt
maxFldrCnt = 99
maxFileCnt = 255
listOfPlaylists = None

# get current working directory
myPath = os.getcwd()
# create directories for playlists and target folders
plPath = os.path.join(os.sep, myPath, plFldrName)
crdPath = os.path.join(os.sep, myPath, crdFldrName)
tgtFldrPath = -1
tgtFileName = -1

print("Hooked to current working directory: %s" % myPath)

# Check for playlist path
if not os.path.exists(plFldrName):
    print("\
Did not find folder containing m3u playlists.\n\
Trying to create folder 'PlayListsM3U' for you.")
    try:
        os.makedirs(plFldrName)
    except:
        quitWithMessage("Couldn't create folder. Is directory read-only?")
    quitWithMessage("\
Playlist folder successfully created: %s\n\
Please move your playlists to this place before restarting the script." % plFldrName)
else:
    # if Playlist folder exists, print playlists to be evaluated.
    listOfPlaylists = os.listdir(plFldrName)
    listOfPlaylists.sort()
    print("Folder containing playlists found. Will try creating DFplayer folders and files for:")
    print(listOfPlaylists)
# input("Press Enter to continue...")

# Check for album(folder) path
if not os.path.exists(crdFldrName):
    print("\
Did not find folder containing SD card MP3 folders.\n\
Trying to create folder 'SDcardFolders' for you.\n \
You will find the files to transfer to your DFplayerMini's SD card in this folder.")
    try:
        os.makedirs(crdFldrName)
    except:
        quitWithMessage("Couldn't create folder. Is directory read-only?")
else:
    # if Playlist folder exists, print playlists to be evaluated.
    listOfCardFolders = os.listdir(crdFldrName)
    print("Folder containing SDcard MP3 folders found. Will modify folder structure based on playlist input.")
    print("Existing folders: " + str(listOfCardFolders))

# create folders with correct naming to contain mp3 files
folderIndex = 0
fName = ""
lineLower = ''
if listOfPlaylists:
    print("Playlists found: " + str(listOfPlaylists))
    # Go through all .m3u files in .m3u folder
    for item in listOfPlaylists:
        os.chdir(crdPath)
        folderIndex += 1
        # get folderIndexes right according to player's needs
        fName = playerFSnumbers(folderIndex, maxFldrCnt)
        if not os.path.exists(fName):
            try:
                os.makedirs(fName)
            except:
                quitWithMessage("Couldn't create folder. Is directory read-only?")
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
                quitWithMessage("Couldn't rename playlist " + str(item) + ". Aborting.")
        playlistFile = open(item, "r")
        fileIndex = 0
        for line in playlistFile.readlines():
            lineLower = line.lower()  # convert to lower case to also find .MP3
            if lineLower.find(".mp3") > -1:  # only list lines that describe MP3 file path
                fileIndex += 1
                fName = playerFSnumbers(fileIndex, maxFileCnt)
                tgtFileName = os.sep + fName + ".mp3"
                line = line.strip()  # strip removes New Line markers \n
                if line.find("file:///") > - 1:  # strip line of file marker within m3u
                    line = line.split("file:///")[-1]
                    line = replaceSpecialCharactersInPlaylist(line)
                tgtFileName = fName + ".mp3"  # new target file name
                try:
                    shutil.copy2(line, os.path.join(os.sep, tgtFldrPath,
                                                    tgtFileName))  # copies & renames file from playlist to tgt folder
                except:
                    quitWithMessage("Couldn't copy file\n" + str(line) + " to:\n" + str(tgtFldrPath) + "\nAborting.")
        quitWithMessage("Successfully copied %s files!" % fileIndex)
else:
    quitWithMessage("No playlists found in folder. Aborting.")