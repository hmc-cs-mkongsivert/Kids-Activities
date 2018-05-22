import requests

site = requests.get("https://www.politics-prose.com/events")
searchTerm = 'views-field-field-date'

def between(string, start, beginTag, endTag):
	begin = string.find(beginTag, start) + len(beginTag)
	end = string.find(endTag, begin)
	return string[begin:end]

def removeTag(string, tag):
	pass
	#removes extraneous tags

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
	table.append([title, time])

print(table)

'''
	TODO: I need to	find somewhere to put the titles and locations, like in a
	CSV file. Also, I need to do some general cleaning up.
'''