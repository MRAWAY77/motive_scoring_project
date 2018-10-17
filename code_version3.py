import nltk
import numpy as np
import os 
import re
import pandas as pd
import csv
import collections
from nltk.util import ngrams

files = open ("/home/alvinwong/Desktop/All_Input.txt", 'r')
content = files.readlines()

files = open ("/home/alvinwong/Desktop/motive.txt", 'r')
valid = files.readlines()

files = open ("/home/alvinwong/Desktop/noMotive.txt", 'r')
invalid = files.readlines()

files = open ("/home/alvinwong/Desktop/keys.txt", 'r')
keys = files.readlines()

D = pd.read_csv("/home/alvinwong/Desktop/AAA.csv")
#data manipulation

D.to_csv("/home/alvinwong/Desktop/AAA.csv")

temp = []
POS = []
input_text = []
pos_text = []
motive = []
non_motive = []
filt_Motive = []
filtnon_Motive = []
num_M = 0
num_N = 0
score = 0
global mistake

def pos_tag(inputs):
	for sentence in inputs:
		text = nltk.word_tokenize(sentence)
		new_sentence = nltk.pos_tag(text)
		input_text.append(new_sentence)
		for tags in new_sentence:
			KW =tags[1]
			POS.append(KW)

	for element in input_text:
		for index in element:
			LIST = list(index)
			LIST.remove(LIST[0])
			temp.append(LIST)
		flatten = [item for sublist in temp for item in sublist]
		pos_text.append(flatten)
		del temp[:]

	# print(pos_text)
	# print(input_text)

def count():
	counter = collections.Counter(POS)
	print(counter)
	print('\n')

def chunker(taggings):
	c = len(taggings)
	patterns = "Exclude: {<VBD><RB>|<CC><VBD>|<VBZ><JJ>|<VBG><IN>}"
	Pchunker = nltk.RegexpParser(patterns)
	for elements in taggings[:]:
		A = Pchunker.parse(elements)
		if A.height() > 2:
			taggings.remove(elements)
			c-=1
		print(A.height())
	print(c)
	print(taggings)
		# A.draw()
	# for elements in taggings:
	# 	tagpairs = list(ngrams(elements,n =2))
	# 	temp.append(tagpairs)
	
	# for elements in temp:
	# 	for index in elements:
	# 		if index[0] == 'CC' and index[1] == 'VBD':
	# 			print(elements)
	# 			print('\n')
	# 			temp.remove(elements)
	# 			c-=1
	# 		if index[0] == 'VBZ' and index[1] == 'JJ':
	# 			print(elements)
	# 			print('\n')
	# 			temp.remove(elements)
	# 			c-=1
	# 		if index[0] == 'MD' and index[1] == 'RB':
	# 			print(elements)
	# 			print('\n')
	# 			temp.remove(elements)
	# 			c-=1
	# 		if index[0] == 'VBD' and index[1] == 'RB':
	# 			print(elements)
	# 			print('\n')
	# 			temp.remove(elements)
	# 			c-=1
	# 		if index[0] == 'MD' and index[1] == 'PRP':
	# 			print(elements)
	# 			print('\n')
	# 			temp.remove(elements)
	# 			c-=1
	# 		if index[0] == 'VBG' and index[1] == 'IN':
	# 			print(elements)
	# 			print('\n')
	# 			temp.remove(elements)
	# 			c-=1
	# print(temp)
	# print(c)


def point_sys(scanning,points):
	switcher ={
	1: 'PRP',
	2: '.',
	3: 'NN',
	4: 'VB',
	5: 'VBD',
	6: 'JJ',
	7: 'IN',
	8: 'DT',
	9: 'NNP',
	10: 'MD',
	11: 'TO',
	12: ',',
	13: 'RB',
	14: 'VBP',
	15: 'CC',
	16: 'PRP$',
	17: 'WRB',
	18: 'VBG',
	19: 'VBZ',
	20: 'FW'
	}
	for pos in scanning:
		for tag in pos:
			for posttag in switcher:
				if tag == switcher[1]:
					points+=0
				if tag == switcher[2]:
					points+=0
					break
				if tag == switcher[3]:
					points+=0
					break
				if tag == switcher[4]:
					points+=0
					break
				if tag == switcher[5]:
					points+=1
					break
				if tag == switcher[6]:
					points+=1
					break
				if tag == switcher[7]:
					points+=1
					break
				if tag == switcher[8]:
					points+=0
				if tag == switcher[9]:
					points+=0
					break
				if tag == switcher[10]:
					points+=1
					break
				if tag == switcher[11]:
					points+=0
					break
				if tag == switcher[12]:
					points+=0
					break
				if tag == switcher[13]:
					points+=1
					break
				if tag == switcher[14]:
					points+=0
					break
				if tag == switcher[15]:
					points+=1
				if tag == switcher[16]:
					points+=0
					break
				if tag == switcher[17]:
					points+=0
					break
				if tag == switcher[18]:
					points+=1
					break
				if tag == switcher[19]:
					points+=1
					break
				if tag == switcher[20]:
					points+=0
					break


		pos.append(int(points))
		points = 0

