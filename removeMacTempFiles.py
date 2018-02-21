import sys
import os

num_deleted = 0
def remove_from_dir(dir):

	file_list = os.listdir(dir)
	num_of_files = 0
	for file in file_list:
		file_path = os.path.join(dir, file)
		if os.path.isfile(file_path) == True:
			# actually converting the file.
			if file.startswith("._"):
				os.remove(file_path)
				print ("Removing [{0}]".format(file_path))
				global num_deleted
				num_deleted = num_deleted + 1
		elif os.path.isdir(file_path):
			remove_from_dir(file_path)

print ("\n\n****************************************************************")
print ("Removing files that starts with \"._\"...")

rootdir = sys.argv[1]

print ("Root directory: [{0}]".format(rootdir))
print ("Start searching...")

remove_from_dir(rootdir)

print ("{0} files removed.".format(num_deleted))
print ("[Finished]")
print ("****************************************************************\n\n")


