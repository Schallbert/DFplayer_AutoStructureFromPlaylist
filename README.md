# DFplayer_AutoStructureFromPlaylist
Script that takes an .m3u playlist and converts copies its files to a folder, renaming files and folder to the format readable by DFplayer Mini.

# Background
Script: 
The script is written in PYTHON.
NOTE: I have a compiled version at hand for Win10 x64. So if you wouldn't like to install python, let me know and I'll share the .exe
DFplayer Mini: 
DFplayer Mini mp3 player module needs a certain file and folder format on its SD-Card in order to be able to correctly index and read files.
Format is Foldername 01, 02 ... 99
and Filename 001, 002, ... 255
So maximum folder count is 99 and max number of files within a folder is 255.
M3U playlist:
An M3U playlist contains the absolute path of where the MP3 file can be found, its track number within the list and additional information on the track.

# Problem/Motivation
Normally, MP3-Files have a "ArtistTitle" naming convention, e.g. Artist - Title.mp3 which have to be modified by hand to 001, 002 etc. to match DFplayer's expectations. Maintaining track sequence may become unnerving especially if you have multiple playlists/folders to be played or make mistakes in between.
To mitigate manual renaming, this script has been developed.

# How to use the script
1. Place the script in the folder you'd like the script's output to appear in, e.g. "Music/DFplayerFiles"
2. Run the script once. It will create the input folder "PlayListsM3U" and end with an error message that it didn't find any files to modify.
3. Create playlists with the songs you'd like to listen to on DFplayer mini and place them in "PlayListsM3U". It makes sense to name them with the corresponding folder name, e.g. "01 - Audiobook Story Of My life"
4. Re-run the script.
5. Find the output folder structure in "SDcardFolders" ;)

# Rough description of what it does
The script will create two folders (in the folder it is placed itself):
"PlayListsM3U" which you put your playlists in to be converted (input for script)
"SDcardFolders" which contains the script's output (numbered folders accoring to the playlist count and copied plus renamed MP3 files)
The script iterates through all playlist files within PlayListsM3U and will create folders accordingly, copying the playlist's linked files into this folder, and renaming it according to the playlist's track number following DFplayer's file/folder format.
