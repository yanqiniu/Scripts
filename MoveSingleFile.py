# moves a document to the Archive bin folder.
import sys
import os
import shutil 


archive_bin_dir = sys.argv[1]
file_path = sys.argv[2]


shutil.move(file_path, archive_bin_dir)