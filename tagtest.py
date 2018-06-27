import sys

with open(sys.argv, 'r', newline='') as htmlFile:
	i = 0
	tagDict = {}
	while i != -1:
		beg = htmlFile.find('<', i)
		end = min([htmlFile.find(' ', i), htmlFile.find('>', i)])
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

for key in tagDict.keys():
	if tagDict[key] != 0:
		print(key+': '+tagDict[key])