import sys
from helpertools import *

exempt = ['br', 'meta', 'link', 'rect', 'polygon']

with open(sys.argv[1], 'r') as filename:
	htmlFile = removeWhitespace(filename.read())
	i = 0
	tagDict = {}
	while i > -1:
		beg = htmlFile.find('<', i)
		
		if htmlFile.find(' ', beg) == -1:
			end = htmlFile.find('>', beg)
		elif htmlFile.find('>', beg) == -1:
			end = htmlFile.find(' ', beg)
		else:
			end = min([htmlFile.find(' ', beg), htmlFile.find('>', beg)])
		tag = htmlFile[beg+1: end]
		i = end

		if tag[0] == '!': #a comment
			pass
		elif tag[0] == '/': #an end tag
			tagDict[tag[1:]]-=1
		else:
			if tag in tagDict:
				tagDict[tag]+=1
			else:
				tagDict[tag] =1
		if (len(htmlFile)-end) <= 1:
			break

for key in tagDict.keys():
	if tagDict[key] != 0 and key not in exempt:
		print(key+': '+str(tagDict[key]))