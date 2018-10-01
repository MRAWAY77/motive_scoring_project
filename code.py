#import nltk.book 
import numpy as np
import os 
import re
import pandas as pd

D = pd.read_csv("/home/alvinwong/Desktop/Excel_details.csv")

#Funtion for breaking groundtruth text
def check_positive(text,positive):
	print (text)
	new_sentence = re.findall(r'\w+',text)
	print(new_sentence)
	Score_Motive = 0
	motive = []
	for word in new_sentence:
		for sametext in positive:
			if word == sametext:
				Score_Motive += 1
				motive.append(sametext)
				print(motive)
	if Score_Motive >1:
		#DispText = " ".join(text)
		DispKey = "-".join(motive)
		print ('Motive Score:{}'.format(Score_Motive))
		print('This input-text: "{}" has positivity in motive imagery because of the phrase/words: {}\n'.format(text,DispKey))
	
	
def check_negative(text,negative):
	new_sentence = re.findall(r'\w+',text)
	#print(negative)
	Score_Neutral = 0
	noMotive = []
	for word in new_sentence:
		for similarword in negative:
			#print(similarword)
			if word == similarword:
				Score_Neutral += 1
				noMotive.append(similarword)
				print(noMotive)
	if Score_Neutral >= 0:
		disptxt = "-".join(noMotive)
		print ('Motive Score:{}'.format(Score_Neutral))
		print('This input-text: "{}" has NO (negative/ denial) motive imagery because of the phrase/words:{}\n'.format(text,disptxt))


#Open ground-truth && keywords for motive.
files = open ("/home/alvinwong/Desktop/motive.txt", 'r')
content = files.readlines()

keywords = open ("/home/alvinwong/Desktop/motiveKeywords.txt", 'r')
key = keywords.readlines()

neutrals = open ("/home/alvinwong/Desktop/noMotiveKeywords.txt", 'r')
negative = neutrals.readlines()

# iterate the files content by lines
for sentence in content:
	for phrase in key:
		wordings = phrase.split()
		for negate in negative:
			#print(negate)
			denial = negate.split()
			#print(denial)
			check_positive(sentence,wordings)
			check_negative(sentence,denial)