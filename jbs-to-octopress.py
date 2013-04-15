#!/usr/bin/env python2

###
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
####
# written by Jon Robbins (@jrobb) 2013
#	http://jrobb.org
###


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

def ensure_dir(f):
	#make sure a directory exists, create it otherwise
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)
		
def octo_header(title, date, categories, comments=None):
	header = "---\n"
	header = header + "layout: post\n"
	header = header + "title: " + title + "\n"
	header = header + "date: " + date + "\n"
	if comments == true:
		header = header + "comments: " + "true" + "\n"
	else:
		header = header + "comments: " + "false" + "\n"
		
	header = header + "categories: ["
	i = 0
	for c in categories:
		if i > 0:
			header = header + ", "
		header = header + c
		i = i + 1
	header = header + "]\n"
	header = header + "---\n"
	return header
	
def jbs_GetTags(lFile, 	startingLine):
	for line in lFile[startingLine:]:
		if line.upper().find("TAGS:") or line.upper().find("CATEGORIES:"):
			#Read as a list
			arLine = line.split("#") #split on the hash
			for c in arLine[1:]:
				cats.append[c.rstrip()]
		elif line.find("#"):
			#line just has a random hashtag-tag in it
			arLine = line.split("#")
			for section in arLine[1:]:
				section = section.split(" ") #now split on space
				cats.append[section[0]]
	
	return cats
		
def convertJBSFileToOctopress(lFile, outDir):
	#print "the first line is: " + lFile[0]
	date = normalizeDate(lFile[0]) #first line should be the date
	print date
	if date == None:
		print "error in file format"
		sys.exit(2)
	
	title = None
	nLine = 1
	for line in lFile[1:]:	#start on the second line, first line captured the date
		if lFile == "":
			pass		#skip blank lines, until we get to the title, anyway.
		elif line[0] =="\\":
			#titles are denoted with a '\'
			title = line[1:] 
			break
		nLine = nLine + 1
			
	if title == None:
		title = "no Title" #assign a default title
		
	#keep parsing and look for "Tags:" or "Categories:" etc
	categories = jbs_GetTags(lFile, nLine)
		
	ensure_dir(outDir)
	outFileName = outDir + "/" + date + "-" + title.replace(' ', '-') #replace spaces with dashes
	outFileName = outFileName.replace("'", '') #remove single quotes. should probably remove all illegal chars
	
	of = open(outFielName, 'w')
	of.write( octo_header(title, date, categories, useComments) )
	of.write( lFile[nLine:] ) #write the rest of the file
	of.close()

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
	outDir = workingDir + '/' + "converted_files"
	
	dirlisting = os.listdir(workingDir)
	dirlisting.sort()
	for infile in dirlisting:
		#print "current file is: " + infile
		try :
			f = open(workingDir + infile, 'r')
			lFile = f.readlines() #read the lines into a list
			convertJBSFileToOctopress(lFile, outDir)
			
		except :
			#file could not be opened for reading
			pass
			

			
	
	
if __name__ == "__main__":
    main(sys.argv[1:])


