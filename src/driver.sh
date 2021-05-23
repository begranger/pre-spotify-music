#!/bin/bash


print_num_types () {
	# print_num_types(dir)
	num_m4as="$(find $1 -name *.m4a -type f | wc -l)"
	num_mp3s="$(find $1 -name *.mp3 -type f | wc -l)"
	num_aiffs="$(find $1 -name *.aiff -type f | wc -l)"
	num_files="$(find $1 -type f | wc -l)"

	# Lets us see if set of extensions covers all files
	num_songs=$(echo $num_m4as+$num_mp3s+$num_aiffs | bc)

	echo "#m4as  = $num_m4as"
	echo "#mp3s  = $num_mp3s"
	echo "#aiffs = $num_aiffs"
	echo "#files = $num_files, sum(exts) = $num_songs"
}

dump_bitrates () {
	# dump_bitrates(dir, ext)
	# print0 in find -> -0 in xargs, deals w spaces/newlines in paths
	# Had to include 2>&1 bc ffprobe was throwing soft error so printing to stderr
	# The regexp replaces everything *except* the bitrate value w '' then prints that
	# Had to put redirect outside quotes to redirect all output of xargs not just one exec of sed
	find $1 -name "*.$2" -type f -print0 | xargs -0 -I{} sh -c "ffprobe '{}' 2>&1 | sed -n -e s/'^.*bitrate: '//p | sed -n -e s/' kb\/s'//p" > "bitrates_$2.txt"
}

avg_bitrate () {
	# avg_bitrate(ext)
	# Assumes filename is "bitrates_<ext>.txt"
	bitrates=( $(cat "bitrates_$1.txt") );
	count=0;
	for i in ${bitrates[@]}
	do
		count=$(echo $count+$i | bc);
	done
	avg=$(echo $count / ${#bitrates[@]} | bc);
	echo "Avg $1 bitrate = $avg"
}


get_yn () {
	# get_yn(prompt)
	# NB: prompt has to be quoted to allow spaces
	read -p "$1" answer
	echo $answer

	# eg usage
	# NB: there *must* be a space in bw '[' and '$'
	# if [ $(get_yn 'Unpack archive? (y/n): ') = 'y' ]
	# then 
	#	do something
	# fi
}


src_dir="./CleanedBackup_working/"
dest_dir="./ProcessedSongs/"


# Flow
# 1. Unpack
# 2. Detox
# 3. Flatten
# 4. Find+Remove zero-byte files
# 5. Convert each type to mp3 w corresponding bitrates (a priori), delete original file
# 6. Verify num-songs-in = num-songs-out, now just only mp3s
#
# Before (5), need to (once)
# a. Dump bitrates
# b. Average bitrates - determine settings for conversion of each type
#

## 1. Unpack
#unzip ~/Downloads/cleaned_zips/Cleaned\ Backup\ \(old\ and\ duplicates\ deleted\)-20200102T054547Z-00\*.zip -d ~/Music/
#mv ~/Music/Cleaned\ Backup\ \(old\ and\ duplicates\ deleted\) ~/Music/CleanedBackup

print_num_types $src_dir;
echo ''

## 2. Detox the filenames (and dirs?)
# NB: 'detox' seems to handle dir names too- ran quick test w 'a nasty dir'/'a nasty file .aiff'
detox -r $src_dir
print_num_types $src_dir;
echo ''

## 3. Flatten files
# Pick out the filename- cant seem to reference dest_dir in xargs cli string below
# so doing it this way- only possible after file detox
# Have to mkdir first- otherwise mv complains-
# Included -p on mkdir to make it safe/quiet if dir already exists
mkdir -p $dest_dir;
full_paths=( $(find $src_dir -type f) );
for i in ${full_paths[@]}
do
	# NB: if this has already run, then full_paths will be empty
	# so we wont even get here to throw 'src doesnt exist' error
	# NB: dest_dir MUST have trailing '/'
	mv -i "$i" $dest_dir
done

print_num_types $dest_dir
exit

## 4. Find+Remove zero-byte files
# Print 0-byte files, then delete
echo "Zero-byte files:"
find $dest_dir -type f -size 0; # print
find $dest_dir -type f -size 0 -print0 | xargs -0 -I{} rm '{}' # remove
echo ''


# Before conversion
print_num_types $dest_dir;
num_files_pre_cnv=$(find $dest_dir -type f | wc -l)
num_zb_files_pre_cnv=$(find $dest_dir -type f -size 0 | wc -l)
expected_num_out=$(echo $num_files_pre_cnv-$num_zb_files_pre_cnv | bc);
echo ''


## (a+b) Dump bitrates for m4a and aiff and average
dump_bitrates $dest_dir m4a
avg_bitrate m4a;
dump_bitrates $dest_dir aiff
avg_bitrate aiff;


exit
## 5a. Convert all aiff's to mp3's using 320 CBR (incurs loss)
# Keep name- only change extension, delete the original aiff
aiff_paths=$(find $dest_dir -name *.aiff -type f);
for i in ${aiff_paths[@]}
do
	#echo $i | sed -n -e s/\.aiff$/\.mp3/p; # Test
	ffmpeg -i $i -codec:a libmp3lame -b:a 320k $(echo $i | sed -n -e s/\.aiff$/\.mp3/p);
	rm $i
done
exit


## 5b. Convert all m4a's to mp3's using 220-260 VBR
#TODO


## 6. Print filetypes post processing
print_num_types $dest_dir;
echo ''
echo "Expected num: $expected_num_out"

















