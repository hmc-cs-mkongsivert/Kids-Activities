import requests
import csv
import datetime as dt
import calendar as cal

def between(string, start, beginTag, endTag):
	'''resturns a substring between two tags'''
	begin = string.find(beginTag, start) + len(beginTag)
	end = string.find(endTag, begin)
	return string[begin:end]

def removeWhitespace(string):
	'''as one might expect, removes all the whitespace from a given string'''
	newString = ''.join([i for i in string if (i != '\t' and i != '\n')])
	return newString

def removeTag(string, tag, middle = True, neg = False):
	'''removes extraneous tags'''
	leftBeg = string.find("<" + tag)
	leftEnd = string.find(">", leftBeg)
	right = string.find("</" + tag + ">", leftEnd)
	if middle:
		#just remove the tags
		return string[0:leftBeg] + string[leftEnd+1:right] + string[right+len(tag)+3:]
	elif (not neg):
		#remove the tags and tagged material
		return string[0:leftBeg] + string[right+len(tag)+3:]
	else:
		#remove everything but the tagged material
		return string[leftEnd+1:right]

def makeIndicesList(siteText, searchTerm):
	'''returns a list of indices of events in a given site text'''
	s = 0
	indices = []
	while True:
		newI = siteText.find(searchTerm, s)
		if newI == -1:
			break
		s = newI + len(searchTerm)
		indices.append(newI)

	return indices

def exhibitions(schedule, begDate, endDate):
	'''takes in a museum schedule and starting and ending dates for an
	exhibition and returns a list of the dates and times when the exhibition
	will be open'''
	allDates = []
	date = begDate
	while date <= endDate:
		if schedule[date.weekday()] != None:
			begTime = dt.combine(date, schedule[date.weekday()][0])
			endTime = dt.combine(date, schedule[date.weekday()][1])
			allDates.append((begTime, endTime))
		date += dt.timedelta(days=1)
	return allDates

def findMonth(dString):
	'''takes in a string representing a date and returns the month that
	that date is in'''
	months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
	
	month = 0
	for i in range(len(months)):
		if months[i] in dString.lower():
			month = i + 1
			break
	return month

def parseDate(dString):
	'''takes in a string representing a date and returns a datetime object
	representing that same date'''
	now = dt.datetime.now()
	year = 0
	date = 0
	
	month = findMonth(dString)
	nums = ''.join([i for i in dString if i.isdigit()])
	if len(nums) <= 2:
		date = int(nums)
		year = now.year if (month >= now.month) else (now.year + 1)
	elif str(now.year) in nums:
		date = int(nums.replace(str(now.year), ''))
		year = now.year
	elif str(now.year+1) in nums:
		date = int(nums.replace(str(now.year+1), ''))
		year = now.year+1
	elif str(now.year-1) in nums:
		date = int(nums.replace(str(now.year-1), ''))
		year = now.year-1
	return dt.date(year, month, date)

def parseTime(tString):
	'''takes in a string representing a time and returns a datetine object
	representing that same date'''
	clean = ''.join([i for i in tString if (i.isdigit() or i.isalpha())])

def sortByDate(table):
	'''merge sort of a table by date'''
	if len(table) <= 1:
		return table
	half = len(table)/2
	firstHalf = sortByDate(table[0:half])
	secondHalf = sortByDate(table[half:])
	sortedL = []
	for i in range(len(table)):
		if firstHalf[0][1] <= secondHalf[0][1]:
			sortedL += [firstHalf[0]]
			firstHalf = firstHalf[1:]
		else:
			sortedL +=[secondHalf[0]]
			secondHalf = secondHalf[1:]
	return sortedL

