import os

# NOTHING MUSIC-RELATED IN HERE

class File:

	def __init__(self, filename, location):

		self.name = filename;
		self.location = location;
		self.ext = filename.split('.')[-1];
		self.path = os.path.join(location, filename);
		self.safepath = File.GetSafePath(self.path);


	def pprint(self):

		toPrint = self.name + '\n' + self.location + '\n';
		print(toPrint);


	@staticmethod
	def GetSafePath(path):

		path = path.replace(' ', '\ ');
		path = path.replace('(', '\(');
		path = path.replace(')', '\)');
		return path;


	@staticmethod
	def GetExtension(pathIn):

		return pathIn.split('.')[-1];



class FileList:

	def __init__(self, rootDir='./'):

		self.rootDir = rootDir;
		self.files = [];

		# recurse through all dirs starting and root_dir
		for dirName, subsirList, fileList in os.walk(rootDir):

			# for each file in current directory
			for i in range(0, len(fileList)):

				#print(file_list);
				self.files.append(File(fileList[i], dirName));


	def findZeroByteFiles(self):

		zbfs = [];

		for i in range(0, len(self.files)):

			if os.stat(self.files[i].path).st_size == 0:

				zbfs.append(self.files[i]);

		if len(zbfs) == 0:

			print('No zero-byte files');

		else:
			for i in range(0, len(zbfs)):

				zbfs[i].pprint();


	# Return a list of all file extensions in file list
	def getExtensions(self):
		
		extNames = [];
		
		for i in range(0, len(self.files)):

			if self.files[i].ext not in extNames:

				extNames.append(self.files[i].ext);

		return extNames;


	def extensionHist(self):

		extNames = [];
		extCount = [];

		for i in range(0, len(self.files)):

			extTmp = self.files[i].ext;

			if extTmp in extNames:

				extCount[extNames.index(extTmp)] += 1;

			else:

				extNames.append(extTmp);
				extCount.append(1);

		total = 0;

		for i in range(0, len(extNames)):

			total += extCount[i];
			print(extNames[i] + ',\t' + str(extCount[i]));

		print('\nTotal, ' + str(total));


	def findByExtension(self, ext):

		for i in range(0, len(self.files)):

			if self.files[i].ext == ext:

				self.files[i].pprint();


