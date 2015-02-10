__author__ = 'Steven Effland'
import os.path
import time
import ConfigParser
import psutil
import datetime
import math

# Built in config funct
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def checkCPU(baseCPU):
    runningCPU = psutil.cpu_percent(interval=1)
    proccessCPU = runningCPU - baseCPU
    if runningCPU + proccessCPU < 100:
        return True
    else:
        return False


def start(alertname, dirname):
    print "Starting fortran program with " + dirname
    baseCPU = psutil.cpu_percent(interval=1)
    # TODO insert fortran argument here
    os.system("mkdir " + dirname)
    os.system("cd " + dirname + "/")
    os.system("new_process " + dirname + alertname)
    if checkCPU(baseCPU) == True:
        print("I Can Start Another Process")


def newalertcheck(list, new):
    test = new[0]
    if test > max(list):
        return True
    else:
        return False


def timematch(newtime, eqtime):
    for item in eqtime:
        if (abs(item - newtime) < float(ConfigSectionMap("Earthquake Options")['delta_eptime'])):
            return True
    return False


def latlongmatch(newlatlong, latlonglist):
    for item in latlonglist:
        if (abs(item - newlatlong) < (float(ConfigSectionMap("Earthquake Options")['delta_latlong'])*math.cos(newlatlong))):
            return True
    return False

def depthmatch(newdepth, depthlist):
    for item in depthlist:
        if (abs(item - newdepth) < float(ConfigSectionMap("Earthquake Options")['delta_depth'])):
            return True
    return False

def newalert(filename, name, eqtime, lat, long, depth, magnitute):
    file = ''.join(filename)
    f = open(ConfigSectionMap("File Options")['path'] + "/" + file)
    junk = f.readline()

    newname = f.readline()
    newname = str(newname[12:])
    if newname in name:
        return False

    temptime = f.readline()
    temptime = temptime[6:]
    year, month, day, hour, min, second = temptime.split("/")
    newtime = datetime.datetime(int(year), int(month), int(day), int(hour), int(min), int(second))

    templat = f.readline()
    templat = templat[12:]
    newlat = float(templat)

    templong = f.readline()
    templong = templong[12:]
    newlong = float(templong)

    tempdepth = f.readline()
    tempdepth = tempdepth[13:]
    newdepth = float(tempdepth)

    tempmag = f.readline()
    tempmag = tempmag[12:]
    newmag = float(tempmag)

    if timematch(newtime, eqtime) and latlongmatch(newlat, lat) and latlongmatch(newlong, long) and depthmatch(newdepth, depth):
        print ("Duplicate Earthquake")
        return False
    else:
        name.append(newname)
        eqtime.append(newtime)
        lat.append(newlat)
        long.append(newlong)
        depth.append(newdepth)

    print newname
    print newtime
    print newlat
    print newlong
    print newdepth
    print newmag

    return True


def startoperational():
    path_to_watch = ConfigSectionMap("File Options")['path']
    filelist = []
    # Creates list of files in path
    for file in os.listdir(path_to_watch):
        filelist.append(file[0:3])

    #Make list of Earthquake elements
    name = []
    eqtime = []
    lat = []
    long = []
    depth = []
    magnitute =[]

    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while 1:
        time.sleep(10)
        after = dict([(f, None) for f in os.listdir(path_to_watch)])
        newfile = [f for f in after if not f in before]
        if newfile:
            if newalert(newfile, name, eqtime, lat, long, depth, magnitute):
                    print "new alert: ", ", ".join(newfile)
                    start(newfile, name[-1])
        before = after


def startresearch():
    maxprocnum = int(ConfigSectionMap("File Options")['maxfilesin'])
    print ("Max number of alerts = "), maxprocnum

    start = int(raw_input("Starting file: "))
    end = int(raw_input("Ending file: "))
    if (end - start) > maxprocnum:
        print("Too many files to proccess")
    elif (end - start) < maxprocnum:
        print("Starting fortran program from file:"), str(start) + "_alert.txt", ("to"), str(end) + "_alert.txt"

# Config file setup
Config = ConfigParser.ConfigParser()
configfile = "/home/seffland/config.ini"
Config.read(configfile)

# gets cpu percentage
#Use to monitor cpu consumption
#print(psutil.cpu_percent(interval=1))

mode = raw_input("Mode to start in: [O]perational or [R]esearch...")
if mode == "O" or mode == "o":
    print("Operational mode running...")
    startoperational()
if mode == "R" or mode == "r":
    print("Starting research mode...")
    startresearch()
else:
    print "Please input valid mode..."
    mode = raw_input("Mode to start in: [O]perational or [R]esearch...")


