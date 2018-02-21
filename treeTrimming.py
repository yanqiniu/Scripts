import os
import sys
import shutil

num_of_dir_removed = 0

def has_single_folder_child(dir):
	file_list = os.listdir(dir)
	if len(file_list) == 1:
		file_path = os.path.join(dir, file_list[0])
		if os.path.isdir(file_path):
			return True
		else:
			return False
	else:
		return False


def search_dir(dir):
	if has_single_folder_child(dir):
		print ("Found <{0}>".format(dir))

		# compare name len, rename parent folder to this if it's shorter
		par_of_dir = os.path.split(dir)[0]
		dir_folder = os.path.split(dir)[1]
		child_folder = os.listdir(dir)[0]
		if len(dir_folder) < len(child_folder):
			print ("1")
			existing_list = os.listdir(par_of_dir)
			already_exist = False
			for existing in existing_list:
				if existing == child_folder:
					already_exist = True
					break
			if already_exist == False:
				os.rename(dir, os.path.join(par_of_dir, child_folder))
				dir = os.path.join(par_of_dir, child_folder)
			print ("2")

		# get child folder path.
		child_folder = os.listdir(dir)[0]
		child_folder = os.path.join(dir, child_folder)

		# rename the folder to ensure no overlap when copying
		os.rename(child_folder, os.path.join(dir, "[TODELETE]"))
		child_folder = os.path.join(dir, "[TODELETE]")

		# move grandchildren to be children
		grandchildren = os.listdir(child_folder)
		for gc in grandchildren:
			print ("Attempt Moving {0} to {1}".format(os.path.join(child_folder, gc), dir))
			#check if there is already file of same name there
			existing_list = os.listdir(dir)
			already_exist = False
			for existing in existing_list:
				if existing == gc:
					already_exist = True
					print("found!!!!")
					break

			if already_exist == True:
				print ("Conflict Moving {0} to {1}...".format(os.path.join(child_folder, gc), dir))
				# check if they are of the same size...
				my_size = get_size(os.path.join(child_folder, gc))
				existing_size = get_size(os.path.join(dir, gc))
				print ("existing size = {0}".format(existing_size))
				print ("      my size = {0}".format(my_size))
				if existing_size > my_size * 0.9:
					print ("Same content. Removing...")
					shutil.rmtree(os.path.join(child_folder, gc))	
				else:
					print ("conflict!!! {0}".format(os.path.join(child_folder, gc)))		
			else:
				shutil.move(os.path.join(child_folder, gc), dir)
		global num_of_dir_removed
		os.rmdir(child_folder)
		num_of_dir_removed = num_of_dir_removed + 1

		# Grandchildren moved. Now do it again to see if new is a single folder.
		search_dir(dir)

	else:
		children = os.listdir(dir)
		for c in children:
			c_path = os.path.join(dir, c)
			if os.path.isdir(c_path):
				search_dir(c_path)


print 



print ("\n\n****************************************************************")
print ("Trimming pointlessly deep directories...")
rootdir = sys.argv[1]
os.system("python F:\\DevArchive\\Scripts\\removeEmptyFolders.py \"{0}\"".format(rootdir))
print ("Empty folders removed, start trimming paths...")
search_dir(rootdir)

print ("\nFinished. {0} useless directories removed.".format(num_of_dir_removed))
print ("[End]")
print ("****************************************************************\n\n")
