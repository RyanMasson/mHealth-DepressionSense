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

def removeAppMissing(path_to_file):
	"""Creates two new csv files, one only with app data that exists and one without"""
	data = open(path_to_file)
	csvDataMissingApp = []
	csvDataRest = []
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	csvDataMissingApp.append(firstRow)
	csvDataRest.append(firstRow)
	for row in data.readlines():
		row = [x.rstrip() for x in row.split(',')]
		if row[10:30] == ['-1']*20:
			print("app.csv doesn't exist")
			csvDataMissingApp.append(row)
		else:
			print("app.csv exists")
			csvDataRest.append(row)
	# create new csv with everyone who didn't have app.csv
	df = pd.DataFrame(csvDataMissingApp)
	df.columns = header
	writeToCSV('allNoApp',df)
	# create new csv for everyone who has app.csv
	df = pd.DataFrame(csvDataRest)
	df.columns = header
	writeToCSV('allWithApp',df)

def removeAllMissing(path_to_file):
	"""Creates two new csv files, one only where there is no missing data and one where there is"""
	data = open(path_to_file)
	csvDataMissing = []
	csvDataNoMissing = []
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	csvDataMissing.append(firstRow)
	csvDataNoMissing.append(firstRow)
	for row in data.readlines():
		row = [x.rstrip() for x in row.split(',')]
		if '-1' in row:
			print("missing data")
			csvDataMissing.append(row)
		else:
			print("no missing data")
			csvDataNoMissing.append(row)
	# create new csv with everyone who didn't have app.csv
	df = pd.DataFrame(csvDataMissing)
	df.columns = header
	writeToCSV('csvDataMissing',df)
	# create new csv for everyone who has app.csv
	df = pd.DataFrame(csvDataNoMissing)
	df.columns = header
	writeToCSV('csvDataNoMissing',df)

def removeWifiMissing(path_to_file):
	"""Creates two new csv files, one only with wifi data that exists and one without"""
	data = open(path_to_file)
	allMissingWifi = []
	allNotMissingWifi = []
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	print(header[49])
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	allMissingWifi.append(firstRow)
	allNotMissingWifi.append(firstRow)
	for row in data.readlines():
		row = [x.rstrip() for x in row.split(',')]
		if row[50] == '-1':
			print("wifi.csv doesn't exist")
			allMissingWifi.append(row)
		else:
			print("wifi.csv exists")
			allNotMissingWifi.append(row)
	# create new csv with everyone who didn't have app.csv
	df = pd.DataFrame(allMissingWifi)
	df.columns = header
	writeToCSV('allMissingWifi',df)
	# create new csv for everyone who has app.csv
	df = pd.DataFrame(allNotMissingWifi)
	df.columns = header
	writeToCSV('allNotMissingWifi',df)

def removeLightMissing(path_to_file):
	"""Creates two new csv files, one only with wifi data that exists and one without"""
	data = open(path_to_file)
	allMissingLight = []
	allNotMissingLight = []
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	allMissingLight.append(firstRow)
	allNotMissingLight.append(firstRow)
	for row in data.readlines():
		row = [x.rstrip() for x in row.split(',')]
		if row[49] == '-1':
			print("lgt.csv doesn't exist")
			allMissingLight.append(row)
		else:
			print("lgt.csv exists")
			allNotMissingLight.append(row)
	# create new csv with everyone who didn't have app.csv
	df = pd.DataFrame(allMissingLight)
	df.columns = header
	writeToCSV('allMissingLight',df)
	# create new csv for everyone who has app.csv
	df = pd.DataFrame(allNotMissingLight)
	df.columns = header
	writeToCSV('allNotMissingLight',df)

def removeAllThreeMissing(path_to_file):
	"""Creates new csv files depending on missing data , one only with wifi data that exists and one without"""
	data = open(path_to_file)
	# all_no_app = []
	# all_no_wifi = []
	# all_no_light = []
	all_no_app_wifi_light = []
	all_rest = []
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	# print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	all_no_app_wifi_light.append(firstRow)
	all_rest.append(firstRow)
	for row in data.readlines():
		row = [x.rstrip() for x in row.split(',')]
		# if row[10:30] == ['-1']*20:
		# 	print("app.csv doesn't exist")
		# 	all_no_app.append(row)
		# if row[50] == '-1':
		# 	print("wifi.csv doesn't exist")
		# 	all_no_wifi.append(row)
		# if row[49] == '-1':
		# 	print("lgt.csv doesn't exist")
		# 	all_no_light.append(row)
		if row[49] != '-1' and row[50] != '-1' and row[10:30] != ['-1']*20:
			print("all_rest")
			all_rest.append(row)
		else:
			print("all_no_app_wifi_light")
			all_no_app_wifi_light.append(row)
	# # create new csv with everyone who didn't have app.csv
	# df = pd.DataFrame(all_no_app)
	# df.columns = header
	# writeToCSV('all_no_app',df)
	# # create new csv for everyone who did't have wifi.csv
	# df = pd.DataFrame(all_no_wifi)
	# df.columns = header
	# writeToCSV('all_no_wifi',df)
	# # create new csv with everyone who didn't have lgt.csv
	# df = pd.DataFrame(all_no_light)
	# df.columns = header
	# writeToCSV('all_no_light',df)
	# create new csv for everyone who is missing app, wifi, and light data
	df = pd.DataFrame(all_no_app_wifi_light)
	df.columns = header
	writeToCSV('all_no_app_wifi_light',df)	
	# create new csv for everyone who has the above three
	df = pd.DataFrame(all_rest)
	df.columns = header
	writeToCSV('all_rest',df)

def removeTouchesMissing(path_to_file):
	"""Creates two new csv files, one only with touches data that exists and one without"""
	data = open(path_to_file)
	allMissingTouches = []
	allNotMissingTouches = []
	row = data.readline()
	header = [x.rstrip() for x in row.split(',')]
	print(header)
	row = data.readline()
	firstRow = [x.rstrip() for x in row.split(',')]
	# print(firstRow)
	prevID = firstRow[2]
	if firstRow[3] == '-1':
		print("tch.csv doesn't exist")
		allMissingTouches.append(firstRow)
	else:
		print("tch.csv exists")
		allNotMissingTouches.append(firstRow)
	for row in data.readlines():
		row = [x.rstrip() for x in row.split(',')]
		if row[3] == '-1':
			print("tch.csv doesn't exist")
			allMissingTouches.append(row)
		else:
			print("tch.csv exists")
			allNotMissingTouches.append(row)
	# create new csv with everyone who didn't have app.csv
	df = pd.DataFrame(allMissingTouches)
	df.columns = header
	writeToCSV('allMissingTouches',df)
	# create new csv for everyone who has app.csv
	df = pd.DataFrame(allNotMissingTouches)
	df.columns = header
	writeToCSV('allNotMissingTouches',df)

def main(path_to_file):
	# removeLightMissing(path_to_file)
	# removeWifiMissing(path_to_file)
	# removeAllThreeMissing(path_to_file)
	removeTouchesMissing(path_to_file)

main('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/mHealth-PurpleRobot/all.csv')
# lgt_std = header[49]


