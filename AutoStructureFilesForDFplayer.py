import os, os.path
import shutil

#this function pads leading zeros to a number, returning a string.
def playerFSnumbers(folderIndex, maxCnt):
	if folderIndex > maxCnt:
		print("Error: player cannot process more than 100 folders")
		input("Press Enter to quit...")
		quit()
	return str(folderIndex).zfill(len(str(maxCnt)))

#folder names
plFldrName = "PlayListsM3U"
crdFldrName = "SDcardFolders"
#player's maximum accepted file cnt
maxFldrCnt = 99
maxFileCnt = 255

#get current working directory
myPath = os.getcwd()
#create directories for playlists and target folders
plPath = os.path.join(os.sep, myPath, plFldrName)
crdPath = os.path.join(os.sep, myPath, crdFldrName)
tgtFldrPath = -1
tgtFileName = -1

#Check for playlist path
if not os.path.exists(plFldrName):
	print("Did not find folder containing m3u playlists.\nTrying to create folder 'PlayListsM3U' for you.\nPlease move your playlists to this place before restarting the script.")
	try:
		os.makedirs(plFldrName)
	except:
		print("Couldn't create folder. Is directory read-only?")
		input("Press Enter to quit...")
		quit()
else:
	#if Playlist folder exists, print playlists to be evaluated.
	listOfPlaylists = os.listdir(plFldrName)
	listOfPlaylists.sort()
	print("Folder containing playlists found. Will try creating DFplayer folders and files for:")
	print(listOfPlaylists)
	#input("Press Enter to continue...")
	
#Check for album(folder) path
if not os.path.exists(crdFldrName):
	print("Did not find folder containing SD card MP3 folders.\nTrying to create folder 'SDcardFolders' for you.\n You will find the files to transfer to Tonuino in this folder.")
	try:
		os.makedirs(crdFldrName)
	except:
		print("Couldn't create folder. Is directory read-only?")
		input("Press Enter to quit...")
		quit()
else:
	#if Playlist folder exists, print playlists to be evaluated.
	listOfCardFolders = os.listdir(crdFldrName)
	print("Folder containing SDcard MP3 folders found. Will modify folder structure based on playlist input.")
	print(listOfCardFolders)

#create folders with correct naming to contain mp3 files
folderIndex = 0
fName = ""
lineLower = ''
print(listOfPlaylists)
#Go through all .m3u files in .m3u folder
for item in listOfPlaylists:
	os.chdir(crdPath)
	folderIndex += 1
	#get folderIndexes right according to player's needs
	fName = playerFSnumbers(folderIndex, maxFldrCnt)
	if not os.path.exists(fName):
		try:
			os.makedirs(fName)
		except:
			print("Couldn't create folder. Is directory read-only?")
			input("Press Enter to quit...")
			quit()
	else:
		#folder already exists. Auto-Overwrite.
		print("Folder '%s' exists. Will auto-overwrite contents." % (fName,))
	#go through all playlists in folder
	tgtFldrPath = os.path.join(os.sep, crdPath, fName)
	os.chdir(plPath)
	#playlist open and show 
	if item.find(str(fName), 0, 4) == -1: #tries to find out if playlist has  been used already, returns -1 if no duplicates
		try:
			os.rename(str(item), fName + " " + str(item))
			item = fName + " " + str(item)
		except:
			print("Couldn't rename playlist " + str(item) + ". Aborting.")
			input("Press Enter to quit...")
			quit()
	playlistFile = open(item, "r")
	fileIndex = 0
	for line in playlistFile.readlines():
		lineLower = line.lower() #convert to lower case to also find .MP3
		if lineLower.find(".mp3") > -1: #only list lines that describe MP3 file path
			fileIndex +=1
			fName = playerFSnumbers(fileIndex, maxFileCnt)
			tgtFileName = os.sep + fName + ".mp3"
			line = line.strip() #strip removes New Line markers \n
			if line.find("file:///") > - 1: #strip line of file marker within m3u
				line = line.split("file:///")[-1]
            #Also replace most commont HTML exclamations
            line = line.replace("%20", " ")
            line = line.replace("%21", "!")
            line = line.replace("%22", '"')
            line = line.replace("%23", "#")
            line = line.replace("%24", "$")
            line = line.replace("%25", "%")
            line = line.replace("%26", "&")
            line = line.replace("%27", "'")
            line = line.replace("%28", "(")
            line = line.replace("%29", ")")
            line = line.replace("%2A", "*")
            line = line.replace("%2B", "+")
            line = line.replace("%2C", ",")
            line = line.replace("%2D", "-")
            line = line.replace("%2E", ".")
            line = line.replace("%2F", "/")
            line = line.replace("%3A", ":")
            line = line.replace("%3B", ";")
            line = line.replace("%3C", "<")
            line = line.replace("%3D", "=")
            line = line.replace("%3E", ">")
            line = line.replace("%3F", "?")
	
			tgtFileName = fName + ".mp3" #new target file name
			try:
				shutil.copy2(line, os.path.join(os.sep, tgtFldrPath,  tgtFileName)) #copies & renames file from playlist to target folder
			except:
			        print("Couldn't copy file\n" + str(line) + " to:\n" + str(tgtFldrPath) + "\nAborting.")
				quit()
	print("Successfully copied %s files!" % (fileIndex,))
	input("\n\nPress Return to quit")
