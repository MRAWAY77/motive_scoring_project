import nltk
import numpy as np
import os 
import re
import pandas as pd
import csv
import collections
from nltk.util import ngrams
from itertools import zip_longest
from nltk.corpus import wordnet

content, Pow, Ach, Aff, Unnamed, temp, POS, input_text, pos_text, token, Sent = ([] for i in range(11))
check1, check2, check3, check4, synonyms, antonyms, result, output = ([] for i in range(8))
P1, P2 ,P3, P4, P5, P6, P7 = ([] for i in range(7))
PowWord, VB, VBG, VBN, VBZ, VBD, NN, NNP, RB, RBR, RBS, JJ, JJR, JJS, DT, PRP, IN, MD, NNS, WRB, CC, WP, PDT  = ([] for i in range(23))

def pos_tag(inputs):
	for sentence in inputs:
		Sent.append(sentence)
		text = nltk.word_tokenize(sentence)
		token.append(text)
		new_sentence = nltk.pos_tag(text)
		input_text.append(new_sentence)
		powerDict(new_sentence)
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
		
def count():
	counter = collections.Counter(POS)
	print(counter)
	print('\n')

def powerDict(new_sentence):
	for tags in new_sentence:
		if tags[1] == 'VB':
			VB.append(tags[0])
		elif tags[1] == 'VBG':
			VBG.append(tags[0])
		elif tags[1] == 'VBN':
			VBN.append(tags[0])
		elif tags[1] == 'VBZ':
			VBZ.append(tags[0])
		elif tags[1] == 'VBD':
			VBD.append(tags[0])
		elif tags[1] == 'NN':
			NN.append(tags[0])
		elif tags[1] == 'NNP':
			NNP.append(tags[0])
		elif tags[1] == 'RB':
			RB.append(tags[0])
		elif tags[1] == 'RBR':
			RBR.append(tags[0])
		elif tags[1] == 'RBS':
			RBS.append(tags[0])
		elif tags[1] == 'JJ':
			JJ.append(tags[0])
		elif tags[1] == 'JJR':
			JJR.append(tags[0])
		elif tags[1] == 'JJS':
			JJS.append(tags[0])
		elif tags[1] == 'DT':
			DT.append(tags[0])
		elif tags[1] == 'PRP' or tags[1] == 'PRP$':
			PRP.append(tags[0])
		elif tags[1] == 'IN':
			IN.append(tags[0])
		elif tags[1] == 'MD':
			MD.append(tags[0])
		elif tags[1] == 'NNS':
			NNS.append(tags[0])
		elif tags[1] == 'WRB':
			WRB.append(tags[0])
		elif tags[1] == 'CC':
			CC.append(tags[0])
		elif tags[1] == 'WP':
			WP.append(tags[0])
		elif tags[1] == 'PDT':
			PDT.append(tags[0])
	
	RemoveDuplicate(VB)
	RemoveDuplicate(VBG)
	RemoveDuplicate(VBN)
	RemoveDuplicate(VBZ)
	RemoveDuplicate(VBD)
	RemoveDuplicate(NN)
	RemoveDuplicate(NNP)
	RemoveDuplicate(RB)
	RemoveDuplicate(RBR)
	RemoveDuplicate(RBS)
	RemoveDuplicate(JJ)
	RemoveDuplicate(JJR)
	RemoveDuplicate(JJS)
	RemoveDuplicate(DT)
	RemoveDuplicate(PRP)
	RemoveDuplicate(IN)
	RemoveDuplicate(MD)
	RemoveDuplicate(NNS)
	RemoveDuplicate(WRB)
	RemoveDuplicate(CC)
	RemoveDuplicate(WP)
	RemoveDuplicate(PDT)

def RemoveDuplicate(datas):
	seen = set()
	for item in datas:
	    if item not in seen:
	        seen.add(item)
	        PowWord.append(item)
	# print(PowWord)
	del datas[:] 
	for uni in PowWord:
		datas.append(uni)
	del PowWord[:]


