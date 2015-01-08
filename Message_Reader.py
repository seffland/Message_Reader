__author__ = 'Steven Effland'
import os.path
import time
import ConfigParser
import psutil

#Built in config funct
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
    runningCPU = psutil.cpu_percent(interval = 1)
    proccessCPU = runningCPU - baseCPU
    if runningCPU+proccessCPU<100:
        return True
    else:
        return False

def start(filename):
    print "Starting fortran program with ", ": ".join(filename)
    baseCPU = psutil.cpu_percent(interval = 1)
    #TODO insert fortran argument here
    #os.system("cd " + filename + "/")
    #rm set_loop_parameters.pro
    #rm *event.txt
    #rm gnss_request.txt
    #rm *_message
    #rm *_solution_pars.dat
    # rm timeseries/*.dat
    # gnss_server < gnss_server_ts.pro > gnss_server.lis | grep 'Request detected' gnss_server.lis &
    # geqdis < geqdis_operational.pro > geqdis.lis | grep 'Displacement field available' geqdis.lis &
    # earthquake < earthquake_$1.pro > earthquake.lis | grep 'Event detected' earthquake.lis &
    if checkCPU(baseCPU) == True:
        print("I Can Start Another Process")

def newalertcheck(list, new):
    test = new[0]
    if test > max(list):
        return True
    else:
        return False

def startoperational():
    path_to_watch = ConfigSectionMap("File Options")['path']
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
    maxprocnum = int(ConfigSectionMap("File Options")['maxfilesin'])
    print ("Max number of alerts = "), maxprocnum

    start = int(raw_input("Starting file: "))
    end = int(raw_input("Ending file: "))
    if (end - start) > maxprocnum:
        print("Too many files to proccess")
    elif (end - start) < maxprocnum:
        print("Starting fortran program from file:"), str(start) + "_alert.txt", ("to"), str(end) + "_alert.txt"

#Config file setup
Config = ConfigParser.ConfigParser()
configfile = "C:\Users\seffl_000\Documents\Message_Reader\config.ini"
Config.read(configfile)

#gets cpu percentage
#Use to monitor cpu consumption
print(psutil.cpu_percent(interval=1))

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



