import csv

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

def writeHTML():
	with open('activities-list.html', 'r', newline='') as htmlRead:
		oldText = htmlRead.read()
		beginTag = "<!-- Table Begins Here -->"
		endTag = "<!-- Table Ends Here -->"
		table = makeTable()
		beforeTable = oldText.find(beginTag) + len(beginTag)
		afterTable = oldText.find(endTag)
		newText = oldText[:beforeTable] + table + oldText[afterTable:]
	with open('activities-list.html', 'w', newline='') as htmlWrite:
		htmlWrite.write(newText)

writeHTML()
