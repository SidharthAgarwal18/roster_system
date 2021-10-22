import sys
import pandas as pd
import json
import time

sys.setrecursionlimit(1000000)

def returnKey(person,day):
	return "N"+str(person)+"_"+str(day)

def returnAllowedValues(solution,person,day,people,mTotal,aTotal,eTotal,cntdict):
	#possibleValues = ['A','R','E','M']

	mThis = 0
	aThis = 0
	eThis = 0
	rThis = 0

	if day in cntdict:
		if 'M' in cntdict[day]:
			mThis = cntdict[day]['M']
		if 'A' in cntdict[day]:
			aThis = cntdict[day]['A']
		if 'E' in cntdict[day]:
			eThis = cntdict[day]['E']
		if 'R' in cntdict[day]:
			rThis = cntdict[day]['R']

	mrem = mTotal - mThis
	arem = aTotal - aThis
	erem = eTotal - eThis
	rrem = people - mTotal - aTotal - eTotal - rThis

	d = {'A':arem,'M':mrem,'E':erem,'R':rrem}

	possibleValues = [k for k, v in sorted(d.items(), key=lambda item: item[1]) if v > 0]
	possibleValues.reverse()
	#print("P",possibleValues,sep = "   ")

	if('M' in possibleValues and day>0 and (solution[returnKey(person,day-1)]=='M' or solution[returnKey(person,day-1)]=='E')):		
		possibleValues.remove('M')			

	if day%7!=6:
		return possibleValues

	temp = 1
	while(temp<=6):
		if(solution[returnKey(person,day-temp)]=='R'):
			return possibleValues
		temp += 1

	if('M' in possibleValues):
		possibleValues.remove('M')
	if('A' in possibleValues):
		possibleValues.remove('A')
	if('E' in possibleValues):
		possibleValues.remove('E')
	return possibleValues

def checkDayConstraint(solution,person,day,people,days,mTotal,aTotal,eTotal,cntdict,lendomain):

	mThis = 0
	aThis = 0
	eThis = 0

	if(lendomain!=0):
		if 'M' in cntdict[day]:
			mThis = cntdict[day]['M']
		if 'A' in cntdict[day]:
			aThis = cntdict[day]['A']
		if 'E' in cntdict[day]:
			eThis = cntdict[day]['E']
		if(mThis>mTotal or aThis>aTotal or eThis>eTotal):
			return False
		return True
	if 'M' in cntdict[day]:
		mThis = cntdict[day]['M']
	if 'A' in cntdict[day]:
		aThis = cntdict[day]['A']
	if 'E' in cntdict[day]:
		eThis = cntdict[day]['E']
	if(mThis==mTotal and aThis==aTotal and eThis==eTotal):
		return True
	return False
	
def returnSortedInDomain(solution,people,day):
	newDomain = []
	domainSize = {}


	for person in range(people):
		thisSize = 4
		
		if(solution[returnKey(person,day-1)]=='E' or solution[returnKey(person,day-1)]=='M'):
			thisSize = 3

		if(day%7==6):
			noR = True
			for temp in range(6):
				if(solution[returnKey(person,day-1-temp)]=='R'):
					noR = False
					break
			if (noR):
				thisSize = 1

		domainSize[person] = thisSize
		newDomain.append(person)

	def func(x):
		return domainSize[x]

	newDomain = sorted(newDomain,key = func)
	return newDomain

def recursiveBackTracking(solution,people,days,mTotal,aTotal,eTotal,person,day,cntdict,domain):

	if(len(solution.keys())==people*days):
		return solution

	if(len(domain)==0):
		domain = returnSortedInDomain(solution,people,day)
	
	person = domain[0]
	domain = domain[1:]

	possibleValuesList = returnAllowedValues(solution,person,day,people,mTotal,aTotal,eTotal,cntdict)

	for value in possibleValuesList:
		
		solution[returnKey(person,day)] = value
		if day in cntdict:
			if value in cntdict[day]:
				cntdict[day][value] += 1
			else:
				cntdict[day][value] = 1
		else:
			cntdict[day] = {value : 1}
		
		if(checkDayConstraint(solution,person,day,people,days,mTotal,aTotal,eTotal,cntdict,len(domain))):
		
		#if(True):
			solution2 = {}

			if(len(domain)==0):
				solution2 = recursiveBackTracking(solution,people,days,mTotal,aTotal,eTotal,0,day+1,cntdict,[])
			else:
				solution2 = recursiveBackTracking(solution,people,days,mTotal,aTotal,eTotal,0,day,cntdict,domain)	

			if(len(solution2.keys())!=0):
				return solution2
		
		del solution[returnKey(person,day)]
		cntdict[day][value] -= 1
	
	return {}

if __name__=='__main__':
	csv_filename = sys.argv[1]
	df = pd.read_csv(csv_filename)
	#print(df.iloc[0]['N'])

	with open("solution.json","w") as file:
		for testCase in range(df.shape[0]):
			domain = [i for i in range(0,df.iloc[testCase]['N'])]

			st = time.time()
			solution = recursiveBackTracking({},df.iloc[testCase]['N'],df.iloc[testCase]['D'],df.iloc[testCase]['m'],df.iloc[testCase]['a'],df.iloc[testCase]['e'],0,0,{},domain)
			en = time.time()
			print(en-st)
			json.dump(solution,file)
			file.write('\n')