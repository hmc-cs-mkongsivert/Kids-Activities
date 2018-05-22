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
