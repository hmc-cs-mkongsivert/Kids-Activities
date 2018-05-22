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

def newseumScrape():
	site = requests.get("http://www.newseum.org/events-programs/")
	searchTerm = '"ai1ec-event"'
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
	searchTerm = 'views-field-field-date'

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

	table = []
	for i in [0]+indices[:-1]:
		title = between(siteText, i, '<div class="views-field views-field-title">', '</div>')
		time = between(siteText, i, '<div class="views-field views-field-field-date-1">', '</div>')
		location = "Politics and Prose Bookstore"
		details = ""
		table.append([title, time, location])

	return table

def writeCSV():
	with open('events.csv', 'w', newline='') as csvfile:
		eventFile = csv.writer(csvfile)
		eventTable = newseumScrape()
		eventTable += politicsProseScrape()
		for event in eventTable:
			eventFile.writerow(event)
			