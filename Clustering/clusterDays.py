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

def clusterNumDays(path_to_file):
	"""Takes the file with all of the features and creates a new files based on the number of days of data for an individual"""
	data = open(path_to_file)
	temp = []
	# quartiles for bins: [7, 47, 50, 56, 137]
	quartile1 = []
	quartile2 = []
	quartile3 = []
	quartile4 = []
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	quartile1.append(firstRow)
	quartile2.append(firstRow)
	quartile3.append(firstRow)
	quartile4.append(firstRow)
	# keep track of the number of days for an individual
	days = 0
	for row in data.readlines():
		# row = row.split(',')
		row = [x.rstrip() for x in row.split(',')]
		# ID number is in 3rd column, index 2
		currID = row[2]
		if prevID == currID:
			# add to dataframe to write to csv
			temp.append(row)
			# increase the number of days that participant spent in the study
			days += 1
		if prevID != currID:
			# figure out the number of days for this individual
			if days >= 7 and days < 47:
				quartile1.extend(temp)
			if days >= 47 and days < 50:
				quartile2.extend(temp)
			if days >= 50 and days < 56:
				quartile3.extend(temp)
			if days >= 56 and days <= 137:
				quartile4.extend(temp)
			# reset the number of days
			days = 0
			# reset the temporary array that keeps track of individual data
			temp = []
			# update prevID
			prevID = currID
			# add first day of the next individual
			temp.append(row)
	# create new personalized csv
	df = pd.DataFrame(quartile1)
	df.columns = header
	writeToCSV('quartile1',df)
	# create new personalized csv
	df = pd.DataFrame(quartile2)
	df.columns = header
	writeToCSV('quartile2',df)
	# create new personalized csv
	df = pd.DataFrame(quartile3)
	df.columns = header
	writeToCSV('quartile3',df)
	# create new personalized csv
	df = pd.DataFrame(quartile4)
	df.columns = header
	writeToCSV('quartile4',df)

# clusterNumDays('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/mHealth-PurpleRobot/all.csv')
def quartiles(path_to_file):
	"""find the edges for the different quartiles for the number of days a participants was in a study"""
	# Min, first quartile, median, third quartile, max
	quartiles = [0,0,0,0,0]
	"""Takes the file with all of the features and creates a new files based on the number of days of data for an individual"""
	data = open(path_to_file)
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	# keep track of the number of days for an individual
	daysAll = []
	days = 0
	for row in data.readlines():
		# row = row.split(',')
		row = [x.rstrip() for x in row.split(',')]
		# ID number is in 3rd column, index 2
		currID = row[2]
		if prevID == currID:
			# increase the number of days that participant spent in the study
			days += 1
		if prevID != currID:
			if days > 100:
				print(prevID)
			daysAll.append(days)
			# reset the number of days
			days = 1
			# update prevID
			prevID = currID
	daysAll.sort()
	quartiles[0] = min(daysAll)
	quartiles[1] = daysAll[len(daysAll)//4]
	quartiles[2] = daysAll[len(daysAll)//2]
	quartiles[3] = daysAll[(len(daysAll)//4)*3]
	quartiles[4] = max(daysAll)
	return quartiles

clusterNumDays('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/mHealth-PurpleRobot/all.csv')
# print(quartiles('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/mHealth-PurpleRobot/all.csv'))


