# -*- coding: UTF8 -*-
import csv
import datetime as dt
from helpertools import *

today = dt.datetime.now()
todayStr = str(today.year)+'-'+str(today.month)+'-'+str(today.day)+'/'
coords = {'Blind Whino Art Annex': [[38.88041, -77.01192], 'https://www.swarts\
club.org/art-annex/'],
	'Hirshhorn Museum and Sculpture Garden': [[38.88816, -77.02304], 'https://\
hirshhorn.si.edu/exhibitions-events/'],
	'International Spy Museum': [[38.8970326, -77.0233503], 'https://www.spymu\
seum.org/calendar/upcoming/1/'],
	'Mount Vernon': [[38.71029, -77.08644], 'https://www.mountvernon.org/plan-\
your-visit/calendar/'+todayStr],
	'National Mall': [[38.88994, -77.02698], 'https://www.nps.gov/nama/planyou\
rvisit/calendar.htm'],
	'Newseum': [[38.89312, -77.0192], 'http://www.newseum.org/events-programs/\
'],
	'Phillips Collection': [[38.9115020, -77.0468522], 'http://www.phillipscol\
lection.org/events?type=all'],
	'Politics and Prose Bookstore': [[38.9554465, -77.0696419], 'https://www.p\
olitics-prose.com/events'],
	'Tudor Place Historic House and Garden': [[38.91146, -77.06304], 'https://\
www.tudorplace.org/programs/'],
	'United States Botanical Garden': [[38.8882478, -77.0129011], 'https://www\
.usbg.gov/programs-and-events']}

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
	tableStr = ''
	for key in mapLabels.keys():
		tableStr += lb+'<div class="sideoverlay" id="'+key[:5]\
.lower()+'">'+lb+'<h3>'+key+'</h3>'
		tableStr += lb+'<table>'
		for item in mapLabels[key]:
			tableStr += lb+'<tr>'
			tableStr += lb+'<th>' + item[1] + '</th>'#time
			tableStr += lb+'<th>' + item[0] + '</th>'#title
			tableStr += lb+'</tr>'
		tableStr += lb+'</table>'+lb+'</div>'+lb
	return tableStr

def makeJS(mapLabels):
	'''takes in a dictionary of events indexed by location and returns the
	javascript to hide and show the corresponding table of events'''
	lb = '\n'+'\t'*7

	#construct map
	scriptStr="<script>"+lb+"var map = L.map('map').setView([38.85, -77.026148\
], 11);"+lb+"L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png\
?access_token={accessToken}', {"+lb+"attribution: 'Map data &copy; <a href=\"h\
ttps://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"http\
s://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\
\"https://www.mapbox.com/\">Mapbox</a>',"+lb+"maxZoom: 20,"+lb+"id: 'mapbox.st\
reets',"+lb+"accessToken: 'pk.eyJ1IjoibWtvbmdzaXZlcnQiLCJhIjoiY2ppNHljYTZlMGVi\
YTNybzY1ODBrZHFteiJ9.cryeQAatX8rCKMgGo8rRNw'"+lb+"}).addTo(map);"
	featFun="function green(e) {"+lb+"var layer = e.target;"+lb+"layer.setStyl\
e({color: \"#00FF08\", fillColor: \"#00FF08\"});"+lb+"}"+lb*2+"function cyan(e\
) {"+lb+"var layer = e.target;"+lb+"layer.setStyle({color: \"#00AD97\", fillCo\
lor: \"#00ffdf\"});"+lb+"}"+"function onEachFeature(feature, layer) {"+lb+"if \
(feature.properties && feature.properties.popupContent) {"+lb+"popupContent = \
feature.properties.popupContent;"+lb+"}"+lb+"layer.bindPopup(popupContent);"
	eventVars=""

	for key in mapLabels.keys():
		keyID = key[:5].lower()
		#set the table's visibility to hidden initially
		scriptStr+=lb*2+"var "+keyID+" = document.getElementById('"+keyID\
+"');"+lb+keyID+"Bool = false;"+lb+keyID+".style.visibility = 'hidden';"
		#create functions to change tables' visibilities
		scriptStr+=lb*2+"function "+keyID+"In(e) {"+lb+keyID+".style.visibilit\
y = 'visible';"+lb+"green(e);"+lb+"}"+lb+"function "+keyID+"Out(e) {"+lb+"if (\
!"+keyID+"Bool) {"+lb+keyID+".style.visibility = 'hidden';"+lb+"cyan(e);"+lb+"\
}"+lb+"}"+lb+"function "+keyID+"Click(e) {"+lb+keyID+"Bool = "+keyID+"Bool ? f\
alse : true;"+lb+"}"
		#add interaction
		featFun+=lb+"if (feature.properties.name == '"+keyID+"'){layer.on({"+\
lb+"mouseover: "+keyID+"In,"+lb+"mouseout: "+keyID+"Out,"+lb+"click: "+keyID+"\
Click"+lb+"});"+lb+"}"
		eventVars+=keyID+'events, '
	featFun+=lb+"}"+lb+"L.geoJSON(["+eventVars[:-2]+"], {"+lb+"style: function \
(feature) {"+lb+"return feature.properties && feature.properties.style;"+lb+"},\
onEachFeature: onEachFeature"+lb+"}).addTo(map);"+lb+"</script>"+lb
	return scriptStr+featFun

def makeJSON(mapLabels):
	'''takes in a dictionary of events indexed by location and returns a
	GeoJSON file to indicate location and quantity of events on a map'''
	jsonStr = ""
	for key in mapLabels.keys():
		keyID = key[:5].lower()
		jsonStr += 'var '+keyID+'events = {\n"type": "Feature",\n"properties"\
: {\n"popupContent": "<a href=\''+coords[key][1]+'\' target=\'_blank\'>'+key+\
'</a>",\n"name": "'+keyID+'",\n"style": {\nweight: .8,\nopacity: 1,\ncolor: "\
#00DDC1",\nfillColor: "#00ffdf",\nfillOpacity: 0.4\n}\n},\n"geometry": {\n"typ\
e": "MultiPolygon",\n"coordinates": \n[\n[\n'
		
		scale = len(mapLabels[key])#events
		shape = polygon(coords[key][0], scale, 42)
		
		jsonStr += str(shape)+'\n]\n]\n}\n};\n\n'
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
		tables = makeTable(eventDict)
		script = makeJS(eventDict)
		beforeTable = oldText.find(beginTag)+len(beginTag)
		afterTable = oldText.find(endTag)
		newText = oldText[:beforeTable]+tables+script+oldText[afterTable:]
	with open('map.html', 'w', newline='') as htmlWrite:
		htmlWrite.write(newText)

if __name__ == "__main__":
	main()