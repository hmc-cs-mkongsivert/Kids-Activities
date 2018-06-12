import requests
import csv
import datetime as dt
import calendar as cal
from helpertools import *


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
#	exhibs = makeIndicesList(siteText, 'class="list-item-title balance-text"')
	events = makeIndicesList(siteText, 'class="tribe-events-title list-item-title balance-text"')

	table = []
#	for i in [0]+exhibs[:-1]:
#		title = between(siteText, i, '<h4 class="list-item-title balance-text">', '</h4>')
#		time = 'time!'
#		location = 'The Hirshhorn Museum and Sculpture Garden'
#		details = ''
	for i in [0]+events[:-1]:
		title = between(siteText, i, '<h4 class="tribe-events-title list-item-title balance-text">', '</h4>')
		title = removeTag(title, 'a')
		dtString = between(siteText, i, '<div class="tribe-events-duration list-item-date">', '</div>')
		where = 'The Hirshhorn Museum and Sculpture Garden'
		details = ''#'<a href = "' + between(siteText, i, '<a href="', '"') + '">click here for details</a>'
		dtList = dtString.split('|')
		date = parseDate(dtList[0])
		time = parseTime(dtList[1])
		when = (dt.datetime.combine(date, time[0]), dt.datetime.combine(date, time[1]))
		table.append([title, when, where, details])

	return table

def newseumScrape():
	site = requests.get("http://www.newseum.org/events-programs/")
	siteText = removeWhitespace(site.text)
	indices = makeIndicesList(siteText, '"ai1ec-event"')

	table = []
	for i in [0]+indices[:-1]:
		title = between(siteText, i, '<span class="ai1ec-event-title">', '</span>')
		dtString = between(siteText, i, '<div class="ai1ec-event-time">', '</div>')
		dtString = removeTag(dtString, "span", middle = False)
		where = "The Newseum"
		details = between(siteText, i, '<div class="ai1ec-popup-excerpt">', '</div>')

		date = None
		time = None

		#parse time(s)
		if '@' in dtString:
			dtList = dtString.split('@')
			time = parseTime(dtList[1])
			dtString = dtList[0]
		else:
			time = (dt.time(9), dt.time(17))

		#parse date(s)
		if '–' in dtString:
			dates = dtString.split('–')
			begDate = parseDate(dates[0])
			endDate = parseDate(dates[1])
			current = begDate
			while current <= endDate:
				when = (dt.datetime.combine(current, time[0]), dt.datetime.combine(current, time[1]))
				table.append([title, when, where, details])
				current += dt.timedelta(days = 1)
		else:
			date = parseDate(dtString)
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
		dtString = between(siteText, i, '<div class="field-event-date-range">', '</div>')
		dtString = removeTag(removeTag(dtString, "span"), "span")
		dtString = removeTag(dtString, "p")
		where = "The Phillips Collection"
		details = '<a href = "https://www.phillipscollection' + between(title, 0, '<a href="', '>') + '>Click here for more details</a>'
		title = removeTag(title, "a", False, True)

		date = None
		time = None

		#parse time(s)
		if 'am' in dtString or 'pm' in dtString:
			dtList = dtString.split(',')
			time = parseTime(dtList[2])
			dtString = dtList[0] + ", " + dtList[1]
		else:
			#not quite accurate, maybe fix later
			time = (dt.time(10), dt.time(17))

		#parse date(s)
		if '–' in dtString:
			dates = dtString.split('–')
			begDate = parseDate(dates[0])
			endDate = parseDate(dates[1])
			current = begDate
			while current <= endDate:
				when = (dt.datetime.combine(current, time[0]), dt.datetime.combine(current, time[1]))
				table.append([title, when, where, details])
				current += dt.timedelta(days = 1)
		else:
			date = parseDate(dtString)
			when = (dt.datetime.combine(date, time[0]), dt.datetime.combine(date, time[1]))
			table.append([title, when, where, details])
	
	return table

def politicsProseScrape():
	site = requests.get("https://www.politics-prose.com/events")
	siteText = removeWhitespace(site.text)
	indices = makeIndicesList(siteText, 'views-field-field-date')

	table = []
	for i in [0]+indices[:-1:2]:
		title = between(siteText, i, '<div class="views-field views-field-title">', '</div>')
		dtString = between(siteText, i, '<span class="date-display-single">', '</span>')
		#not sure if this will do anything
		where = "Politics and Prose Bookstore"
		details = '<a href = "https://www.politics-prose.com' + between(title, 0, '<a href="', '>') + '>Click here for details</a>'
		title = removeTag(title, "a", False, True)
		dtList = dtString.split(',')
		
		date = 0
		time = 0

		time = parseTime(dtList[2])
		date = parseDate(dtList[0] + ", " + dtList[1])
		start = dt.datetime.combine(date, time[0])
		when = (start, start + dt.timedelta(hours = 1))
		
		table.append([title, when, where, details])

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
		if mo+1 < len(moIndices):
			if i > moIndices[mo+1]:
				mo += 1
		month = between(siteText, moIndices[mo], moMarker, '</h5>')
		day = between(siteText, i, '</small><big>', '</big>')
		title = between(siteText, i, '<h4>', '</h4>')
		title = removeTag(title, "a")
		where = "Tudor Place Historic House and Garden"
		details = '<a href = https://www.tudorplace.org/programs' + between(siteText, i, '<a href="', '>') + '>Click here for more details</a>'
		
		date = parseDate(day + ' ' + month) #TODO: add time of day
		tString = between(siteText, i, '</a></h4><small>', "&#183;")
		times = parseTime(tString)
		when = (dt.datetime.combine(date,times[0]),dt.datetime.combine(date,times[1]))

		table.append([title, when, where, details])
	return table

def usbgScrape():
	site = requests.get("https://www.usbg.gov/programs-and-events")
	siteText = removeWhitespace(site.text)
	indices = makeIndicesList(siteText, '<div class="fullcalendar-event">')

	table = []
	for i in [0]+indices[:-1]:
		dtString = between(siteText, i, '<div class="fullcalendar-instance">', '</div>')
		dtString = removeTag(dtString, "span", False, True)
		title = between(siteText, i, '<h3 class="title">', '</h3>')
		title = removeTag(title, 'a')
		where = "United States Botanical Garden"
		details = '<a href="usbg.gov' + between(siteText, i, '<a href="', '">') + '">Click here for more details</a>'

		dtString = dtString.split(',')[1]#remove day of week
		dtList = dtString.split('-')
		when = dtList
		table.append([title, when, where, details])
	return table

def writeCSV():
	'''gathers all of the data and packs them into a CSV file'''
	with open('events.csv', 'w', newline='') as csvfile:
		eventFile = csv.writer(csvfile)
		eventTable = blindWhinoScrape()
		eventTable += hirshhornScrape()
		eventTable += newseumScrape()
		eventTable += phillipsScrape()
		eventTable += politicsProseScrape()
		eventTable += tudorScrape()
		
		sortedTable = sortByDate(eventTable)
		
		for event in sortedTable:
			if event[1][1] >= dt.datetime.now():
				eventFile.writerow(event)
				#eventFile.writerow(formatDates(event))

print(usbgScrape())