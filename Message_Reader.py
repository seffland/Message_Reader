__author__ = 'Steven Effland'
import os.path

startingNum = raw_input("Input starting alert number")

filepath = "C:/Users/seffl_000/Documents/WORK/"
endText = "_alert.txt"

#Checks to see if file exists
print "Searching for: " + startingNum + endText
print os.path.isfile(filepath+startingNum+endText)

