import sys
import os
import shutil 
import importlib

num_files_converted = 0
num_files_to_convert = 0

searchdir = sys.argv[1]
authors_root = "K:\漫画"
authordir = authors_root

author_dict = {"authorname": "some path", 'authorname2': "some path"}

author_name_file = "{0}\\author_list.txt".format(authors_root)
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
def build_author_dict():
	dir_list = os.listdir(authors_root)
	author_dict.clear()
	with open(author_name_file) as names:
		for n in names:
			author = n.rstrip('\n')
			author = author.rstrip('\r')
			if len(author) != 0:
				print("Finding path for [{0}]...".format(author))
				authordir = ""
				found = False
				for dir in dir_list:
					if dir.find(author) != -1:
						authordir = os.path.join(authors_root, dir)
						found = True

				if found == False:
					newdir = os.path.join(authors_root, author)
					os.makedirs(newdir)
					authordir = newdir
				author_dict[author] = authordir

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
		found = False
		for author in author_dict.keys():
			if file_path.find(author) != -1 and file != author: # found it
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
						print ("Same content. Removing...")
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

build_author_dict();
search_move(searchdir, 0)

print ("{0} directories moved.".format(num_moved))
print ("\nRemoving empty folders...")
os.system("python F:\\DevArchive\\Scripts\\removeEmptyFolders.py \"{0}\"".format(searchdir))
print ("\n[End]")
print ("****************************************************************\n\n")


