import time
START_TIME = time.time()
import sys
import pandas as pd
import json

#sys.setrecursionlimit(1000000)

def returnKey(person,day):
	return "N"+str(person)+"_"+str(day)

def verifysolandscore(solution,N,D,M,A,E,S,T):
	if(len(solution.keys())==0):
		print("No sol verified")
		return 0
	score = 0
	for day in range(D):
		cnt = {'E':0,'M':0,'A':0,'R':0}
		for nurse in range(N):
			assign = solution[returnKey(nurse,day)]
			cnt[assign] += 1
			if(nurse < S):
				#print(assign)
				if(assign == 'M' or assign == 'E'):
					score += 1
		if(cnt['M'] != M):
			print("Day",day,":Morning constraint",sep = "")
			return score
		if(cnt['E'] != E):
			print("Day",day,":Evening constraint",sep = "")
			return score
		if(cnt['A'] != A):
			print("Day",day,":Afternoon constraint",sep = "")
			return score
	for nurse in range(N):
		for day in range(D):
			if(day%7 == 6):
				atleast = 0
				for temp in range(7):
					if(solution[returnKey(nurse,day-temp)] == 'R'):
						atleast = 1
				if(atleast == 0):
					print("Nurse",nurse,"day",day,"No rest week",sep = "")
					return score
			if(day > 0):
				assign = solution[returnKey(nurse,day)]
				if(assign == 'M'):
					assignlast = solution[returnKey(nurse,day-1)]
					if(assignlast == 'M' or assignlast == 'E'):
						print("ME constraint for ",nurse,"on",day,sep = "")
						return score
	#print("Solution Verified")
	#print(score)
	return score

def returnAllowedValues(solution,person,day,people,mTotal,aTotal,eTotal,S,cntdict,alpha,beta):
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

	if(alpha > 1 and person < S):
		mrem *= alpha
		erem *= alpha
	elif(person>=S and beta>1):
		mrem = mrem/beta
		erem = erem/beta

	k = day%7
	had_rest = 0
	for i in range(k):
		if(solution[returnKey(person,day-1 - i)] == 'R'):
			had_rest = 1
	if(had_rest == 0):
		rrem *= pow(1.2,day%7)
	if(had_rest == 1):
		rrem /= 2

	d = {'M':mrem,'E':erem,'A':arem,'R':rrem}

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
	
def returnSortedInDomain(solution,people,day,S):
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
		if x<S:
			return domainSize[x] - 0.5
		else:
			return domainSize[x]

	newDomain = sorted(newDomain,key = func)
	return newDomain

def recursiveBackTracking(solution,people,days,mTotal,aTotal,eTotal,S,T,person,day,cntdict,domain,alpha,beta):

	if(len(solution.keys())==people*days):
		return solution

	if(T!=0 and (T-(time.time() - START_TIME))<0.002):
		print('Terminated in time allowed')
		sys.exit()

	if(len(domain)==0):
		domain = returnSortedInDomain(solution,people,day,S)
	
	person = domain[0]
	domain = domain[1:]

	possibleValuesList = returnAllowedValues(solution,person,day,people,mTotal,aTotal,eTotal,S,cntdict,alpha,beta)

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
				solution2 = recursiveBackTracking(solution,people,days,mTotal,aTotal,eTotal,S,T,0,day+1,cntdict,[],alpha,beta)
			else:
				solution2 = recursiveBackTracking(solution,people,days,mTotal,aTotal,eTotal,S,T,0,day,cntdict,domain,alpha,beta)	

			if(len(solution2.keys())!=0):
				return solution2
		
		del solution[returnKey(person,day)]
		cntdict[day][value] -= 1
	
	return {}

def recursiveBackTracking2(solutionInit,people,days,mTotal,aTotal,eTotal,S,T,person,day,cntdict,domain,alpha,beta,outputfilename):
	st0 = START_TIME
	en = time.time()
	alpha = 1
	beta = 1
	max_score = 0
	while(T - (en-st0) > 0.02 and alpha<people and beta < people):
		solution = {}

		domain = [i for i in range(0,people)]
		solution = recursiveBackTracking({},people,days,mTotal,aTotal,eTotal,S,T,0,0,{},domain,alpha,beta)
		#print(solution)
		alpha += 0.2
		if(alpha > people):
			beta += 0.2
			alpha = 1
		score = verifysolandscore(solution,df.iloc[testCase]['N'],df.iloc[testCase]['D'],df.iloc[testCase]['m'],df.iloc[testCase]['a'],df.iloc[testCase]['e'],S,T)
		if(score > max_score and len(solution.keys())!=0):
			file = open(outputfilename,"w")
			json.dump(solution,file)
			file.close()
			max_score = score
			print(max_score)
		en = time.time()
	return solution

def checkSolExists(N,D,M,A,E):
	if(M+A+E>N):
		return False
	if(D>6 and (N-M-A-E)*7<N):
		return False
	if((N-M-E)<M):				#No possible assignment for M on the next day
		return False
	return True

if __name__=='__main__':
	csv_filename = sys.argv[1]
	df = pd.read_csv(csv_filename)

	file = open("solution.json","w")
	json.dump({},file)				# In case of non convergence
	file.close()

	testCase = 0			#Only one test case per file
	domain = [i for i in range(0,df.iloc[testCase]['N'])]
	#st = time.time()

	if (not checkSolExists(df.iloc[testCase]['N'],df.iloc[testCase]['D'],df.iloc[testCase]['m'],df.iloc[testCase]['a'],df.iloc[testCase]['e'])):
		solution = {}
	elif('S' not in df.iloc[testCase]):
		solution = recursiveBackTracking({},df.iloc[testCase]['N'],df.iloc[testCase]['D'],df.iloc[testCase]['m'],df.iloc[testCase]['a'],df.iloc[testCase]['e'],0,0,0,0,{},domain,1,1)
		verifysolandscore(solution,df.iloc[testCase]['N'],df.iloc[testCase]['D'],df.iloc[testCase]['m'],df.iloc[testCase]['a'],df.iloc[testCase]['e'],0,0)
	else:
		solution = recursiveBackTracking2({},df.iloc[testCase]['N'],df.iloc[testCase]['D'],df.iloc[testCase]['m'],df.iloc[testCase]['a'],df.iloc[testCase]['e'],df.iloc[testCase]['S'],df.iloc[testCase]['T'],0,0,{},domain,1,1,"solution.json")
	
	if(len(solution.keys())!=0):
		file = open("solution.json","w")
		json.dump(solution,file)
		file.close()
	en = time.time()

	#print(en-st)
	print(en-START_TIME)