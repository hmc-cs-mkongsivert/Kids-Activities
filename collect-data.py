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
			begTime = dt.datetime.combine(date, schedule[date.weekday()][0])
			endTime = dt.datetime.combine(date, schedule[date.weekday()][1])
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

def parseTimeHelper(tString):
	num = ''.join([i for i in tString if i.isdigit()])
	time = None
	if len(num) <= 2:
		time = dt.time(int(num))
	else:
		time = dt.time(int(num[:-2]), int(num[-2:]))

	if time < dt.time(7):
		dTime = dt.datetime.combine(dt.datetime.now(), time)
		dTime += dt.timedelta(hours = 12)
		time = dTime.time()
	#TODO: add a.m. and p.m.
	return time

def parseTime(tString):
	'''takes in a string representing a time and returns a datetime object
	representing that same date'''
	tString
	if "–" in tString:
		interval = tString.split('–')
		begin = parseTimeHelper(interval[0])
		end = parseTimeHelper(interval[1])
		return (begin, end)
	else:
		print("get hecked")
		return None

def sortByDate(table):
	'''merge sort of a table by date'''
	if len(table) <= 1:
		return table
	half = len(table)//2
	firstHalf = sortByDate(table[0:half])
	secondHalf = sortByDate(table[half:])
	sortedL = []
	for i in range(len(table)):
		if len(firstHalf) == 0:
			sortedL += [secondHalf[0]]
			secondHalf = secondHalf[1:]
		elif len(secondHalf) == 0:
			sortedL += [firstHalf[0]]
			firstHalf = firstHalf[1:]
		elif firstHalf[0][1][0] <= secondHalf[0][1][0]:
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
		timeRough = between(siteText, i, '</h3><h3>', '</h3><p>')
		if 'h3' in timeRough:
			timeRough = timeRough.split('<h3>')[1]
		interval = timeRough.split('-')
		if len(interval) == 1:
			month = findMonth(timeRough)
			year = int(''.join([i for i in timeRough if i.isdigit()]))
			#the first and last days of that particular month
			firstDay = dt.date(year, month, 1)
			lastDay = dt.date(year, month, cal.monthrange(year,month)[1])
			opening = (firstDay, lastDay)
		else:
			interval[0] += interval[1][-4:]
			opening = (parseDate(interval[0]), parseDate(interval[1]))
		dates = exhibitions(BWSchedule, opening[0], opening[1])
		location = "The Blind Whino Art Annex"
		details = between(siteText, i, '<p>', '</p>')
		for day in dates:
			table.append([title, day, location, details])

	return table

def hirshhornScrape():
	site = requests.get("https://hirshhorn.si.edu/exhibitions-events/")
	siteText = removeWhitespace(site.text)
	exhibs = makeIndicesList(siteText, 'class="list-item-title balance-text"')
	events = makeIndicesList(siteText, 'class="tribe-events-title list-item-title balance-text"')

	table = []
	for i in [0]+exhibs[:-1]:
		title = between(siteText, i, '<h4 class="list-item-title balance-text">', '</h4>')
		time = 'time!'
		location = 'The Hirshhorn Museum and Sculpture Garden'
		details = ''
	for i in [0]+events[:-1]:
		title = between(siteText, i, '<h4 class="tribe-events-title list-item-title balance-text">', '</h4>')
		time = 'time!'
		location = 'The Hirshhorn Museum and Sculpture Garden'
		details = ''

def newseumScrape():
	site = requests.get("http://www.newseum.org/events-programs/")
	siteText = removeWhitespace(site.text)
	indices = makeIndicesList(siteText, '"ai1ec-event"')

	table = []
	for i in [0]+indices[:-1]:
		title = between(siteText, i, '<span class="ai1ec-event-title">', '</span>')
		dtString = between(siteText, i, '<div class="ai1ec-event-time">', '</div>')
		dtString = removeTag(dtString, "span", middle = False)
		where = "Newseum, " + between(siteText, i, '<span class="ai1ec-event-location">', '</span>')
		details = between(siteText, i, '<div class="ai1ec-popup-excerpt">', '</div>')

		date = None
		time = None
		if '@' in dtString:
			dtList = dtString.split('@')
			date = parseDate(dtList[0])
			time = parseTime(dtList[1])
		else:
			date = parseDate(dtString)
			time = (dt.time(9), dt.time(17))
		when = (dt.datetime.combine(date, time[0]), dt.datetime.combine(date, time[1]))
		table.append([title, when, where, details])

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
		time = removeTag(between(siteText, i, '<div class="views-field views-field-field-date-1">', '</div>'), "span")
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
		eventTable += newseumScrape()
#		eventTable += phillipsScrape()
#		eventTable += politicsProseScrape()
#		eventTable += tudorScrape()
		
		print("total table:", len(eventTable))
		sortedTable = sortByDate(eventTable)
		
		for event in eventTable:
			eventFile.writerow(event)

writeCSV()