def blindWhinoScrape():
	site = requests.get("https://www.swartsclub.org/art-annex/")
	siteText = removeWhitespace(site.text)
	indices = makeIndicesList(siteText, 'sqs-block html-block sqs-block-html')

	BWSchedule = [None, None, (dt.time(17), dt.time(20)), None, None, (dt.time(12), dt.time(17)), (dt.time(12), dt.time(17))]

	table = []
	for i in [0]+indices[:-1]:
		title = between(siteText, i, '<h3>', '</h3>')
		timeRough = between(siteText, i, '</h3><h3>', '</h3>')
		interval = timeRough.split('-')
		if len(interval) == 1:
			month = findMonth(timeRough)
			year = int(''.join([i for i in timeRough if i.isdigit()]))
			#the first and last days of that particular month
			firstDay = dt.date(year, month, 1)
			lastDay = dt.date(year, month, cal.monthrange(year,month)[1])
			dates = (firstDay, lastDay)
		else:
			interval[0] += interval[1][-4:]
			dates = (parseDate(interval[0]), parseDate(interval[1]))
		location = "The Blind Whino Art Annex"
		details = between(siteText, i, '<p>', '</p>')
		table.append([title, dates, location, details])

	return table

def newseumScrape():
	site = requests.get("http://www.newseum.org/events-programs/")
	siteText = removeWhitespace(site.text)
	indices = makeIndicesList(siteText, '"ai1ec-event"')

	table = []
	for i in [0]+indices[:-1]:
		title = between(siteText, i, '<span class="ai1ec-event-title">', '</span>')
		time = between(siteText, i, '<div class="ai1ec-event-time">', '</div>')
		time = removeTag(time, "span", middle = False)
		location = "Newseum, " + between(siteText, i, '<span class="ai1ec-event-location">', '</span>')
		details = between(siteText, i, '<div class="ai1ec-popup-excerpt">', '</div>')
		table.append([title, time, location, details])

	return table

def phillipsScrape():
	site = requests.get("http://www.phillipscollection.org/events?type=all")
	siteText = removeWhitespace(site.text)
	indices = makeIndicesList(siteText, '<div class="field-event-date-range">')

	table = []
	for i in [0]+indices[:-1]:
		title = between(siteText, i, '<h2 class="delta a">', '</h2>')
		title = removeTag(title, "strong")
		time = between(siteText, i, '<div class="field-event-date-range">', '</div>')
		location = "The Phillips Collection"
		details = '<a href = "https://www.phillipscollection' + between(title, 0, '<a href="', '>') + '>Click here for more details</a>'
		title = removeTag(title, "a", False, True)
		table.append([title, time, location, details])
	
	return table

def politicsProseScrape():
	site = requests.get("https://www.politics-prose.com/events")
	siteText = removeWhitespace(site.text)
	indices = makeIndicesList(siteText, 'views-field-field-date')

	table = []
	for i in [0]+indices[:-1]:
		title = between(siteText, i, '<div class="views-field views-field-title">', '</div>')
		time = between(siteText, i, '<div class="views-field views-field-field-date-1">', '</div>')
		time = removeTag(time, "span") #not sure if this will do anything
		location = "Politics and Prose Bookstore"
		details = '<a href = "https://www.politics-prose.com' + between(title, 0, '<a href="', '>') + '>Click here for details</a>'
		title = removeTag(title, "a", False, True)
		table.append([title, time, location, details])

	return table

def tudorScrape():
	site = requests.get("https://www.tudorplace.org/programs/")
	siteText = removeWhitespace(site.text)
	indices = makeIndicesList(siteText, '<td class="thumb">')
	moMarker = '<td colspan="3"><h5>'
	moIndices = makeIndicesList(siteText, moMarker)

	table = []
	mo = 0
	for i in [0]+indices[:-1]:
		if i > moIndices[mo+1]:
			mo += 1
		month = between(siteText, moIndices[mo], moMarker, '</h5>')
		date = between(siteText, i, '</small><big>', '</big>')
		title = between(siteText, i, '<h4>', '</h4>')
		title = removeTag(title, "a")
		time = date + month #TODO: add time of day
		location = "Tudor Place Historic House and Garden"
		details = '<a href = https://www.tudorplace.org/programs' + between(siteText, i, '<a href="', '>') + '>Click here for more details</a>'
		table.append([title, time, location, details])
	return table

def writeCSV():
	'''gathers all of the data and packs them into a CSV file'''
	with open('events.csv', 'w', newline='') as csvfile:
		eventFile = csv.writer(csvfile)
		eventTable = blindWhinoScrape()
#		eventTable += newseumScrape()
#		eventTable += politicsProseScrape()
#		eventTable += phillipsScrape()
#		eventTable += tudorScrape()
		for event in eventTable:
			eventFile.writerow(event)

writeCSV()