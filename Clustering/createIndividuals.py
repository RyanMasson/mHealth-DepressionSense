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

def main(path_to_file):
	"""Takes the file with all of the features and creates a new file for each individual"""
	data = open(path_to_file)
	csvData = []
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	csvData.append(firstRow)
	for row in data.readlines():
		# row = row.split(',')
		row = [x.rstrip() for x in row.split(',')]
		# ID number is in 3rd column, index 2
		currID = row[2]
		if prevID == currID:
			# add to dataframe to write to csv
			csvData.append(row)
		if prevID != currID:
			# create new personalized csv
			df = pd.DataFrame(csvData)
			df.columns = header
			writeToCSV(prevID,df)
			# empty dataframe
			csvData = []
			# update prevID
			prevID = currID
			# add first day of the next individual
			csvData.append(row)

main('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/mHealth-PurpleRobot/all.csv')


