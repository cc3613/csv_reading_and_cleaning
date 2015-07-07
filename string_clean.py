#1) string cleaning: taking the raw strings and express in human readable manner
#with normal spacing.

#2) Code swapping: taking state_abbreviations.csv and swap all abbreviations of states
#to actual names

#3) regularize the date format, eliminate the incomplete or bad dates

#assumption: the program and the raw files are in the same folder, to simplify the
#navigating task. Also, assuming the files already exist (no checking done here).

import csv, re, datetime, calendar

#funciton for cleaning the lines
def line_clean(line):
	#split the words and recombine by a single space
	words=line.split()
	words=' '.join(words)
	return words

#function for swapping states from abbreviaton to actual name
def state_swap(state, state_list):
	for row in state_list:
		if state in row:
			#return the actual name (stored in [1] element of each row) when there's
			#a match
			return row[1]

#function for start_date explanation
def start_date(date, new_date):
	#stripping the space, comma, etc.
	observation=re.split('\s|-|\/|/r|,\s',date)
	#valid dates should have length of 3
	if len(observation)!=3:
		return 'Invalid'
	else:
		#3 different possible formats, each with different operation
		#first format (MM/DD/YYYY)
		#eliminate the non-date format but len=3 first, since all 3 formats
		#have numbers for middle element, use that for test.
		#assumption: natural languages do not contain numbers for that element.
		try:
			int(observation[1])
			if len(observation[0])==2:
				return observation[2]+'-'+observation[0]+'-'+observation[1]
			else:
				#second format(YYYY/MM/DD)
				try:
					int(observation[0])	
					return observation[0]+'-'+observation[1]+'-'+observation[2]
				#thrid format (Month Day, Year)
				except ValueError:
					mon_name=dict((v,k) for k,v in enumerate(calendar.month_name))
					
					return observation[2]+'-'+str(mon_name[observation[0]])+'-'+observation[1]
		except ValueError:
			return 'Invalid'

#opening and reading the csv files
with open('test.csv', 'rb') as Q1_raw:
	#using csv reader to store all cells into lists in an organized way, separated
	#by ','
	csvreader=csv.reader(Q1_raw, delimiter=',')
	#skips header
	next(csvreader, None)
	
	#state list place holder
	state_list=[]
	#reading the 'state_abbreviations.csv' and extract values
	with open('state_abbreviations.csv', 'rb') as states:
		state_reader=csv.reader(states, delimiter=',')
		for row in state_reader:
			state_list.append(row)

	#create a new list to store cleaned bio
	new_bio=[]
	#create a new list for storing state names
	new_state=[]
	#create a new list for storing start_date for processing
	new_date=[]
	#craete output csv file
	solution=open('solution.csv', 'wb')
	wr = csv.writer(solution, dialect='excel')
	#write headers
	wr.writerow(['name', 'gender','birthdate', 'address', 'city', 'state', 'zipcode', 'email', 'bio', 'job', 'start_date', 'start_date_description'])
	
	for row in csvreader:
		#copy most of the elements in the test.csv file while cleaning the others
		
		#6th element([5]) is the state abbreviation, extracting this to do string
		#comparison with state_list
		
		#9th element (using 8 as it starts at 0) is the string that needs to be cleaned.
		#after cleaning, store the string into the list 'new_bio'

		#extracting start_date from row[10]
		wr.writerow([row[0], row[1], row[2], row[3], row[4],state_swap(row[5], state_list), row[6], row[7], line_clean(row[8]), row[9],row[10],start_date(row[10], new_date)])

	solution.close()


