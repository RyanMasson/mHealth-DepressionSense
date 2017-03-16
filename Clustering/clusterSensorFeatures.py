import os
import pandas as pd
from os import listdir
from os.path import isfile, join
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import csv
import numpy as np

def writeToCSV(ID,data):
	"""creates a file for the individual"""
	# write to file
	# make file name be person's ID
	if (os.path.exists(ID + ".csv")):
		data.to_csv(ID + ".csv", mode='a', index=False, header=False)
	else:
		data.to_csv(ID + ".csv", index=False, header=True)

def clusterSensorFeatures(path_to_file):
	"""Takes the file with all of the features and creates a new files based on the number of numTouches of data for an individual"""
	data = open(path_to_file)
	temp = []
	# quartileTouches for bins: [0, 1180, 2230, 3508, 20849]
	quartileTouches1 = []
	quartileTouches2 = []
	quartileTouches3 = []
	quartileTouches4 = []
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	# keep track of the number of numTouches for an individual
	numTouches = 0
	days = 0
	for row in data.readlines():
		row = [x.rstrip() for x in row.split(',')]
		# ID number is in 3rd column, index 2
		currID = row[2]
		if prevID == currID:
			# add to dataframe to write to csv
			temp.append(row)
			# increase the number of numTouches that participant spent in the study
			numTouches += int(row[3])
			days += 1
		if prevID != currID:
			numTouches = numTouches//days
			# figure out the number of numTouches for this individual
			if numTouches >= 0 and numTouches < 1180:
				quartileTouches1.extend(temp)
			if numTouches >= 1180 and numTouches < 2230:
				quartileTouches2.extend(temp)
			if numTouches >= 2230 and numTouches < 3508:
				quartileTouches3.extend(temp)
			if numTouches >= 3508 and numTouches <= 20849:
				quartileTouches4.extend(temp)
			# reset the number of numTouches
			numTouches = int(row[3])
			days = 1
			# reset the temporary array that keeps track of individual data
			temp = []
			# update prevID
			prevID = currID
			# add first day of the next individual
			temp.append(row)
	# create new personalized csv
	df = pd.DataFrame(quartileTouches1)
	df.columns = header
	writeToCSV('quartileTouches1',df)
	# create new personalized csv
	df = pd.DataFrame(quartileTouches2)
	df.columns = header
	writeToCSV('quartileTouches2',df)
	# create new personalized csv
	df = pd.DataFrame(quartileTouches3)
	df.columns = header
	writeToCSV('quartileTouches3',df)
	# create new personalized csv
	df = pd.DataFrame(quartileTouches4)
	df.columns = header
	writeToCSV('quartileTouches4',df)

# clusterNumnumTouches('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/mHealth-PurpleRobot/all.csv')
def quartileTouches(path_to_file):
	"""find the edges for the different quartileTouches for the average number of touches"""
	# Min, first quartileTouches, median, third quartileTouches, max
	quartileTouches = [0,0,0,0,0]
	"""Takes the file with all of the features and creates a new files based on the number of numTouches of data for an individual"""
	data = open(path_to_file)
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	# keep track of the number of numTouches for an individual
	numTouchesAll = []
	numTouches = 0
	days = 0
	for row in data.readlines():
		# row = row.split(',')
		row = [x.rstrip() for x in row.split(',')]
		# ID number is in 3rd column, index 2
		currID = row[2]
		if prevID == currID:
			# increase the number of numTouches that participant spent in the study
			numTouches += int(row[3])
			days += 1
		if prevID != currID:
			numTouchesAll.append(numTouches//days)
			# reset the number of numTouches
			numTouches = int(row[3])
			days = 1
			# update prevID
			prevID = currID
	numTouchesAll.sort()
	quartileTouches[0] = min(numTouchesAll)
	quartileTouches[1] = numTouchesAll[len(numTouchesAll)//4]
	quartileTouches[2] = numTouchesAll[len(numTouchesAll)//2]
	quartileTouches[3] = numTouchesAll[(len(numTouchesAll)//4)*3]
	quartileTouches[4] = max(numTouchesAll)
	return quartileTouches

clusterSensorFeatures('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/mHealth-PurpleRobot/all.csv')
# print(quartileTouches('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/mHealth-PurpleRobot/allNotMissingTouches.csv'))


