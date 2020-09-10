import filetools as ft;
import mutagen;
import musictools as mt;

			




#srcRoot = '/home/ben/Music/Cleaned';
srcRoot = '/home/ben/Music/CleanedByExt/mp3/songs';
fl = ft.FileList(srcRoot);

#convertToFlac(fl, 'aiff');
#sortByExt(fl, srcRoot, '/home/ben/Music/CleanedByExt');
#fl.extensionHist();


song = mutagen.File('/home/ben/Music/CleanedByExt/mp3/songs/Jakubi/Can_t Afford It All (Kygo Remix) - Singl/Can_t Afford It All (Kygo Remix).mp3');
print(type(song.tags));

'''
for i in range(0, len(fl.files)):
#i=143;

	song = mutagen.File(fl.files[i].path);

	if 'APIC:' not in song.keys():

		print(fl.files[i].name);
'''

#mt.dumpToExcel(fl, workbookName='/home/ben/Music/CleanedByExt/mp3/mp3.xlsx')
#mt.loadFromExcel('/home/ben/Music/CleanedByExt/flac', '/home/ben/Music/CleanedByExt/flac/flac_processed.xlsx');


#fl.extensionHist();
#convertAiffToFlac(fl);
#fl.extensionHist();
#fl.findByExtension('flac');
