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

def removeNonAscii(s): 
	return "".join(i for i in s if ord(i)<128)

def ensure_dir(f, isFile='true'):
	#make sure a directory exists, create it otherwise	
	if isFile == 'true':
		d = os.path.dirname(f)
	else:
		d = f
		
	if not os.path.exists(d):
		print "creating directory: " + d
		os.makedirs(d)
	else:
		print "directory exists ( " + d + " )"	
		
def removeBadChars(s, allowSpace = 0):
	charsToStrip = ['\n', '\t','"', "'", '?', '!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '\\', '/', '{', '}', '|', ':', ';', ',', '<', '>', '(', ')']		
	if allowSpace == 0:
		charsToStrip.append(" ")
	for char in charsToStrip:
		s = s.replace(char, '') #remove all illegal chars
		
	return s
		
def octo_header(title, date, categories, comments='false'):
	date = date.replace(' ', '-') #clean up the date
	
	header = "---\n"
	header = header + "layout: post\n"
	header = header + "title: " + title + "\n"
	header = header + "date: " + date + "\n"
	if comments == 'true':
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
	cats = ["jbs"]
	print "getting tags"
	for line in lFile: #[startingLine:]:
		#print "line: " + line
		if line.upper().find("TAGS:") > -1 or line.upper().find("CATEGORIES:") > -1:
			#Read as a list
			#print "line has tags: " + line
			arLine = line.split("#") #split on the hash
			for c in arLine[1:]:
				#print "tag: " + c
				tag = removeBadChars(c)
				tag = tag.replace('.', '')
				if tag != "" and not tag.isdigit(): #don't take null strings, or numbers
					cats.append(c.rstrip() )
		elif line.find("#") > -1:
			#line just has a random hashtag-tag in it
			#print "line has tags: " + line
			arLine = line.split("#")
			for section in arLine[1:]:
				section = section.split(" ") #now split on space
				tag = removeBadChars(section[0].rstrip())
				tag = tag.replace('.', '')
				if tag != "" and not tag.isdigit():	#don't take null strings, or numbers
					#print "tag: " + tag
					cats.append(tag)
	print "done with for-loop"
	
	print "exiting jbs_GetTags()"
	return cats
	
def normalizeDate(text):
	print text;
	outDate = text #initial assignment
	jbsDate = text.split(" ") #split it up by string.
	if len(jbsDate) == 2:
		#ie. 2010-02-16 07:20:36	
		#print "yyyy-mm-dd hh:mm:ss"
		jbsTime = jbsDate[1] #time is the second half
		jbsDate = jbsDate[0].split("-") #split the first half by the hyphen
		if len(jbsDate) <= 1:
			return outDate
		#else:
			#should be a correctly formatted string for octopress
			outDate = text #done at top
		
	elif len(jbsDate) == 3:
		#ie. Dec 24 2011
		#print "Month dd yyy"
		day = str(monthToNum(jbsDate[0]))
		if len(day) < 2:
			day = "0" + day
		outDate = str(jbsDate[2]) + "-" + day + "-" + str(jbsDate[1])
		
	elif len(jbsDate) == 1:
		#ie. 2011-01-02
		#this is ok for octopress too
		#print "yyyy-mm-dd"
		outDate = text #done at top.
		
	else:
		#ie... ?
		print "unknown date format"
		return None
	
	outDate = outDate.rstrip()
	outDate = outDate.replace("\n", "")
	return outDate
	
def createOutFilename(outDir, date, title):
	print "outdir: " + outDir
	
	ensure_dir(outDir, 'false')
	if outDir[-1] != ["/"]:
		outDir = outDir + "/"
	
	outFileName = date.split(" ")[0] + "-" + title + ".md" 
	outFileName = removeBadChars(outFileName)
	
	print "outfile: " + outFileName
	outFileName = outDir + outFileName #prepend directory
	
	return outFileName
	
def cleanupOutput(text):
	
	text = removeNonAscii(text)
	
	#text = text.rstrip()
	text = text.lstrip()
	
	#HTML stuffs:
	text = text.replace("<br>", "\n")
	text = text.replace("</br>", "")
	text = text.replace("<P>", "\n")
	text = text.replace("</P>", "")
	
	#check for blank:
	if text == "":
		text = "\n"
		
	return text
	
def convertJBSFileToOctopress(inFname,lFile, outDir):
	useComments = 'false' #disable comments by default for converted posts.
	
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
			title = line.strip()
			title = removeBadChars(title[1:], 1)
			break
		nLine = nLine + 1
	if title == None:
		title = "no Title" #assign a default title
	title = title.rstrip()
	title = title.replace(' ', '-') #replace spaces with dashes
	print "title: " + title
	
	#keep parsing and look for "Tags:" or "Categories:" etc
	categories = jbs_GetTags(lFile, nLine)
	#print "categories: " 
	#print categories
		
	outFileName = createOutFilename(outDir, date, title)
	
	print "starting to write output file: " + outFileName
	try : 
		of = open(outFileName, 'w')
		of.write( octo_header(title, date, categories, useComments) )
		for line in lFile[nLine+1:]:
			line = cleanupOutput(line)
			of.write( line ) #write the rest of the file
		of.write( "\n original filename: " + str(inFname) )
		of.close()
	finally :
		print "could not write file for output"


def main(argv):
	args = sys.argv[1:] #skip the filename
	workingDir = args[0]
	outDir = os.path.join(workingDir,"converted_files")
	
	dirlisting = os.listdir(workingDir)
	dirlisting.sort()
	for infile in dirlisting:
		print "current file is: " + infile
		try :
			f = open(workingDir + infile, 'r')
			lFile = f.readlines() #read the lines into a list
			convertJBSFileToOctopress(infile, lFile, outDir)
			print "file converted"
		finally :
			print "file could not be opened for reading (may be directory)"
			pass
			

			
	
	
if __name__ == "__main__":
    main(sys.argv[1:])


