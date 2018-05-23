import requests
import csv

def between(string, start, beginTag, endTag):
	'''resturns a substring between two tags'''
	begin = string.find(beginTag, start) + len(beginTag)
	end = string.find(endTag, begin)
	return string[begin:end]

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

def makeIndicesList(siteText, searchTerm, ):
	#remove whitespace
	siteText = site.text
	siteText = siteText.replace("\t", "")
	siteText = siteText.replace("\n", "")

	s = 0
	indices = []
	while True:
		newI = siteText.find(searchTerm, s)
		if newI == -1:
			break
		s = newI + len(searchTerm)
		indices.append(newI)

	return indices

def newseumScrape():
	site = requests.get("http://www.newseum.org/events-programs/")
	siteText = site.text
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

def politicsProseScrape():
	site = requests.get("https://www.politics-prose.com/events")
	siteText = site.text
	indices = makeIndicesList(siteText, 'views-field-field-date')

	table = []
	for i in [0]+indices[:-1]:
		title = between(siteText, i, '<div class="views-field views-field-title">', '</div>')
		time = between(siteText, i, '<div class="views-field views-field-field-date-1">', '</div>')
		time = removeTag(time, "span") #not sure if this will do anything
		location = "Politics and Prose Bookstore"
		details = '<a href = "https://www.politics-prose.com/event' + between(title, 0, '<a href="', '>') + '>Click here for details'
		title = removeTag(title, "a", False, True)
		table.append([title, time, location])

	return table

def phillipsScrape():
	site = requests.get("http://www.phillipscollection.org/events?type=all")
	siteText = site.text
	indices = makeIndicesList(siteText, '<div class="field-event-date-range">')

	table = []
	for i in [0]+indices[:-1]:
		title = between(siteText, i, '<h2 class="delta a">', '</h2>')
		title = removeTag(title, "strong")
		time = between(siteText, i, '<div class="field-event-date-range">', '</div>')
		location = "The Phillips Collection"
		details = 

def writeCSV():
	with open('events.csv', 'w', newline='') as csvfile:
		eventFile = csv.writer(csvfile)
		eventTable = newseumScrape()
		eventTable += politicsProseScrape()
		for event in eventTable:
			eventFile.writerow(event)
