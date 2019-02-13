import sys
import os

print ("\n\n****************************************************************")

print ("Deleting every other file...")

directory = sys.argv[1]
target_num = 0
# if len(sys.argv) > 2 :
# 	target_num = int(sys.argv[2])
# 	print "Target number: {0}".format(target_num)


print ("Directory: [{0}]".format(directory))

file_list = os.listdir(directory)
num_of_files = len(file_list)
print ("Number of files: {0}".format(num_of_files))

do_delete = False
counter = 0
for img in file_list:
	if img.endswith(".bat") or img.endswith(".py"):
		do_delete = do_delete
	elif do_delete == True:
		file_path = os.path.join(directory, img)
		print ("Deleted {0}".format(file_path))
		os.remove(file_path)
		do_delete = False
		counter = counter + 1
	else: 
		do_delete = True

print ("Finished one run-thru. Deleted [{0}] files.".format(counter))
num_of_files = num_of_files - counter
print ("****************************************************************\n\n")


