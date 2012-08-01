#!/usr/bin/python

import os
import glob
import re

filePatternToTest="TEST-*"
timeRegex="time=\"[0-9]*(\.[0-9]*)*\""
classNameRegex="classname=\"[A-Za-z0-9\.]*\""
nameRegex="name=\"[A-Za-z0-9_]*\""
testCases = []

def main():
	files = findFiles()
	readFiles(files)
	testCases = sortTestCases()
	testCases.reverse()
	for item in testCases:
		print item

def findFiles():
	return glob.glob(filePatternToTest)

def readFiles(files):
	for file in files:
		with open(file, "rb") as openedFile:
			content = openedFile.read()
		openedFile.closed
		parseContent(content)

def parseContent(content):
	matches = re.findall("<testcase .*/>", content)
	for testCase in matches:		
		value = getValues(testCase)
		testCases.append(value)

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

main()
