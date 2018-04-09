import csv
import random
import math
import operator
 

def datasetLoadFun(filename, cutset, train=[] , test=[]):
	with open(filename, 'r') as csvfile: # Read the given file, works for numeric data only
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(4):        # Have to change this if number of attributes changes
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < cutset: # Devide the data set into test and train set
	            train.append(dataset[x]) # Random used is not non-deterministic, so everytime elements will change 
	        else:
	            test.append(dataset[x])

	              
def euclideanDistanceFun(point1, point2, length):  # Calculate the Euclidean distance
	distance = 0
	for x in range(length):
		distance += pow((point1[x] - point2[x]), 2)
	return math.sqrt(distance) # return the distance
 


def neighborsCalcFun(train, testcase, k): # Get all the K neighbour distance
	distances = []
	length = len(testcase)-1
	for x in range(len(train)):
		dist = euclideanDistanceFun(testcase, train[x], length)
		distances.append((train[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighborPoint = []
	for x in range(k):
		neighborPoint.append(distances[x][0]) # Append all the neighbours in the range K
	return neighborPoint
 


def sendResponseFun(neighborPoint): # Calculate the majority in the K distance values obtained to classify the data
	classVotes = {}
	for x in range(len(neighborPoint)):
		response = neighborPoint[x][-1]
		if response in classVotes:
			classVotes[response] += 1 #Increment if already key is available
		else:
			classVotes[response] = 1 # Add new key if not present already
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0] # Return ther majnority element after sorting
 


def checkAccuracyFun(test, predictions): #Calculate the accuracy, by comparing it with the original data
	correct = 0
	for x in range(len(test)):
		if test[x][-1] == predictions[x]:
			correct += 1
	print ((correct/float(len(test))) * 100.0) #Calculate the % of successful prediction 
	


def main():
	train=[]
	test=[]
	cutset =0.85 #to split the data set 75% to train , 25% to test it
	datasetLoadFun('iris_data.data', cutset, train, test) # file name changes with each dataset, should be there in same folder as this file
	print('No. of elements in Train Set : ' + repr(len(train))) # Number of elements in the training dataset
	print('No. of elements in Test Set : ' + repr(len(test)))  # Number of elements in the testing dataset
	predictions=[]
	num = [30] #Can be used for multiple K values

	for i in range(len(num)): #Run for each K
		for x in range(len(test)): #Run for each element in test
				neighborPoint = neighborsCalcFun(train, test[x], num[i])
				result = sendResponseFun(neighborPoint)
				predictions.append(result)
		print(num[i])#Print the current K value, when multiple values are used
		accuracy = checkAccuracyFun(test, predictions)#Compare with original dataset to get the accuracy 

main()