def POWER1(taggings,tags):
	filtering = ['Pass', 'Removed']
	c = len(taggings)
	dp = len(taggings)
	counter, c1pm ,c1nm, c2pm, c2nm, c3pm, c3nm =(0 for i in range(7))
	rule1 = "Include: {<VB*><VBN>|<VB><VBN>|<VBG><RB>|<IN><VBG>|<VB><WRB>|<MD><VB>}"
	Pchunker = nltk.RegexpParser(rule1)
	for elements in taggings[:]:
		A = Pchunker.parse(elements)
		if A.height() > 2:
			check1.append(filtering[0])
			c1pm +=1
		else:
			check1.append(filtering[1])
			c1nm+=1
	
	for elements in tags[:]:
		for w in elements:
			if w == 'NNP':
				counter+=1
		if counter > 2:
			counter = 0
			c2pm+=1
			check2.append(filtering[0])
		else:
			check2.append(filtering[1])
			c2nm+=1

		counter = 0
		
		for z in elements:
			if z == 'PRP':
				counter+=1
		if counter > 2:
			counter = 0
			c3pm+=1
			check3.append(filtering[0])
		else:
			check3.append(filtering[1])
			c3nm+=1

	for i, j, k in zip(check1,check2,check3):
		if i == 'Removed' and j == 'Removed' and k == 'Removed':
			dp-=1
			P1.append(filtering[1])
		else:
			P1.append(filtering[0])
	del check1[:]
	del check2[:]
	del check3[:]

	print('total = {}. c1pm ={} & c1nm ={}. c2pm={} & c2nm={}. c3pm={} & c3nm={}.'.format(c,c1pm,c1nm,c2pm,c2nm,c3pm,c3nm))
	print('total Positive Capture for rule 1 = {}'.format(dp))

def POWER2(taggings,tags):
	filtering = ['Pass', 'Removed']
	c = len(taggings)
	dp = len(taggings)
	counter, c1pm ,c1nm, c2pm, c2nm, c3pm, c3nm =(0 for i in range(7))
	rule2 = "Include: {<JJ><TO>|<JJR><NN>|<NN><WP>|<RB><VBN>}"
	Pchunker = nltk.RegexpParser(rule2)
	for elements in taggings[:]:
		A = Pchunker.parse(elements)
		if A.height() > 2:
			check1.append(filtering[0])
			c1pm +=1
		else:
			check1.append(filtering[1])
			c1nm+=1
	
	for elements in tags[:]:
		for w in elements:
			if w == 'WP':
				counter+=1
		if counter > 0:
			counter = 0
			c2pm+=1
			check2.append(filtering[0])
		else:
			check2.append(filtering[1])
			c2nm+=1

	for i, j in zip(check1,check2):
		if i == 'Removed' and j == 'Removed':
			dp-=1
			P2.append(filtering[1])
		else:
			P2.append(filtering[0])
	del check1[:]
	del check2[:]

	print('total = {}. c1pm ={} & c1nm ={}. c2pm={} & c2nm={}.'.format(c,c1pm,c1nm,c2pm,c2nm))
	print('total Positive Capture for rule 2 = {}'.format(dp))

def POWER3(taggings,tags):
	filtering = ['Pass', 'Removed']
	c = len(taggings)
	dp = len(taggings)
	counter, c1pm ,c1nm, c2pm, c2nm, c3pm, c3nm =(0 for i in range(7))
	rule3 = "Include: {<MD><RB>|<VB><IN>|<MD><RB>|<VBG><IN>|<NN><VBZ>|<WP><VBD>|<VBZ><VBG>|<TO><VB>|<VBZ><RB>|<VBP><VBG>}"
	Pchunker = nltk.RegexpParser(rule3)
	for elements in taggings[:]:
		A = Pchunker.parse(elements)
		if A.height() > 2:
			check1.append(filtering[0])
			c1pm +=1
		else:
			check1.append(filtering[1])
			c1nm+=1
	
	for elements in tags[:]:
		if elements[0] == 'RB' or elements[0] == 'IN':
			counter+=1
		if counter > 1:
			counter = 0
			c2pm+=1
			check2.append(filtering[0])
		else:
			check2.append(filtering[1])
			c2nm+=1

	for i, j in zip(check1,check2):
		if i == 'Removed' and j == 'Removed':
			dp-=1
			P3.append(filtering[1])
		else:
			P3.append(filtering[0])
	del check1[:]
	del check2[:]

	print('total = {}. c1pm ={} & c1nm ={}. c2pm={} & c2nm={}.'.format(c,c1pm,c1nm,c2pm,c2nm))
	print('total Positive Capture for rule 3 = {}'.format(dp))

def POWER4(taggings):
	filtering = ['Pass', 'Removed']
	c = len(taggings)
	dp = len(taggings)
	counter, c1pm ,c1nm, c2pm, c2nm, c3pm, c3nm =(0 for i in range(7))
	rule4 = "Include: {<VBG><TO><VB>|<VBD><RB>|<VBG><IN><JJ>}"
	Pchunker = nltk.RegexpParser(rule4)
	for elements in taggings[:]:
		A = Pchunker.parse(elements)
		if A.height() > 2:
			check1.append(filtering[0])
			c1pm +=1
		else:
			check1.append(filtering[1])
			c1nm+=1
	
	for i in check1:
		if i == 'Removed':
			dp-=1
			P4.append(filtering[1])
		else:
			P4.append(filtering[0])
	del check1[:]

	print('total = {}. c1pm ={} & c1nm ={}.'.format(c,c1pm,c1nm))
	print('total Positive Capture for rule 4 = {}'.format(dp))

