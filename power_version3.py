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

content, Sent, token ,input_text, pos_text, temp, POS, output = ([] for i in range(8))
Pow, Ach, Aff, Unnamed = ([] for i in range(4))
total = 1381

def pos_tag(inputs):
	for sentence in inputs:
		Sent.append(sentence)
		text = nltk.word_tokenize(sentence)
		token.append(text)
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

def great_filter(postag):
	Noun = ['NN', 'NNS', 'NNP'] 
	Adjective = ['JJ', 'JJR', 'JJS'] 
	Adverb = ['RB', 'RBR', 'RBS'] 
	Verb = ['VB', 'VBP', 'VBD', 'VBN', 'VBZ', 'VBG'] 
	Function = ['CC', 'MD','IN', 'PRP', 'PRP$']
	Identifier = ['WRB', 'WP', 'WP$', 'WDT', 'PDT']

	context, noun, adjective, adverb, verb, function, identifier, useless = (0 for i in range(8))

	for inputtag in postag:
		for tag in inputtag:
			for A in Noun:
				if tag == A:
					noun +=1	
			for B in Adjective:
				if tag == B:
					adjective +=1
			for C in Adverb:
				if tag == C:
					adverb +=1
			for D in Verb:
				if tag == D:
					verb +=1
			for item in Function:
				if tag == item:
					function+=1
			for notes in Identifier:
				if tag == notes:
					identifier+=1
		context = noun + adverb + adjective + verb
		useless = len(inputtag) - (context+function+identifier)
		# print('Noun = {}, Adjective = {}, Adverb = {}, Verb = {}, function = {}, identifier = {}, useless = {}.'.format(noun,adjective,adverb,verb,function,identifier,useless))
		decision(len(inputtag),noun, adjective, adverb, verb,function,identifier,useless)
		context, noun, adjective, adverb, verb, function, identifier, useless = (0 for i in range(8))

def decision(total,noun,adjective,adverb,verb,function,identifier,useless):
	Filter = ['Pass', 'Removed']
	
	Noun = (noun/total)*100
	Adjective = (adjective/total)*100
	Adverb = (adverb/total)*100
	Verb = (verb/total)*100
	function = (function/total)*100
	identifier = (identifier/total)*100
	useless = (useless/total)*100

	if Noun > 15 and Noun <30:
		output.append(Filter[0])
	elif Adjective >=15:
		output.append(Filter[0])
	elif Adverb >=15 :
		output.append(Filter[0])
	elif Verb >= 25 :
		output.append(Filter[0])
	elif Noun <= 20:
		if (function+identifier) < useless:
			output.append(Filter[1])
		else:
			output.append(Filter[0])
	else:
		output.append(Filter[1])

	# print('Noun = {}%, Adjective = {}%, Adverb = {}%, Verb = {}%, function = {}%, identifier = {}%, useless = {}%.'.format(Noun,Adjective,Adverb,Verb,function,identifier,useless))

def CSV():
	title = ['Pow', 'Ach', 'Aff','Unnamed: 6']
	df = pd.read_csv('/home/alvinwong/Desktop/Winter.csv',skipinitialspace=True)
	for val in df['Pow']:
		Pow.append(val)
	for item in df['Ach']:
		Ach.append(item)
	for text in df['Aff']:
		Aff.append(text)
	for notes in df['Unnamed: 6']:
		Unnamed.append(notes)

	fields = ['Input Sentence', 'Tokenizer', 'POS', 'Great Filter', 'POW', 'ACH', 'AFF', 'Unnamed']
	original = pd.DataFrame(data = [Sent, token, pos_text, output, Pow, Ach, Aff, Unnamed], index = fields).transpose()
	original.to_csv('/home/alvinwong/Desktop/WWW.csv')

