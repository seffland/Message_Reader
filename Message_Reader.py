__author__ = 'Steven Effland'
import os.path
import time


def start(argument):
    print "Starting fortran program with ", ": ".join(argument)


def newmsgcheck(path, dirpath):
    filelist = []
    filelist += [file for file in os.listdir(dirpath) if os.path.isfile(file)]
    for item in filelist:
        print item
    return True


path_to_watch = "C:\Users\seffl_000\Documents\Message_Reader"
before = dict([(f, None) for f in os.listdir(path_to_watch)])
while 1:
    time.sleep(10)
    after = dict([(f, None) for f in os.listdir(path_to_watch)])
    added = [f for f in after if not f in before]
    if added:
        if newmsgcheck(added, path_to_watch):
            print "Added: ", ", ".join(added)
            start(added)
    before = after