def POWER5(taggings):
	filtering = ['Pass', 'Removed']
	c = len(taggings)
	dp = len(taggings)
	counter, c1pm ,c1nm, c2pm, c2nm, c3pm, c3nm =(0 for i in range(7))
	rule5 = "Include: {<JJ><JJ>|<VBD><RB>|<VB*><PRP*>|<VBZ><VBG>|<RB><RB>|<RB><JJ>}"
	Pchunker = nltk.RegexpParser(rule5)
	for elements in taggings[:]:
		A = Pchunker.parse(elements)
		if A.height() > 2:
			check1.append(filtering[0])
			c1pm +=1
		else:
			check1.append(filtering[1])
			c1nm+=1
	
	for i in check1:
		if i == 'Removed':
			dp-=1
			P5.append(filtering[1])
		else:
			P5.append(filtering[0])
	del check1[:]

	print('total = {}. c1pm ={} & c1nm ={}.'.format(c,c1pm,c1nm))
	print('total Positive Capture for rule 5 = {}'.format(dp))

def POWER6(taggings,tags):
	filtering = ['Pass', 'Removed']
	c = len(taggings)
	dp = len(taggings)
	counter, c1pm ,c1nm, c2pm, c2nm, c3pm, c3nm, c4pm, c4nm =(0 for i in range(9))
	rule6 = "Include: {<VBZ><VBN>|<RB><VBN>|<JJ><WRB>|<JJ><JJ>|<RB><JJ>|<CC><RB>|<JJ><NN>|<VBD><JJ>}"
	Pchunker = nltk.RegexpParser(rule6)
	for elements in taggings[:]:
		A = Pchunker.parse(elements)
		if A.height() > 2:
			check1.append(filtering[0])
			c1pm +=1
		else:
			check1.append(filtering[1])
			c1nm+=1
	
	for elements in tags[:]:
		for w in elements:
			if w == 'JJ':
				counter+=1
		if counter > 2:
			counter = 0
			c2pm+=1
			check2.append(filtering[0])
		else:
			check2.append(filtering[1])
			c2nm+=1

		counter = 0
		
		for z in elements:
			if z == 'PRP':
				counter+=1
		if counter > 2:
			counter = 0
			c3pm+=1
			check3.append(filtering[0])
		else:
			check3.append(filtering[1])
			c3nm+=1

		counter = 0
		
		for x in elements:
			if x == 'NNP':
				counter+=1
		if counter > 2:
			counter = 0
			c4pm+=1
			check4.append(filtering[0])
		else:
			check4.append(filtering[1])
			c4nm+=1

	for i, j, k, l in zip(check1,check2,check3,check4):
		if i == 'Removed' and j == 'Removed'and k == 'Removed' and l == 'Removed':
			dp-=1
			P6.append(filtering[1])
		else:
			P6.append(filtering[0])
	del check1[:]
	del check2[:]
	del check3[:]
	del check4[:]

	print('total = {}. c1pm ={} & c1nm ={}. c2pm={} & c2nm={}. c3pm={} & c3nm={}. c4pm={} & c4nm={}.'.format(c,c1pm,c1nm,c2pm,c2nm,c3pm,c3nm,c4pm,c4nm))
	print('total Positive Capture for rule 6 = {}'.format(dp))

def CSV():
	title = ['Pow', 'Ach', 'Aff','Unnamed: 6']
	df = pd.read_csv('/home/alvinwong/Desktop/GGD.csv',skipinitialspace=True)
	for val in df['Pow']:
		Pow.append(val)
	for val in df['Ach']:
		Ach.append(val)
	for val in df['Aff']:
		Aff.append(val)
	for val in df['Unnamed: 6']:
		Unnamed.append(val)

	fields = ['Input Sentence', 'Tokenizer', 'POS', 'Rule 1', 'Rule 2', 'Rule 3', 'Rule 4', 'Rule 5', 'Rule 6', 'POW', 'ACH', 'AFF', 'Unnamed']
	original = pd.DataFrame(data = [Sent, token, pos_text, P1, P2, P3, P4, P5, P6, Pow, Ach, Aff, Unnamed], index = fields).transpose()
	original.to_csv('/home/alvinwong/Desktop/WWW.csv')

def main_method(subject):
	pos_tag(subject)
	count()
	POWER1(input_text,pos_text)
	POWER2(input_text,pos_text)
	POWER3(input_text,pos_text)
	POWER4(input_text)
	POWER5(input_text)
	POWER6(input_text,pos_text)
	CSV()
