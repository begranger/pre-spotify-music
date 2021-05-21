import subprocess as sp;
import filetools as ft;
import musictools as mt;

# Unpack the archive
run_unpack = input('Unpack archive? (y/n): ');
if run_unpack == 'y':
	print('Unpacking archive ... ', end='');
	sp.run('./extract_drive_dumps.sh');
	print('Done');

# Continue to excel generation?
run_excel_gen = input('Generate songs.xlsx? (y/n): ');
if run_excel_gen == 'n':
	quit();

# Generate FileList of all songs
srcRoot = '/home/ben/Music/CleanedBackup';
fl = ft.FileList(srcRoot);
print('Num songs = ' + str(len(fl.files)));

# Check for empty FileList
if len(fl.files) == 0:
	print('Error: no songs found, exiting');
	quit();

# Extract metadata and dump to excel
print('Extracting metadata and dumping to excel ... ', end='');
mt.dumpToExcel(fl, '/home/ben/Music/songs.xlsx');
print('Done');



