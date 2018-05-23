import csv

def makeTable():
	table = "<tbody>"
	with open('events.csv', newline='') as csvFile:
		dataReader = csv.reader(csvFile)
		for row in dataReader:
			table += "\n<tr>"
			for item in row:
				table += "\n<th>" + item + "</th>"
			table+= "\n</tr>"
	table += "\n</tbody>"
	return table

def writeHTML():
	with open('activities-list.html', newline='') as htmlFile:
		oldText = htmlFile.read()
		beginTag = "<!-- Table Begins Here -->"
		endTag = "<!-- Table Ends Here -->"
		table = makeTable()
		beforeTable = oldText.find(beginTag) + len(beginTag)
		afterTable = oldText.find(endTag)
		newText = oldText[:beforeTable] + table + oldText[afterTable:]
		htmlFile.write(newText)

writeHTML()
