import sys
import os
import shutil 
import importlib

num_files_converted = 0
num_files_to_convert = 0

# python thisScript searchInDir authorDir authorListName

searchdir = sys.argv[1]
authors_root = sys.argv[2]
authordir = authors_root
bindir = os.path.join(authors_root, "_Bin")

author_dict = {"authorname": "some path", 'authorname2': "some path"}

author_name_file = "{0}\\{1}".format(authors_root, sys.argv[3])
open(author_name_file, 'r')

logfile = "{0}\\log.txt".format(authors_root)
f = open(logfile, 'r+')
f.truncate()
f.close()

num_moved = 0

# append content to log file
def append( file, msg ):
	with open(file, "ab") as log:
		log.write(msg.encode('utf8'))

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size



# If can't find it, create a new one in 
# suthor root.
def build_author_dict(mode):
	dir_list = os.listdir(authors_root)
	author_dict.clear()
	with open(author_name_file) as names:
		for n in names:
			author = n.rstrip('\n')
			author = author.rstrip('\r')
			if len(author) != 0:
				if mode == 0:
					print("Finding path for [{0}]...".format(author))
				authordir = ""
				found = False
				for dir in dir_list:
					if dir.find(author) != -1:
						authordir = os.path.join(authors_root, dir)
						found = True

				if found == False:
					# Check bin, see if there's another one written by 
					# this author, and only create dir if there is.
					#print("N/A")
					binlist = os.listdir(bindir)
					has_another = 0
					for f in binlist:
						if f.find(author) != -1:
							has_another = has_another + 1
							#print("Found {0} {1}".format(has_another, author))
					if has_another > 1:
						newdir = os.path.join(authors_root, author)
						os.makedirs(newdir)
						authordir = newdir
						# also move existing to that folder
						for f in binlist:
							if f.find(author) != -1:
								print ("Moving {0}".format(os.path.join(bindir, f)))
								shutil.move(os.path.join(bindir, f), authordir)

					else:
						authordir = bindir
					#print("New Path: {0}\n".format(authordir))
				author_dict[author] = authordir
	
	if mode == 0:
		print ("Finished building author dict.")


def search_move(dir, depth):
	if False: 
		for x in range(0,depth):
			sys.stdout.write("    ")
		sys.stdout.write("-")
		sys.stdout.flush()
		print (os.path.split(dir)[1])
	file_list = os.listdir(dir)
	for file in file_list:
		#always use absolute path.
		file_path = os.path.join(dir, file)
		lower_file_path = file_path.casefold()
		found = False
		for author in author_dict.keys():
			if lower_file_path.find(author.casefold()) != -1 and file.casefold() != author.casefold(): # found it
				found = True
				print ("    [{0}]  attemp moving <{1}>...".format(author, file_path))

				#check if there is already file of same name there
				author_all_list = os.listdir(author_dict[author])
				already_exist = False
				for existing in author_all_list:
					if existing == file:
						already_exist = True
						break

				if already_exist == True:
					print ("    [{0}]conflict moving <{1}>...".format(author, file_path))
					# check if they are of the same size...
					my_size = get_size(file_path)
					existing_size = get_size(os.path.join(author_dict[author], file))
					print ("existing size = {0}".format(existing_size))
					print ("      my size = {0}".format(my_size))
					if existing_size > my_size * 0.9:
						print ("Same or large enough content exist. Removing...")
						shutil.rmtree(file_path)	
						append(logfile, "resolved conflict: [{0}] - <{1}>\r\n".format(author, file_path))
					else:
						append(logfile, "!!!!conflict: [{0}] - <{1}>\r\n".format(author, file_path))		
				else: 		
					#actually move the dir
					shutil.move(file_path, author_dict[author])
					append(logfile, "[{0}] - <{1}>\r\n".format(author, file_path))		
					global num_moved
					num_moved = num_moved + 1
				break
		if found == False and os.path.isdir(file_path):
			search_move(file_path, depth+1)




print ("\n\n****************************************************************")
append( logfile, "\n" )

if searchdir != authors_root:
	build_author_dict(0);
	if searchdir != bindir:
		search_move(searchdir, 0)

	print ("{0} directories moved.".format(num_moved))

	print ("Checking bin...")
	build_author_dict(1);

	if num_moved > 0:
		print ("\nRemoving empty folders...")
		os.system("python F:\\DevArchive\\Scripts\\removeEmptyFolders.py \"{0}\"".format(searchdir))
else:
	print ("Can't search in author directory.")

print ("\n[End]")
print ("****************************************************************\n\n")


