import filetools as ft;
import subprocess as sp;
import os;
import shutil as sh;
import mutagen;

TITLE 	= 0;
ARTIST 	= 1;
ALBUM 	= 2;


def cleanTitle(tIn):
	# Remove all troublesome characters from title string
	
	tmp = tIn;

	tmp = tmp.replace('(', '');
	tmp = tmp.replace(')', '');
	tmp = tmp.replace(' ', '');
	tmp = tmp.replace('/', '');
	#tmp = tmp.replace('\\', '');
	tmp = tmp.replace('\'', '');
	tmp = tmp.replace('\"', '');
	tmp = tmp.replace('.', '');
	tmp = tmp.replace('&', '');
	
	return tmp;


def convertToFlac(flist, srcExt):

	# convert all aiffs to flacs
	for song in flist.files:

		if song.ext == srcExt:

			cmd = ['flac', '--delete-input-file', '--no-padding', song.path];
			sp.run(cmd);


def sortByExt(flist, srcRoot, destRoot):

	for song in flist.files:

		# Remove srcRoot, song, and ext: '/Artist/Album'
		path_ArtistAlbum = song.path.replace(srcRoot, '').replace('/' + song.name, '');

		# append destRoot, extension and 'songs':
		# 'destRoot/ext/songs/Artist/Album'
		path_DestExtSongsArtistAlbum = destRoot + '/' + song.ext + '/songs' + path_ArtistAlbum;

		# Append song name and ext:
		# 'destRoot/ext/songs/Artist/Album/Song.ext'
		path_DestExtSongsArtistAlbumSong = path_DestExtSongsArtistAlbum + '/' + song.name;
		
		os.makedirs(path_DestExtSongsArtistAlbum, exist_ok=True);
		os.makedirs(destRoot + '/' + song.ext + '/pictures', exist_ok=True);
		sh.copyfile(song.path, path_DestExtSongsArtistAlbumSong);


def getMetadataFromPath(path_ArtistAlbumSong):

	# path_ArtistAlbumSong: '/Artist/Album/Song.ext'

	ext = path_ArtistAlbumSong.split('.')[-1];

	possibleArtist 	= path_ArtistAlbumSong[1:].split('/')[0];
	possibleAlbum  	= path_ArtistAlbumSong[1:].split('/')[1];

	possibleTitle  	= path_ArtistAlbumSong[1:].split('/')[2];
	possibleTitle  	= possibleTitle.replace('.' + ext, '');

	return [possibleTitle, possibleArtist, possibleAlbum];



def getPossibleMetadata(song, usePath=False, path_ArtistAlbumSong=''):

	# [title, artist, album]
	if usePath:
		possibleMetadata = getMetadataFromPath(path_ArtistAlbumSong);
	else:
		possibleMetadata = ['', '', ''];


	if type(song) is mutagen.flac.FLAC:

		if 'TITLE' in song.keys():

			possibleMetadata[TITLE] = song['TITLE'];

		if 'ARTIST' in song.keys():

			possibleMetadata[ARTIST] = song['ARTIST'];

		if 'ALBUM' in song.keys():

			possibleMetadata[ALBUM] = song['ALBUM'];

		hasPic = 'Not implemented for FLAC';
		
	elif type(song) is mutagen.mp3.MP3:

		if 'TIT2' in song.keys():

			possibleMetadata[TITLE] = song['TIT2'].text[0];

		if 'TPE1' in song.keys():

			possibleMetadata[ARTIST] = song['TPE1'].text[0];

		if 'TALB' in song.keys():

			possibleMetadata[ALBUM] = song['TALB'].text[0];

		hasPic = 'True' if 'APIC:' in song.keys() else 'False';
		
	elif type(song) is mutagen.mp4.MP4:

		if '©nam' in song.keys():

			possibleMetadata[TITLE] = song['©nam'][0];

		if '©ART' in song.keys():

			possibleMetadata[ARTIST] = song['©ART'][0];

		if '©alb' in song.keys():
			
			possibleMetadata[ALBUM] = song['©alb'][0];

		hasPic = 'Not implemented for M4A';

	else:
		raise Exception;

	return possibleMetadata, hasPic;