def Calulation(name,data1,data2):
	TP,FP,TN,FN = (0 for i in range(4))

	for i,j in zip(data1,data2):
		if  i == 'Pass' and j == 'yes':
			TP+=1
		elif i == 'Pass' and j == 'no':
			FP+=1
		elif i == 'Removed' and j == 'no':
			TN+=1
		elif i == 'Removed' and j == 'yes':
			FN+=1			

	TPR = TP/(TP+FN)*100
	FPR = FP/(FP+TN)*100
	recall = TP/(TP+FN)*100
	precision = TP/(TP+FP)*100
	F_measure = (2*precision*recall)/(precision+recall)

	print('\n')
	print(' {}: True_Positive = {}, False_Positive = {}, True_Negative = {}, False_Negative = {}.'.format(name,TP,FP,TN,FN))
	print('{}: Precision = {}, Recall = {}, F-Measure = {}.'.format(name,precision,recall,F_measure))
	print('{}: True_Positive_Rate = {}, False_Positive_Rate = {}.'.format(name,TPR,FPR))
	print('\n')

def General_Filter(name,data1,data2,data3,data4,data5,data6):
	TP,FP,TN,FN = (0 for i in range(4))

	FP = data5 - TP
	FN = data6 - TN

	for i, j, k, l in zip(data1,data2,data3,data4):
		if i == 'Removed' and j == 'no' and k == 'no' and l == 'no':
			TN+=1		

	for i, j, k, l in zip(data1,data2,data3,data4):
		if i == 'Pass' and (j == 'yes' or k == 'yes' or l == 'yes'):
			TP+=1			

	TPR = TP/(TP+FN)*100
	FPR = FP/(FP+TN)*100
	recall = TP/(TP+FN)*100
	precision = TP/(TP+FP)*100
	F_measure = (2*precision*recall)/(precision+recall)

	print('\n')
	print(' {}: True_Positive = {}, False_Positive = {}, True_Negative = {}, False_Negative = {}.'.format(name,TP,FP,TN,FN))
	print('{}: Precision = {}, Recall = {}, F-Measure = {}.'.format(name,precision,recall,F_measure))
	print('{}: True_Positive_Rate = {}, False_Positive_Rate = {}.'.format(name,TPR,FPR))

################################ MAIN PROGRAM ##############################################################
pwr, ach, aff, M = (0 for i in range(4))
df = pd.read_csv('/home/alvinwong/Desktop/GGD.csv',skipinitialspace=True)
for element in df['Text']:
	content.append(element)

for i,j,k in zip(df['Pow'],df['Ach'], df['Aff']):
	if i == 'yes' or j == 'yes' or k =='yes':
		M+=1
	
df.to_csv('/home/alvinwong/Desktop/GGD.csv')
for word in df['Pow']:
	if word == 'yes':
		pwr+=1

for word in df['Ach']:
	if word == 'yes':
		ach+=1

for word in df['Aff']:
	if word == 'yes':
		aff+=1
NM = total - M
print('Power Motive = {}, Achievement Motive = {}, Affiliation Motive = {}, Total_Motive Count = {}, Non-Motive Count = {}.'.format(pwr,ach,aff,M,NM))
pos_tag(content)
great_filter(pos_text)
CSV()
########################################################################## OUTPUT FILE ################################################
df = pd.read_csv('/home/alvinwong/Desktop/WWW.csv',skipinitialspace=True)

Pass_count, Removed_count = (0 for i in range(2)) 

for i in df['Great Filter']:
	if i == 'Pass':
		Pass_count+=1
	elif i == 'Removed':
		Removed_count+=1

print('Predicted_Motive = {}, Predicted_No_Motive = {}.'.format(Pass_count,Removed_count))

General_Filter('General_Filter',df['Great Filter'],df['POW'],df['ACH'],df['AFF'],Pass_count,Removed_count)
Calulation('Power',df['Great Filter'], df['POW'])
Calulation('Achievement',df['Great Filter'], df['ACH'])
Calulation('Affiliation',df['Great Filter'], df['AFF'])
