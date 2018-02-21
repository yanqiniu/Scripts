import sys
import os

root_dir = sys.argv[1]


def is_empty(dir):
	isempty = False
	file_list = os.listdir(dir)
	if not file_list and os.path.isdir(dir):
		print ("Removing [{0}]".format(dir))
		#os.startfile(dir)
		os.rmdir(dir)
		isempty = True
	else:
		for file in file_list:
			file_path = os.path.join(dir, file)
			if os.path.isdir(file_path):
				is_empty(file_path)
		if len(os.listdir(dir)) == 0:
			print ("Removing [{0}]".format(dir))
			#os.startfile(dir)
			os.rmdir(dir)




is_empty(root_dir)