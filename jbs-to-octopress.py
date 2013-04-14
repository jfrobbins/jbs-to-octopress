#!/usr/bin/env python2
import sys
import os

def monthToNum(month):
	#a text month gets passed in.
	#	ie. "Dec" or "December"
	#and a number is returned.
	#	ie. 12
	month = month.upper()
	if month == "JANUARY" or month == "JAN":
		return 1
	elif month == "FEBRUARY" or month == "FEB":
		return 2
	elif month == "MARCH" or month == "MAR":
		return 3
	elif  month == "APRIL" or month == "APR":
		return 4
	elif  month == "MAY":
		return 5
	elif  month == "JUNE" or month == "JUN":
		return 6
	elif  month == "JULY" or month == "JUL":
		return 7
	elif  month == "AUGUST" or month == "AUG":
		return 8
	elif  month == "SEPTEMBER" or month == "SEPT":
		return 9
	elif  month == "OCTOBER" or month == "OCT":
		return 10
	elif  month == "NOVEMBER" or month == "NOV":
		return 11
	elif  month == "DECEMBER" or month == "DEC":
		return 12
	else:
		return 0

def convertJBSFileToOctopress(lFile)
	#print "the first line is: " + lFile[0]
	date = normalizeDate(lFile[0]) #first line should be the date
	print date
	if date == None:
		print "error in file format"
		sys.exit(2)
	
	

def normalizeDate(text):
	outDate = text #initial assignment
	jbsDate = text.split(" ") #split it up by string.
	if len(jbsDate) == 2:
		#ie. 2010-02-16 07:20:36	
		print "yyyy-mm-dd hh:mm:ss"
		jbsTime = jbsDate[1] #time is the second half
		jbsDate = jbsDate[0].split("-") #split the first half by the hyphen
		if len(jbsDate) <= 1:
			return outDate
		#else:
			#should be a correctly formatted string for octopress
			#outDate = text #done at top
		
	elif len(jbsDate) == 3:
		#ie. Dec 24 2011
		print "Month dd yyy"
		outDate = jbsDate[2] + "-" + monthToNum(jbsDate[0]) + "-" + jbsDate[1]
		
	elif len(jbsDate) == 1:
		#ie. 2011-01-02
		#this is ok for octopress too
		print "yyyy-mm-dd"
		#outDate = text #done at top.
		
	else:
		#ie... ?
		print "unknown date format"
		return None
	
	return outDate

def main(argv):
	args = sys.argv[1:] #skip the filename
	workingDir = args[0]
	
	dirlisting = os.listdir(workingDir)
	dirlisting.sort()
	for infile in dirlisting:
		#print "current file is: " + infile
		try :
			f = open(workingDir + infile, 'r')
			lFile = f.readlines() #read the lines into a list
			convertJBSFileToOctopress(lFile)
			
		except :
			#file could not be opened for reading
			pass
			

			
	
	
if __name__ == "__main__":
    main(sys.argv[1:])

