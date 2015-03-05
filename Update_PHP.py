#!/usr/bin/python
__author__ = 'Steven Effland'
import os.path
import fileinput

def llupdater(eqname, date):
    with open('/home/webwork/mari/GREAT/solutions/local_links_operational.php', 'r') as file:
        lines = file.readlines()

    line1 = ('<a href="' + eqname + '".php" target="main">' + date + '</a>\n')
    line2 = '</td></tr><tr><td class="menuele">\n'
    final = line1 + line2
    index = 2
    lines.insert(index, final)

    with open('/home/webwork/mari/GREAT/solutions/local_links_operational.php', 'w') as file:
        lines = "".join(lines)
        file.write(lines)


def equpdater(eqname):
    tempfile = "/home/webwork/mari/GREAT/solutions/temp.php"
    eqfile = "/home/webwork/mari/GREAT/solutions/" + eqname + ".php"
    searchchar = "#####"

    os.system("cp " + tempfile + " " + eqfile)

    f = open(eqfile, 'r')
    data = f.read()
    f.close()

    newdata = data.replace(searchchar, eqname)

    f = open(eqfile, 'w')
    f.write(newdata)
    f.close()
