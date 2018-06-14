import csv
from helpertools import *

coords = {'Blind Whino Art Annex': [38.88041, -77.01192],
	'Hirshhorn Museum and Sculpture Garden': [38.88816, -77.02304],
	'International Spy Museum': [38.8970326, -77.0233503],
	'Mount Vernon': [38.71029, -77.08644],
	'National Mall': [38.88994, -77.02698],	
	'Newseum': [38.89312, -77.0192],
	'Phillips Collection': [38.9115020, -77.0468522],
	'Politics and Prose Bookstore': [38.9554465, -77.0696419],
	'Tudor Place Historic House and Garden': [38.91146, -77.06304],
	'United States Botanical Garden': [38.8882478, -77.0129011]}

def makeDict():
	'''reads events from a CSV file and formats them into a dictionary
	separated by location'''
	mapLabels = {}
	with open('events.csv', newline='') as csvFile:
		dataReader = csv.reader(csvFile)
		for row in dataReader:
			if row[2] in mapLabels:
				mapLabels[row[2]].append(row)
			else:
				mapLabels[row[2]] = [row]
	return mapLabels

#TODO: add javascript
def makeTable(mapLabels):
	'''takes in a dictionary of events separated by location and returns an
	HTML-formatted table displaying event times and titles'''
	lb = '\n' + '\t'*11 #indenting to match the rest
	tableStr = lb+'<table>'
	for key in mapLabels.keys():
		tableStr += lb+'<div id="'+key[:5].lower()'">'+lb+'<h3>'+key+'</h3>'
		tableStr += lb+'<table>'
		for item in mapLabels[key]:
			tableStr += lb+'<tr>'
			tableStr += lb+'<th>' + item[1] + '</th>'#time
			tableStr += lb+'<th>' + item[0] + '</th>'#title
			tableStr += lb+'</tr>'
		tableStr += lb+'</table>'+lb
	return tableStr

def makeMap(mapLabels):
	'''takes in a dictionary of events separated by location and returns a
	GeoJSON file to indicate location and quantity of events on a map'''
	jsonStr = ""
	for key in mapLabels.keys():
		jsonStr += 'var '+key[:4].lower()+'events = {\n"type": "Feature",\n'
		jsonStr += 'properties": {\n"popupContent": "'+key+'",\n"style": {\n'
		jsonStr += 'weight: 0,\nopacity: 0,\nfillColor: "#00ffdf",\n'
		jsonStr += 'fillOpacity: 0.5\n}\n},\n"geometry": {\n'
		jsonStr += '"type": "MultiPolygon",\n"coordinates": [\n[\n[\n'
		
		scale = len(mapLabels[key])#events
		shape = polygon(coords[key], scale, 6)
		
		jsonStr += str(shape)+']\n]\n]\n}\n};\n\n'
	return jsonStr

#OVERHAUL
def writeHTML(beginTag, endTag, filename, function):
	'''inserts what a given function indicates should be inserted in filename
	between beginTag and endTag'''
	with open(filename, 'r', newline='') as htmlRead:
		oldText = htmlRead.read()
		table = function(mapLabels)
		beforeTable = oldText.find(beginTag) + len(beginTag)
		afterTable = oldText.find(endTag)
		newText = oldText[:beforeTable] + table + oldText[afterTable:]
	with open(filename, 'w', newline='') as htmlWrite:
		htmlWrite.write(newText)

begTable = "<!-- Table Begins Here -->"
endTable = "<!-- Table Ends Here -->"
#writeHTML(begTable, endTable, 'map.html', makeTable)

begMap = "//begin labels"
endMap = "//end labels"
writeHTML(begMap, endMap, 'map.html', makeMap)
