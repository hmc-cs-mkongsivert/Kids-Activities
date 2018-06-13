import csv

coords = {'The Blind Whino Art Annex': [38.88041, -77.01192],
	'The Hirshhorn Museum and Sculpture Garden': [38.88816, -77.02304],
	'The International Spy Museum': [38.8970326, -77.0233503],
	'Mount Vernon': [38.71029, -77.08644],
	'National Mall': [38.88994, -77.02698],	
	'The Newseum': [38.89312, -77.0192],
	'The Phillips Collection': [38.9115020, -77.0468522],
	'Politics and Prose Bookstore': [38.9554465, -77.0696419],
	'Tudor Place Historic House and Garden': [38.91146, -77.06304],
	'United States Botanical Garden': [38.8882478, -77.0129011]}

def makeTable():
	table = "\n<table>"
	with open('events.csv', newline='') as csvFile:
		dataReader = csv.reader(csvFile)
		for row in dataReader:
			table += "\n<tr>"
			for item in row:
				table += "\n<th>" + item + "</th>"
			table+= "\n</tr>"
	table += "\n</table>\n"
	return table

def makeMap():
	mapLabels = {}
	with open('events.csv', newline='') as csvFile:
		dataReader = csv.reader(csvFile)
		for row in dataReader:
			if row[2] in mapLabels:
				mapLabels[row[2]].append(row)
			else:
				mapLabels[row[2]] = [row]

	labelString = "\n"
	for key in mapLabels.keys():
		num = len(mapLabels[key])#events
		labelString += "\n\nvar circle= L.circle(" + str(coords[key])
		labelString += ", { \ncolor: '#00ffdf', \nfillColor: '#00ffdf', \nfillOpacity: 0.5, \nradius:"
		labelString += str(20*num) + "\n}).addTo(mymap);"
	return labelString

def writeHTML(beginTag, endTag, filename, function):
	with open(filename, 'r', newline='') as htmlRead:
		oldText = htmlRead.read()
		table = function()
		beforeTable = oldText.find(beginTag) + len(beginTag)
		afterTable = oldText.find(endTag)
		newText = oldText[:beforeTable] + table + oldText[afterTable:]
	with open(filename, 'w', newline='') as htmlWrite:
		htmlWrite.write(newText)

begTable = "<!-- Table Begins Here -->"
endTable = "<!-- Table Ends Here -->"
#writeHTML(begTable, endTable, 'activities-list.html', makeTable)

begMap = "//begin labels"
endMap = "//end labels"
writeHTML(begMap, endMap, 'map.html', makeMap)
