import sys
import os

num_files_converted = 0
num_files_to_convert = 0

def should_convert(file):
	if os.path.isfile(file) == False:
		return False
	elif file.endswith(".png") or file.endswith(".PNG") or file.endswith(".bmp") or file.endswith(".BMP"):
		return True
	else:
		return False

dir_depth = 0
def convert_in_dir(dir):
	file_list = os.listdir(dir)
	num_of_files = 0
	for file in file_list:
		#always use absolute path.
		file_path = os.path.join(dir, file)
		if should_convert(file_path) == True:
			# actually converting the file.
			print ("Converting [{0}]...".format(file_path))
			os.system("magick convert \"{0}\" \"{1}.jpg\"".format(file_path, os.path.splitext(file_path)[0]))
			os.remove(file_path)

			global num_files_converted
			num_files_converted = num_files_converted + 1
			if num_files_to_convert != 0:
				print ("Processed [{0}/{1}]".format(num_files_converted, num_files_to_convert) + " ({:.2%})".format( float(num_files_converted) / num_files_to_convert))

		elif os.path.isdir(file_path):
			convert_in_dir(file_path)

# depth first count how many files in total needed to be converted.
def num_to_convert(dir):
	file_list = os.listdir(dir)
	num_of_files = 0
	for file in file_list:
		#always use absolute path.
		file_path = os.path.join(dir, file)
		if should_convert(file_path) == True:
			num_of_files = num_of_files + 1
		elif os.path.isdir(file_path):
			num_of_files = num_of_files + num_to_convert(file_path)

	if num_of_files > 0:
		print ("Num of files to convert in {0}: {1}".format(dir, num_of_files))	
	return num_of_files


print ("\n\n****************************************************************")

print ("NOTICE: this use magick command line imag conversion tool. ")
print ("Start converting PNGs to JPEGs...")

rootDir = sys.argv[1]

print ("Root directory: [{0}]".format(rootDir))
print ("Start counting num of files to convert...")
num_files_to_convert = num_to_convert(rootDir)
if num_files_to_convert != 0:
	print ("Total to convert: {0}. Proceed? (Y/n)".format(num_files_to_convert))
	user_input = input()
	if user_input == "Y":
		print ("Start converting...")
		convert_in_dir(rootDir)
else:
	print("No file found needs to be converted. Ending.")

print ("[End]")
print ("****************************************************************\n\n")


