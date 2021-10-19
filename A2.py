import sys
import pandas as pd
import json

def returnKey(person,day):
	return "N"+str(person)+"_"+str(day)

def returnAllowedValues(solution,person,day):
	possibleValues = ['M','A','E','R']

	if(day>0 and (solution[returnKey(person,day-1)]=='M' or solution[returnKey(person,day-1)]=='E')):		
		possibleValues = possibleValues[1:]				#No consec mornings and no morn after evening.

	if day%7!=6:
		return possibleValues

	temp = 1
	while(temp<=6):
		if(solution[returnKey(person,day-temp)]=='R'):
			return possibleValues
		temp += 1

	return ['R']

def checkDayConstraint(solution,person,day,people,days,mTotal,aTotal,eTotal):

	mThis = 0
	aThis = 0
	eThis = 0

	if(person<people-1):

		for thisPerson in range(person+1):
			if(solution[returnKey(thisPerson,day)]=='M'):
				mThis += 1
			if(solution[returnKey(thisPerson,day)]=='A'):
				aThis += 1
			if(solution[returnKey(thisPerson,day)]=='E'):
				eThis += 1

		if(mThis>mTotal or aThis>aTotal or eThis>eTotal):
			return False
		
		return True

	for thisPerson in range(people):

		if(solution[returnKey(thisPerson,day)]=='M'):
			mThis += 1
		if(solution[returnKey(thisPerson,day)]=='A'):
			aThis += 1
		if(solution[returnKey(thisPerson,day)]=='E'):
			eThis += 1

	if(mThis==mTotal and aThis==aTotal and eThis==eTotal):
		return True
	return False


def recursiveBackTracking(solution,people,days,mTotal,aTotal,eTotal,person,day):

	if(len(solution.keys())==people*days):
		return solution
	possibleValuesList = returnAllowedValues(solution,person,day)

	for value in possibleValuesList:
		solution[returnKey(person,day)] = value
		if(checkDayConstraint(solution,person,day,people,days,mTotal,aTotal,eTotal)):

			if(person==people-1):
				solution2 = recursiveBackTracking(solution,people,days,mTotal,aTotal,eTotal,0,day+1)
			else:
				solution2 = recursiveBackTracking(solution,people,days,mTotal,aTotal,eTotal,person+1,day)			

			if(len(solution2.keys())!=0):
				return solution2
	
	return {}

if __name__=='__main__':
	csv_filename = sys.argv[1]
	df = pd.read_csv(csv_filename)
	#print(df.iloc[0]['N'])

	with open("solution.json","w") as file:
		for testCase in range(df.shape[0]):
			solution = recursiveBackTracking({},df.iloc[testCase]['N'],df.iloc[testCase]['D'],df.iloc[testCase]['m'],df.iloc[testCase]['a'],df.iloc[testCase]['e'],0,0)
			json.dump(solution,file)
			file.write('\n')