#!/usr/bin/python

import os
import glob
import re
import argparse

filePatternToTest="TEST-*"
timeRegex="time=\"[0-9]*(\.[0-9]*)*\""
classNameRegex="classname=\"[A-Za-z0-9\.]*\""
nameRegex="name=\"[A-Za-z0-9_]*\""
testCases = []
baseDirectory = '.'

def main():
	changeDirectory()
	files = findFiles()
	readFiles(files)
	testCases = sortTestCases()
	testCases.reverse()
	for item in testCases:
		print item

def changeDirectory():
	os.chdir(baseDirectory)

#Find all surefire reports in the current directory
def findFiles():
	return glob.glob(filePatternToTest)

#Read each surefire report and pass the content to parseContent method
def readFiles(files):
	for file in files:
		with open(file, "rb") as openedFile:
			content = openedFile.read()
		openedFile.closed
		parseContent(content)

#Find all test cases within the the content passed and add name, class and timings to the testCases array
def parseContent(content):
	matches = re.findall("<testcase .*/>", content)
	for testCase in matches:		
		value = getValues(testCase)
		testCases.append(value)

#Parse a testCase and pull out the classname, time and name of each test
def getValues(testCase):
	timeAttribute = re.search(timeRegex, testCase)
	if timeAttribute != None:
		timeAttribute = timeAttribute.group(0)

	classnameAttribute = re.search(classNameRegex, testCase)
	if classnameAttribute != None:
		classnameAttribute = classnameAttribute.group(0)

	nameAttribute = re.search(nameRegex, testCase)
	if nameAttribute != None:
		nameAttribute = nameAttribute.group(0)

	return tuple([timeAttribute, classnameAttribute, nameAttribute])

def sortTestCases():
	return sorted(testCases, key=lambda row: row[0])

#Parse arguments
parser = argparse.ArgumentParser(description="Find the longest running maven tests.")
parser.add_argument('-d', help='Base directory to find the unit tests', required=False, action='store', default='.', dest='baseDirectory')
arguments = parser.parse_args()
baseDirectory = arguments.baseDirectory

main()
