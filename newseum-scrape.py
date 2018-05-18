import requests

site = requests.get("http://www.newseum.org/events-programs/")
searchTerm = '"ai1ec-event"'

def between(string, start, beginTag, endTag):
	begin = string.find(beginTag, start) + len(beginTag)
	end = string.find(endTag, begin)
	return string[begin:end]

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
	location = between(siteText, i, '<span class="ai1ec-event-location">', '</span>')
	table.append([title, location])

print(table)

'''
	TODO: I think there is a bug where I don't consider multiple instances of
	the end tag, so I need to fix that in the between function. I also need to
	find somewhere to put the titles and locations, like in a CSV file.
	Finally, I need to include othe tags than title and location and do some
	general cleaning up.
'''