def dumpToExcel(flist, workbookName='songs.xlsx'):

	import xlsxwriter as xl;

	wb = xl.Workbook(workbookName);
	ws = wb.add_worksheet();

	ws.write(0, 0, 'PATH');
	ws.write(0, 1, 'TITLE');
	ws.write(0, 2, 'ARTIST');
	ws.write(0, 3, 'ALBUM');
	ws.write(0, 4, 'HAS-PIC');
	ws.write(0, 5, 'PICTURE');

	for row in range(0, len(flist.files)):
	#for row in range(0, 1):

		# Remove root: '/Artist/Album/Song.ext'
		path_ArtistAlbumSong = flist.files[row].path.replace(flist.rootDir, '');

		song = mutagen.File(flist.files[row].path);
		
		# [title, artist, album]
		#possibleMetadata, hasPic = getPossibleMetadata(song, path_ArtistAlbumSong);
		possibleMetadata, hasPic = getPossibleMetadata(song);

		# '/Artist/Album/Song.ext'
		ws.write(row+1, 0, path_ArtistAlbumSong);
		ws.write(row+1, 1, possibleMetadata[TITLE]);
		ws.write(row+1, 2, possibleMetadata[ARTIST]);
		ws.write(row+1, 3, possibleMetadata[ALBUM]);
		ws.write(row+1, 4, hasPic);
		

	wb.close();


def getFlacPicture(pathToPicture):

	p = mutagen.flac.Picture();

	with open(pathToPicture, 'rb') as f:
		p.data = f.read()

	p.type 		= mutagen.id3.PictureType.COVER_FRONT;
	p.mime 		= 'image/jpeg';
	p.width 	= 500;
	p.height 	= 500;
	p.depth 	= 16;

	return p;


def getPicture(ext, pathToPicture):

	if ext == 'flac':
		return getFlacPicture(pathToPicture);
	#else if ext == 'mp3':


def loadFromExcel(srcRoot, workbookName):

	colPATH 	= 0;
	colTITLE 	= 1;
	colARTIST 	= 2;
	colALBUM 	= 3;
	colPICTURE 	= 4;

	# srcRoot: everything up to (but not including): /songs/Artist/Album/Song.ext
	# e.g. /home/ben/Music/CleanedByExt/flac

	os.makedirs(srcRoot + '/processed_songs', exist_ok=True);

	import xlrd;
	import filetools as ft;

	wb = xlrd.open_workbook(workbookName);
	ws = wb.sheet_by_index(0);

	# skip header row
	for row in range(1, ws.nrows):

		# move song first
		oldPathToSong 	= srcRoot + '/songs' + ws.cell_value(row, colPATH);
		ext 		= ft.File.GetExtension(oldPathToSong);
		
		newPathToSong 	= srcRoot + '/processed_songs/' + cleanTitle(ws.cell_value(row, colTITLE)) + '.' + ext;
		sh.copyfile(oldPathToSong, newPathToSong);

		# add metadata to new copy of song
		song 	= mutagen.File(newPathToSong);

		title 	= ws.cell_value(row, colTITLE);
		artist 	= ws.cell_value(row, colARTIST);
		album 	= ws.cell_value(row, colALBUM);

		# filename only
		picture = ws.cell_value(row, colPICTURE);

		# remove all tags and picture
		song.clear();
		song.clear_pictures();

		# must have at least these two
		song['TITLE'] 	= title;
		song['ARTIST'] 	= artist;

		# if there is an album
		if album != '':

			song['ALBUM'] = album;
			print(album);

			# if there is a picture
			if picture != '':

				pathToPicture 	= srcRoot + '/pictures/' + picture;
				pic 		= getPicture(ext, pathToPicture);

				song.add_picture(pic);

		song.save();
			
			




