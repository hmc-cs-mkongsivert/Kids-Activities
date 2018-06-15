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
	'''takes in a dictionary of events indexed by location and returns an
	HTML-formatted table displaying event times and titles'''
	lb = '\n' + '\t'*7 #indenting to match the rest
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

def makeJS(mapLabels):
	'''takes in a dictionary of events indexed by location and returns the
	javascript to hide and show the corresponding table of events'''
	lb = '\n'+'\t'*7

	#construct map
	scriptStr="<script>"+lb+"var map = L.map('map').setView([38.89,"
	scriptStr+=" -77.026148], 11);"+lb+"L.tileLayer('https://api.tiles.mapbox"
	scriptStr+=".com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {"+lb
	scriptStr+="attribution: 'Map data &copy; <a href=\"https://www."
	scriptStr+="openstreetmap.org/\">OpenStreetMap</a> contributors, <a href="
	scriptStr+="\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA"
	scriptStr+="</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>"
	scriptStr+="',"+lb+"maxZoom: 20,"+lb+"id: 'mapbox.streets',"+lb+"access"
	scriptStr+="Token: 'pk.eyJ1IjoibWtvbmdzaXZlcnQiLCJhIjoiY2ppNHljYTZlMGViYTN"
	scriptStr+="ybzY1ODBrZHFteiJ9.cryeQAatX8rCKMgGo8rRNw'"+lb+"}).addTo(map);"

	for key in mapLabels.keys():
		keyID = key[:5].lower()
		#set the table's visibility to hidden initially
		scriptStr+=ls*2+"var "+keyID+"Table = document.getElementById('"+keyID
		scriptStr+="');"+lb+keyID"Table.style.visibility = 'hidden';"
		#create functions to change tables' visibilities
		scriptStr+=ls*2+"function "+keyID+"In(e) {"+lb+keyID+"Table.style."
		scriptStr+="visibility = 'visible';"+lb+"}"+lb+"function "+keyID
		scriptStr+="Out(e) {"+lb+keyID+"Table.style.visibility = 'hidden';"+lb+"}"
		#add interaction FIX-----------------------------------------------------------------------------------
		scriptStr+="function onEachFeature(feature, layer) {"+lb+"if (feature."
		scriptStr+="properties && feature.properties.popupContent) {"+lb
		scriptStr+="popupContent = feature.properties.popupContent;"+lb+"}"
		scriptStr+=lb+"layer.bindPopup(popupContent);"+lb+"layer.on({"
		scriptStr+=lb+"mouseover: sidebarIn,"+lb+"mouseout: sidebarOut"+lb
		scriptStr+="});"+lb+"}"

def makeJSON(mapLabels):
	'''takes in a dictionary of events indexed by location and returns a
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

def main():
	'''reads in events from CSV file and puts them into the HTML and JSON
	files'''
	beginTag = "<!-- Tables Begin Here -->"
	endTag = "<!-- Tables End Here -->"
	eventDict = makeDict()
	with open('geojson.js', 'w', newline='') as jsonWrite:
		jsonStr = makeJSON(eventDict)
		jsonWrite.write(jsonStr)
	with open('map.html', 'r', newline='') as htmlRead:
		oldText = htmlRead.read()
		tables = makeTable(mapLabels)
		script = makeJS(mapLabels)
		beforeTable = oldText.find(beginTag) + len(beginTag)
		afterTable = oldText.find(endTag)
		newText = oldText[:beforeTable] + tables + script + oldText[afterTable:]
	with open('map.html', 'w', newline='') as htmlWrite:
		htmlWrite.write(newText)