################################ MAIN PROGRAM ##############################################################
df = pd.read_csv('/home/alvinwong/Desktop/GGD.csv',skipinitialspace=True)
for element in df['Text']:
	content.append(element)
	
main_method(content)

########################## Checking for Every Rule ########################################################

TP1, TP2, TP3, TP4, TP5, TP6, TC = (0 for a in range(7))
TP = 0
TI = 1381
df = pd.read_csv('/home/alvinwong/Desktop/WWW.csv',skipinitialspace=True)

for i, j in zip(df['Rule 1'], df['POW']):
	if i == 'Pass' and j == 'yes':
		TP1+=1		
print('TP1={}'.format(TP1))

precision1 = (TP1/525)*100
recall1 = (TP1/188)*100
Fmeasure1 = (2*precision1*recall1)/(precision1+recall1)

print('Power Rule1: [precision = {}, recall = {}, F.measure = {}] '.format(precision1,recall1,Fmeasure1))

for i, j in zip(df['Rule 2'], df['POW']):
	if i == 'Pass' and j == 'yes':
		TP2+=1		
print('TP2={}'.format(TP2))

precision2 = (TP2/230)*100
recall2 = (TP2/188)*100
Fmeasure2 = (2*precision2*recall2)/(precision2+recall2)

print('Power P2: [precision = {}, recall = {}, F.measure = {}] '.format(precision2,recall2,Fmeasure2))

for i, j in zip(df['Rule 3'], df['POW']):
	if i == 'Pass' and j == 'yes':
		TP3+=1		
print('TP3={}'.format(TP3))

precision3 = (TP3/874)*100
recall3 = (TP3/188)*100
Fmeasure3 = (2*precision3*recall3)/(precision3+recall3)

print('Power P3: [precision = {}, recall = {}, F.measure = {}] '.format(precision3,recall3,Fmeasure3))

for i, j in zip(df['Rule 4'], df['POW']):
	if i == 'Pass' and j == 'yes':
		TP4+=1		
print('TP4={}'.format(TP4))

precision4 = (TP4/122)*100
recall4 = (TP4/188)*100
Fmeasure4 = (2*precision4*recall4)/(precision4+recall4)

print('Power P4: [precision = {}, recall = {}, F.measure = {}] '.format(precision4,recall4,Fmeasure4))

for i, j in zip(df['Rule 5'], df['POW']):
	if i == 'Pass' and j == 'yes':
		TP5+=1		
print('TP5={}'.format(TP5))

precision5 = (TP5/467)*100
recall5 = (TP5/188)*100
Fmeasure5 = (2*precision5*recall5)/(precision5+recall5)

print('Power P5: [precision = {}, recall = {}, F.measure = {}] '.format(precision5,recall5,Fmeasure5))

for i, j in zip(df['Rule 6'], df['POW']):
	if i == 'Pass' and j == 'yes':
		TP6+=1		
print('TP6={}'.format(TP6))

precision6 = (TP6/789)*100
recall6 = (TP6/188)*100
Fmeasure6 = (2*precision6*recall6)/(precision6+recall6)

print('Power P6: [precision = {}, recall = {}, F.measure = {}] '.format(precision6,recall6,Fmeasure6))

b = 'Fail'

for i, j, k, l, m, n in zip(df['Rule 1'],df['Rule 2'],df['Rule 3'],df['Rule 4'],df['Rule 5'], df['Rule 6']):
	if i == 'Removed' and  j == 'Removed' and  k == 'Removed' and  l == 'Removed' and  m == 'Removed' and n == 'Removed' :
		TC+=1
		P7.append('Removed')
	else:
		P7.append('Pass')

for p, f in zip(P7,df['POW']):
	 if p == 'Pass' and f == 'yes':
	 	TP+=1
PC = TI - TC
print('Removed Count={}'.format(TC))
print('Pass Count ={}'.format(PC))
print('TP={}'.format(TP))

precision = (TP/1220)*100
recall = (TP/188)*100
Fmeasure = (2*precision*recall)/(precision+recall)

print('Power Final Result: [precision = {}, recall = {}, F.measure = {}] '.format(precision,recall,Fmeasure))

fields = ['VB', 'VBG', 'VBN', 'VBZ', 'VBD', 'NN', 'NNP', 'RB', 'RBR', 'RBS', 'JJ', 'JJR', 'JJS', 'DT', 'PRP', 'IN', 'MD', 'NNS', 'WRB', 'CC', 'WP', 'PDT']
Verb = pd.DataFrame(data = [VB, VBG, VBN, VBZ, VBD, NN, NNP, RB, RBR, RBS, JJ, JJR, JJS, DT, PRP, IN, MD, NNS, WRB, CC, WP, PDT], index = fields).transpose()
Verb.to_csv('/home/alvinwong/Desktop/POS.csv')
