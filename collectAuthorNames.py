import sys
import os
import shutil 

num_files_converted = 0
num_files_to_convert = 0

authors_root = "K:\漫画和本子"

author_name_file = "{0}\\author_list.txt".format(authors_root)
open(author_name_file, 'w+')


# append content to log file
def append( msg ):
	with open(author_name_file, "a") as log:
		log.write('%s' % msg)

dir_list = os.listdir(authors_root)
for dir in dir_list:
	print (dir)
	file_path = os.path.join(authors_root, dir)
	if os.path.isdir(file_path):
		append("{0}\n".format(dir))
