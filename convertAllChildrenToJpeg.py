import sys
import os
import time
from multiprocessing import Process, Queue

def should_convert(file):
	if os.path.isfile(file) == False:
		return False
	elif file.endswith(".png") or file.endswith(".PNG") or file.endswith(".bmp") or file.endswith(".BMP"):
		return True
	else:
		return False

#convert a single file
def do_convert(file_path):
	num = 5
	#print ("Converting [{0}]...".format(file_path))
	os.system("magick convert \"{0}\" \"{1}.jpg\"".format(file_path, os.path.splitext(file_path)[0]))
	os.remove(file_path)

def gather_files(dir, queue):
	file_list = os.listdir(dir)
	num_of_files = len(file_list)
	for file in file_list:
		#always use absolute path.
		file_path = os.path.join(dir, file)
		if should_convert(file_path) == True:
			queue.put(file_path)
			# p = Process(target=do_convert, args=(file_path,))
			# p.start()

		elif os.path.isdir(file_path):
			gather_files(file_path, queue)

def batch_process(queue):
	while True:
		if queue.empty():
			break

		file_path = queue.get()
		if not file_path:
			break
		elif should_convert(file_path) == True:
			do_convert(file_path)
			# print progress info

def progress_checker(queue, n_total_files):
	while True:
		time.sleep(1)
		queuesize = queue.qsize()
		n_files_converted = n_total_files - queuesize
		print ("Processed [{0}/{1}]".format(n_files_converted, n_total_files) + " ({:.2%})".format( float(n_files_converted) / n_total_files))

		if queuesize == 0:
			print( "===== Finished converting all files ======" );
			break

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


if __name__ == '__main__':
	print ("\n\n****************************************************************")

	print ("NOTICE: this use magick command line imag conversion tool. ")
	print ("Start converting PNGs to JPEGs...")

	rootDir = sys.argv[1]
	pqueue = Queue()

	print ("Root directory: [{0}]".format(rootDir))
	print ("Start counting num of files to convert...")
	num_files_to_convert = num_to_convert(rootDir)
	if num_files_to_convert != 0:
		print ("Total to convert: {0}. Proceed? (Y/n)".format(num_files_to_convert))
		user_input = input()
		if user_input == "Y":
			print ("Start converting...")
			gather_files(rootDir, pqueue)

			# start the end checker process
			p_progresscheck = Process(target=progress_checker, args=(pqueue, num_files_to_convert))
			p_progresscheck.start()

			# number of processes
			for i in range(20):
				p = Process(target=batch_process, args=(pqueue, ))
				p.start()
	else:
		print("No file found needs to be converted. Ending.")

