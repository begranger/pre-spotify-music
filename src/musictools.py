import filetools as ft;
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


def getMetadata(song):

	# [title, artist, album]
	metadata = ['', '', ''];

	if type(song) is mutagen.flac.FLAC:

		if 'TITLE' in song.keys():
			metadata[TITLE] = song['TITLE'];
		if 'ARTIST' in song.keys():
			metadata[ARTIST] = song['ARTIST'];
		if 'ALBUM' in song.keys():
			metadata[ALBUM] = song['ALBUM'];
		
	elif type(song) is mutagen.mp3.MP3 or type(song) is mutagen.aiff.AIFF:
		# AIFFs seem to use the same tagging as MP3s

		if 'TIT2' in song.keys():
			metadata[TITLE] = song['TIT2'].text[0];
		if 'TPE1' in song.keys():
			metadata[ARTIST] = song['TPE1'].text[0];
		if 'TALB' in song.keys():
			metadata[ALBUM] = song['TALB'].text[0];
		
	elif type(song) is mutagen.mp4.MP4:

		if '©nam' in song.keys():
			metadata[TITLE] = song['©nam'][0];
		if '©ART' in song.keys():
			metadata[ARTIST] = song['©ART'][0];
		if '©alb' in song.keys():
			metadata[ALBUM] = song['©alb'][0];

	else:
		print('UNKNOWN TYPE ---- ' + str(type(song)));
		raise Exception;

	return metadata;


def dumpToExcel(flist, workbookName='songs.xlsx'):

	import xlsxwriter as xl;

	wb = xl.Workbook(workbookName);
	ws = wb.add_worksheet();

	ws.write(0, 0, 'PATH');
	ws.write(0, 1, 'TITLE');
	ws.write(0, 2, 'ARTIST');
	ws.write(0, 3, 'ALBUM');

	for row in range(0, len(flist.files)):

		# Remove root: '/Artist/Album/Song.ext'
		path_ArtistAlbumSong = flist.files[row].path.replace(flist.rootDir, '');

		song = mutagen.File(flist.files[row].path);
		
		# For 0-byte files (corrupted), mutagen songtype comes back as 'NoneType'
		if song is None:
			metadata = ['FILE ERROR: NoneType', '', ''];
		else:
			# [title, artist, album]
			metadata = getMetadata(song);

		# '/Artist/Album/Song.ext'
		ws.write(row+1, 0, path_ArtistAlbumSong);
		ws.write(row+1, 1, metadata[TITLE]);
		ws.write(row+1, 2, metadata[ARTIST]);
		ws.write(row+1, 3, metadata[ALBUM]);
		
	wb.close();