def Perror_sentence(Input,filtered,valid,mistake):
	errorP = len(valid)
	for element in Input:
		for nodes in filtered:
			if nodes[-1] == element[-1]:
				errorP-=1

	mistake = abs(errorP)
	return mistake

def Nerror_sentence(Input,filtered,invalid,mistake):
	errorN = len(invalid)
	for element in Input:
		for nodes in filtered:
			if nodes[-1] == element[-1]:
				errorN-=1

	mistake = abs(errorN)
	return mistake

def Positive_filt(judge,correct,wrong,valid):
	countTrue = 0
	countP = 0 
	countN = 0
	accuracy = 0
	mistake = 0

	for tve in correct:
		if tve[-1] >2:
			filt_Motive.append(tve)
			countP+=1
	
	print(filt_Motive)
	print(countP)
	print('\n')

	for nve in wrong:
		if nve[-1] >2:
			filt_Motive.append(nve)
			countN+=1

	print(filt_Motive)
	print(countN)
	Perror_sentence(judge,filt_Motive,valid,mistake)
	print('\n')
	
	countTrue+= countP + countN
	percentage = (countTrue/len(valid))*100
	error = Perror_sentence(judge,filt_Motive,valid,mistake)
	errorRate = (error/len(valid)) * 100
	accuracy = countTrue - error
	accuracyRate = accuracy/len(valid)*100
	print('Motive Sentence = {}/{} with result of ({}%) and error rate of {}/{} ({}%).'.format(countTrue,len(valid),percentage,error,len(valid),errorRate))
	print('Accurary level of Motive Sentence = {}/{} with result of ({}%).'.format(accuracy,len(valid),accuracyRate))
	print('\n')


def Negative_filt(judge,invalid):
	countFalse = 0
	countP = 0 
	countN = 0
	accuracy = 0 
	mistake = 0

	for lists in judge:
		if lists[-1] >=2:
			filtnon_Motive.append(lists)
			countN+=1
	
	print(filtnon_Motive)
	Nerror_sentence(judge,filtnon_Motive,invalid,mistake)
	print(countN)
	print('\n')

	countFalse+= countP + countN
	percentage = (countFalse/len(invalid))*100
	error = Nerror_sentence(judge,filtnon_Motive,invalid,mistake)
	errorRate = (error/len(valid)) * 100
	accuracy = countFalse - error
	accuracyRate = accuracy/len(invalid)*100
	print('Non-Motive Sentence = {}/{} with result of ({}%) and error rate of {}/{} ({}%).'.format(countFalse,len(invalid),percentage,error,len(invalid),errorRate))
	print('Accurary level of Non-Motive Sentence = {}/{} with result of ({}%).'.format(accuracy,len(invalid),accuracyRate))
	print('\n')

def main_method(subject):
	pos_tag(subject)
	chunker(input_text)
	count()
	point_sys(pos_text,score)
	# Positive_filt(input_text,motive,non_motive,valid)
	# Negative_filt(pos_text,invalid)
	print(len(input_text))
	# print('\n')
	# print(pos_text)
	# print('\n')
	# print(non_motive)


main_method(content)

######################STILL TESTING WITH FLAWS NOW############################
	#D.to_csv("Excel_details.csv")
	# motive = "motive: {<VBP>?<VBP><TO>*<VB>}"
	# action = 'action: {<JJ>?<NN>*<NN>}'
	# cp = nltk.RegexpParser(motive or action)
	# result = cp.parse(new_sentence)
	# print(result)
	# result.draw()
	#break

# groucho_grammar = nltk.CFG.fromstring("I saw a car accident outside the mall.")
# sent = nltk.word_tokenize("I saw a car accident outside the mall.")
# parser = nltk.ChartParser(groucho_grammar)
# for tree in parser.parse(sent):
# 	 print(tree)