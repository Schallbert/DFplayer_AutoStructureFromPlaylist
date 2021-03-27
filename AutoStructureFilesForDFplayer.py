import os
import sys
import os.path
import shutil


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
    line_of_playlist = line_of_playlist.replace("%20", " ")
    line_of_playlist = line_of_playlist.replace("%21", "!")
    line_of_playlist = line_of_playlist.replace("%22", '"')
    line_of_playlist = line_of_playlist.replace("%23", "#")
    line_of_playlist = line_of_playlist.replace("%24", "$")
    line_of_playlist = line_of_playlist.replace("%25", "%")
    line_of_playlist = line_of_playlist.replace("%26", "&")
    line_of_playlist = line_of_playlist.replace("%27", "'")
    line_of_playlist = line_of_playlist.replace("%28", "(")
    line_of_playlist = line_of_playlist.replace("%29", ")")
    line_of_playlist = line_of_playlist.replace("%2A", "*")
    line_of_playlist = line_of_playlist.replace("%2B", "+")
    line_of_playlist = line_of_playlist.replace("%2C", ",")
    line_of_playlist = line_of_playlist.replace("%2D", "-")
    line_of_playlist = line_of_playlist.replace("%2E", ".")
    line_of_playlist = line_of_playlist.replace("%2F", "/")
    line_of_playlist = line_of_playlist.replace("%3A", ":")
    line_of_playlist = line_of_playlist.replace("%3B", ";")
    line_of_playlist = line_of_playlist.replace("%3C", "<")
    line_of_playlist = line_of_playlist.replace("%3D", "=")
    line_of_playlist = line_of_playlist.replace("%3E", ">")
    line_of_playlist = line_of_playlist.replace("%3F", "?")
    line_of_playlist = line_of_playlist.replace("%7E", "~")
    line_of_playlist = line_of_playlist.replace("%C3%80", "À")
    line_of_playlist = line_of_playlist.replace("%C3%81", "Á")
    line_of_playlist = line_of_playlist.replace("%C3%82", "Â")
    line_of_playlist = line_of_playlist.replace("%C3%83", "Ã")
    line_of_playlist = line_of_playlist.replace("%C3%84", "Ä")
    line_of_playlist = line_of_playlist.replace("%C3%85", "Å")
    line_of_playlist = line_of_playlist.replace("%C3%86", "Æ")
    line_of_playlist = line_of_playlist.replace("%C3%87", "Ç")
    line_of_playlist = line_of_playlist.replace("%C3%88", "È")
    line_of_playlist = line_of_playlist.replace("%C3%89", "É")
    line_of_playlist = line_of_playlist.replace("%C3%8A", "Ê")
    line_of_playlist = line_of_playlist.replace("%C3%8B", "Ë")
    line_of_playlist = line_of_playlist.replace("%C3%8C", "Ì")
    line_of_playlist = line_of_playlist.replace("%C3%8D", "Í")
    line_of_playlist = line_of_playlist.replace("%C3%8E", "Î")
    line_of_playlist = line_of_playlist.replace("%C3%8F", "Ï")
    line_of_playlist = line_of_playlist.replace("%C3%90", "Ð")
    line_of_playlist = line_of_playlist.replace("%C3%91", "Ñ")
    line_of_playlist = line_of_playlist.replace("%C3%92", "Ò")
    line_of_playlist = line_of_playlist.replace("%C3%93", "Ó")
    line_of_playlist = line_of_playlist.replace("%C3%94", "Ô")
    line_of_playlist = line_of_playlist.replace("%C3%95", "Õ")
    line_of_playlist = line_of_playlist.replace("%C3%96", "Ö")
    line_of_playlist = line_of_playlist.replace("%C3%98", "Ø")
    line_of_playlist = line_of_playlist.replace("%C3%99", "Ù")
    line_of_playlist = line_of_playlist.replace("%C3%9A", "Ú")
    line_of_playlist = line_of_playlist.replace("%C3%9B", "Û")
    line_of_playlist = line_of_playlist.replace("%C3%9C", "Ü")
    line_of_playlist = line_of_playlist.replace("%C3%9D", "Ý")
    line_of_playlist = line_of_playlist.replace("%C3%9E", "Þ")
    line_of_playlist = line_of_playlist.replace("%C3%9F", "ß")
    line_of_playlist = line_of_playlist.replace("%C3%A0", "à")
    line_of_playlist = line_of_playlist.replace("%C3%A1", "á")
    line_of_playlist = line_of_playlist.replace("%C3%A2", "â")
    line_of_playlist = line_of_playlist.replace("%C3%A3", "ã")
    line_of_playlist = line_of_playlist.replace("%C3%A4", "ä")
    line_of_playlist = line_of_playlist.replace("%C3%A5", "å")
    line_of_playlist = line_of_playlist.replace("%C3%A6", "æ")
    line_of_playlist = line_of_playlist.replace("%C3%A7", "ç")
    line_of_playlist = line_of_playlist.replace("%C3%A8", "è")
    line_of_playlist = line_of_playlist.replace("%C3%A9", "é")
    line_of_playlist = line_of_playlist.replace("%C3%AA", "ê")
    line_of_playlist = line_of_playlist.replace("%C3%AB", "ë")
    line_of_playlist = line_of_playlist.replace("%C3%AC", "ì")
    line_of_playlist = line_of_playlist.replace("%C3%AD", "í")
    line_of_playlist = line_of_playlist.replace("%C3%AE", "î")
    line_of_playlist = line_of_playlist.replace("%C3%AF", "ï")
    line_of_playlist = line_of_playlist.replace("%C3%B0", "ð")
    line_of_playlist = line_of_playlist.replace("%C3%B1", "ñ")
    line_of_playlist = line_of_playlist.replace("%C3%B2", "ò")
    line_of_playlist = line_of_playlist.replace("%C3%B3", "ó")
    line_of_playlist = line_of_playlist.replace("%C3%B4", "ô")
    line_of_playlist = line_of_playlist.replace("%C3%B5", "õ")
    line_of_playlist = line_of_playlist.replace("%C3%B6", "ö")
    line_of_playlist = line_of_playlist.replace("%C3%B8", "ø")
    line_of_playlist = line_of_playlist.replace("%C3%B9", "ù")
    line_of_playlist = line_of_playlist.replace("%C3%BA", "ú")
    line_of_playlist = line_of_playlist.replace("%C3%BB", "û")
    line_of_playlist = line_of_playlist.replace("%C3%BC", "ü")
    line_of_playlist = line_of_playlist.replace("%C3%BD", "ý")
    line_of_playlist = line_of_playlist.replace("%C3%BE", "þ")
    line_of_playlist = line_of_playlist.replace("%C3%BF", "ÿ")
    return line_of_playlist


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
