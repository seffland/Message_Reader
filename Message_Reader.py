__author__ = 'Steven Effland'
import os.path
import time


def start(argument):
    print "Starting fortran program with " + argument

path_to_watch = "C:/Users/seffl_000/Documents/WORK/Message-Reader/"
before = dict([(f, None) for f in os.listdir(path_to_watch)])
while 1:
    time.sleep(10)
    after = dict([(f, None) for f in os.listdir(path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added:
        print "Added: ", ", ".join(added)
        start(added)
    if removed:
        print "Removed: ", ", ".join(removed)
    before = after
