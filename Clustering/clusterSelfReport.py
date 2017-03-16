import os
import pandas as pd
from os import listdir
from os.path import isfile, join
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import csv
import numpy as np


# Age
# Gender
# Control / Depressed / Anxious


def writeToCSV(ID,data):
	"""creates a file for the individual"""
	# write to file
	# make file name be person's ID
	if (os.path.exists(ID + ".csv")):
		data.to_csv(ID + ".csv", mode='a', index=False, header=False)
	else:
		data.to_csv(ID + ".csv", index=False, header=True)

def csvToDataFrame(path_to_file):
    csvData = []
    data = open(path_to_file).readlines()
    for row in data:
        row = [x.rstrip() for x in row.split('\t')]
        row = [x.strip('"') for x in row]
        if row != ['']:
            csvData.append(row)
    return pd.DataFrame(csvData)

def clusterAge(path_to_file):
	"""Takes the file with all of the features and creates a new files based on the year of birth for an individual"""
	data = open(path_to_file)
	temp = []
	# quartiles for bins: ['49', '69', '78', '84', '97']
	quartileAge1 = []
	quartileAge2 = []
	quartileAge3 = []
	quartileAge4 = []
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	quartileAge1.append(firstRow)
	quartileAge2.append(firstRow)
	quartileAge3.append(firstRow)
	quartileAge4.append(firstRow)
	# keep track of the number of year for an individual
	year = 0
	for row in data.readlines():
		# row = row.split(',')
		row = [x.rstrip() for x in row.split(',')]
		# ID number is in 3rd column, index 2
		currID = row[2]
		if prevID == currID:
			# add to dataframe to write to csv
			temp.append(row)
			# increase the number of year that participant spent in the study
		if prevID != currID:
			# figure out the number of year for this individual by looking at the selfReport csv file
			year = int(searchSelfReport(prevID))
			if year >= 49 and year < 69:
				quartileAge1.extend(temp)
			if year >= 69 and year < 78:
				quartileAge2.extend(temp)
			if year >= 78 and year < 84:
				quartileAge3.extend(temp)
			if year >= 84 and year <= 97:
				quartileAge4.extend(temp)
			# reset the temporary array that keeps track of individual data
			temp = []
			# update prevID
			prevID = currID
			# add first day of the next individual
			temp.append(row)
	# create new personalized csv
	df = pd.DataFrame(quartileAge1)
	df.columns = header
	writeToCSV('quartileAge1',df)
	# create new personalized csv
	df = pd.DataFrame(quartileAge2)
	df.columns = header
	writeToCSV('quartileAge2',df)
	# create new personalized csv
	df = pd.DataFrame(quartileAge3)
	df.columns = header
	writeToCSV('quartileAge3',df)
	# create new personalized csv
	df = pd.DataFrame(quartileAge4)
	df.columns = header
	writeToCSV('quartileAge4',df)

def searchSelfReport(ID):
	data = open('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/CS120Clinical/CS120GroupLabels_BasicDemosSimple.csv')
	for row in data.readlines():
		row = [x.rstrip() for x in row.split(',')]
		if row[0] == ID:
			# return the year of birth for 
			return row[6].split('-')[2]

def quartileDOB(path_to_file):
	"""find the edges for the different quartileDOB for the average number of touches"""
	# Min, first quartileDOB, median, third quartileDOB, max
	quartileDOB = [0,0,0,0,0]
	"""Takes the file with all of the features and creates a new files based on the number of numTouches of data for an individual"""
	data = open(path_to_file)
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	dob = []
	for row in data.readlines():
		row = [x.rstrip() for x in row.split(',')]
		year = row[6].split('-')[2]
		dob.append(year)
	dob.sort()
	quartileDOB[0] = min(dob)
	quartileDOB[1] = dob[len(dob)//4]
	quartileDOB[2] = dob[len(dob)//2]
	quartileDOB[3] = dob[(len(dob)//4)*3]
	quartileDOB[4] = max(dob)
	return quartileDOB
	# ['49', '69', '78', '84', '97']

def searchSelfReport2(ID):
	data = open('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/CS120Clinical/CS120GroupLabels_BasicDemosSimple.csv')
	for row in data.readlines():
		row = [x.rstrip() for x in row.split(',')]
		if row[0] == ID:
			# return the mental state and gender
			return [row[1],row[2],row[3],row[4],row[5]]

def clusterSelfReport(path_to_file):
	"""Takes the file with all of the features and creates a new files based on the year of birth for an individual"""
	temp = []
	all_female = []
	all_male = []
	all_control = []
	all_anxious = []
	all_depressed = []
	all_depressedAndAnxious = []
	data = open(path_to_file)
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	all_female.append(firstRow)
	all_male.append(firstRow)
	all_control.append(firstRow)
	all_anxious.append(firstRow)
	all_depressed.append(firstRow)
	all_depressedAndAnxious.append(firstRow)
	for row in data.readlines():
		# row = row.split(',')
		row = [x.rstrip() for x in row.split(',')]
		# ID number is in 3rd column, index 2
		currID = row[2]
		if prevID == currID:
			# add to dataframe to write to csv
			temp.append(row)
			# increase the number of year that participant spent in the study
		if prevID != currID:
			# figure out the number of year for this individual by looking at the selfReport csv file
			[control,anxious,depressed,depressedAndAnxious,gender] = searchSelfReport2(prevID)
			if gender == 'Female':
				all_female.extend(temp)
			elif gender == 'Male':
				all_male.extend(temp)
			if control:
				all_control.extend(temp)
			elif anxious:
				all_anxious.extend(temp)
			elif depressed:
				all_depressed.extend(temp)
			elif depressedAndAnxious:
				all_depressedAndAnxious.extend(temp)
			# reset the temporary array that keeps track of individual data
			temp = []
			# update prevID
			prevID = currID
			# add first day of the next individual
			temp.append(row)
	# create new personalized csv
	df = pd.DataFrame(all_female)
	df.columns = header
	writeToCSV('all_female',df)
	# create new personalized csv
	df = pd.DataFrame(all_male)
	df.columns = header
	writeToCSV('all_male',df)
	# create new personalized csv
	df = pd.DataFrame(all_control)
	df.columns = header
	writeToCSV('all_control',df)
	# create new personalized csv
	df = pd.DataFrame(all_anxious)
	df.columns = header
	writeToCSV('all_anxious',df)
	# create new personalized csv
	df = pd.DataFrame(all_depressed)
	df.columns = header
	writeToCSV('all_depressed',df)
	# create new personalized csv
	df = pd.DataFrame(all_depressedAndAnxious)
	df.columns = header
	writeToCSV('all_depressedAndAnxious',df)

def main(path_to_file):
	# removeLightMissing(path_to_file)
	# removeWifiMissing(path_to_file)
	# removeAllThreeMissing(path_to_file)
	# selfReportDf = csvToDataFrame('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/CS120Clinical/CS120GroupLabels_BasicDemos.xlsx')
	# clusterAge(path_to_file)
	clusterSelfReport(path_to_file)

main('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/mHealth-PurpleRobot/all.csv')
# print(quartileDOB('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/CS120Clinical/CS120GroupLabels_BasicDemosSimple.csv'))

