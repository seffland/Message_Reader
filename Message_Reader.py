#!/usr/bin/python
__author__ = 'Steven Effland'
import os.path
import time
import ConfigParser
import psutil
import datetime
import math
import linecache
from Update_PHP import llupdater
from Update_PHP import equpdater


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


def updatePHP(alertname, earthquakename, date):
    print "Updating php files..."
    os.system("update_web " + earthquakename + ConfigSectionMap("File Options")['web_dir'])
    llupdater(earthquakename, date)
    equpdater(earthquakename)
    return


def researchupdatePHP(alertname, earthquakename, date):
    print "Updating php files..."
    os.system("researchupdate_web " + earthquakename + ConfigSectionMap("File Options")['web_dir'])
    llupdater(earthquakename, date)
    equpdater(earthquakename)
    return


def setparameters():
    filename = "set_parameters.pro"
    target = open(filename, 'a')
    target.write("sampling " + ConfigSectionMap("Set Parameters Options")['sampling'])
    target.write("network " + ConfigSectionMap("Set Parameters Options")['network'])
    target.write("station_dir " + ConfigSectionMap("Set Parameters Options")['station_dir'])
    target.write("fp_dir " + ConfigSectionMap("Set Parameters Options")['fp_dir'])
    target.write("model_dir " + ConfigSectionMap("Set Parameters Options")['model_dir'])
    target.write("ts_dir " + ConfigSectionMap("Set Parameters Options")['ts_dir'])
    target.close()
    return

def start(alertname, dirname, date):
    print "Starting fortran program with " + dirname
    baseCPU = psutil.cpu_percent(interval=1)

    #Strip extra chars
    earthquakename, junk1, junk2 = dirname.partition(" ")

    #Create dirs
    os.system("mkdir " + earthquakename)
    os.chdir(earthquakename)
    setparameters()
    os.system("mkdir models")
    os.system("mkdir timeseries")
    #Start new_process
    os.system("new_process " + str(earthquakename) + " " + str(alertname))

    #Update the PHP files
    updatePHP(alertname, earthquakename, date)

    return


def researchstart(alertname, dirname, date):
    print "Starting fortran program with " + dirname
    baseCPU = psutil.cpu_percent(interval=1)

    #Strip extra chars
    earthquakename, junk1, junk2 = dirname.partition(" ")

    #Create dirs
    os.system("mkdir " + earthquakename)
    os.chdir(earthquakename)
    setparameters()
    os.system("mkdir models")
    os.system("mkdir timeseries")
    #Start new_process
    os.system("researchnew_process " + str(earthquakename) + " " + str(alertname))

    #Update the PHP files
    researchupdatePHP(alertname, earthquakename, date)

    return

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

    #Waits for new file in path
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while 1:
        time.sleep(10)
        after = dict([(f, None) for f in os.listdir(path_to_watch)])
        newfile = [f for f in after if not f in before]
        if newfile:
            if newalert(newfile, name, eqtime, lat, long, depth, magnitute):
                    print "new alert: ", ", ".join(newfile)
                    start(newfile, name[-1], str(eqtime[-1]))
        before = after


def research():
    maxprocnum = int(ConfigSectionMap("File Options")['maxfilesin'])
    print ("Max number of alerts = "), maxprocnum

    start = int(raw_input("Starting file: "))
    end = int(raw_input("Ending file: "))
    if (end - start) > maxprocnum:
        print("Too many files to proccess")
    elif (end - start) < maxprocnum:
        print("Starting fortran program from file:"), str(start) + "_alert.txt", ("to"), str(end) + "_alert.txt"
        for x in range(start, end):
            aname = str(x) + "_alert.txt"
            fpath = ConfigSectionMap("File Options")['path'] + "/" + aname
            f = open(fpath)
            junk = f.readline()

            #Get eqname
            newname = f.readline()
            newname = str(newname[12:])
            print newname

            #Get Date From Files
            date = linecache.getline(fpath, 3)
            date = date[6:]
            year, month, day, hour, min, second = date.split("/")
            newdate = datetime.datetime(int(year), int(month), int(day), int(hour), int(min), int(second))
            print newdate

            researchstart(aname, newname, newdate)


# Config file setup
Config = ConfigParser.ConfigParser()
configfile = "config.ini"
Config.read(configfile)

mode = raw_input("Mode to start in: [O]perational or [R]esearch")
if mode == "O" or mode == "o":
    print("Operational mode running...")
    startoperational()
if mode == "R" or mode == "r":
    print("Starting research mode...")
    research()
else:
    print "Please input valid mode..."


