# A template script for basic file ops to make life easier :)
# 2/24/2019 Roy Niu


import os

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

############################################
# Template section, change things here for
# specifc use cases.
############################################

def condition(path):
    filename = os.path.basename(path)
    foldername = os.path.abspath(os.path.join(path, os.pardir))
    return False

#operation on a single file:
def operation(path):
    filename = os.path.basename(path)
    foldername = os.path.abspath(os.path.join(path, os.pardir))
    print("Operating in {0} --- {1}".format(foldername, filename))

#################################
def for_each_child_in_dir(directory, doSearchSubfolder):
    allfiles = os.listdir(directory)
    for f in allfiles:
        file_path = os.path.join(directory, f)
        if condition(file_path):
            operation(file_path)
        elif doSearchSubfolder and os.path.isdir(file_path):
            for_each_child_in_dir(file_path, doSearchSubfolder)

############################################
# Actual running logic: 
############################################
for_each_child_in_dir(CUR_DIR, False)