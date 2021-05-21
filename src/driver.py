import subprocess as sp;
import filetools as ft;
import musictools as mt;

# Unpack the archive
##sp.run('./extract_drive_dumps.sh')

srcRoot = '/home/ben/Music/CleanedBackup';
fl = ft.FileList(srcRoot);

mt.dumpToExcel(fl, '/home/ben/Music/song.xlsx');



