__author__ = 'Steven Effland'
import os.path
import time


def start(argument):
    print "Starting fortran program with ", ": ".join(argument)


def newalertcheck(list, new):
    test = new[0]
    if test > max(list):
        print "New Alert!"
    return True

def startoperational():
    path_to_watch = "C:\Users\seffl_000\Documents\WORK\Message-Reader\Alerts"
    filelist = []
    #Creates list of files in path
    for file in os.listdir(path_to_watch):
        filelist.append(file[0:3])

    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while 1:
        time.sleep(10)
        after = dict([(f, None) for f in os.listdir(path_to_watch)])
        newfile = [f for f in after if not f in before]
        if newfile:
            if newalertcheck(filelist, newfile):
                print "new alert: ", ", ".join(newfile)
                start(newfile)
        before = after


def startresearch():
    start = raw_input("Starting file:")
    end = raw_input("Ending file")


mode = raw_input("Mode to start in: [O]perational or [R]esearch...")
if mode == "O" or "o":
    print("Operational mode running...")
    startoperational()
elif mode == "R" or "r":

    startresearch()
else:
    print "Please input valid mode..."
    mode = raw_input("Mode to start in: [O]perational or [R]esearch...")



