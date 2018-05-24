import requests
import csv
import datetime

def between(string, start, beginTag, endTag):
	'''resturns a substring between two tags'''
	begin = string.find(beginTag, start) + len(beginTag)
	end = string.find(endTag, begin)
	return string[begin:end]

def removeWhitespace(string):
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
	s = 0
	indices = []
	while True:
		newI = siteText.find(searchTerm, s)
		if newI == -1:
			break
		s = newI + len(searchTerm)
		indices.append(newI)

	return indices

def parseDate(dString):
	months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
	now = datetime.datetime.now()
	year = 0
	month = 0
	date = 0
	for i in range(len(months)):
		if months[i] in dtString.lower():
			month = i + 1
			break
	nums = ''.join([i for i in dtString if i.isdigit()])
	if len(nums) <= 2:
		date = int(nums)
		year = now.year if (month >= now.month) else (now.year + 1)
	elif str(now.year) in nums:
		date = int(nums.replace(str(now.year), ''))
		year = now.year
	elif str(now.year+1) in nums:
		date = int(nums.replace(str(now.year+1), ''))
		year = now.year
	return datetime.date(year, month, date)

def parseTime(tString):
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

	table = []
	for i in [0]+indices[:-1]:
		title = between(siteText, i, '<h3>', '</h3>')
		time = ''
		location = "The Blind Whino Art Annex"
		details = between(siteText, i, '<p>', '</p>')

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
		month = betwen(siteText, moIndices, moMarker, '</h5>')
		date = between(siteText, i, '</small><big>', '</big>')
		title = between(siteText, i, '<h4>', '</h4>')
		title = removeTag(title, "a")
		time = date + month #TODO: add time of day
		location = "Tudor Place Historic House and Garden"
		details = '<a href = https://www.tudorplace.org/programs' + between(siteText, i, '<a href="', '>') + '>Click here for more details</a>'
	return table

def writeCSV():
	with open('events.csv', 'w', newline='') as csvfile:
		eventFile = csv.writer(csvfile)
		eventTable = newseumScrape()
		eventTable += politicsProseScrape()
		eventTable += phillipsScrape()
		for event in eventTable:
			eventFile.writerow(event)

#writeCSV()