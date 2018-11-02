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
			for D in Adverb:
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
		print('Noun = {}, Adjective = {}, Adverb = {}, Verb = {}, function = {}, identifier = {}, useless = {}.'.format(noun,adjective,adverb,verb,function,identifier,useless))
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

	if Noun > 10 and Noun < 30:
		output.append(Filter[0])
	elif Adjective >10:
		output.append(Filter[0])
	elif Adverb >10 :
		output.append(Filter[0])
	elif Verb > 20 :
		output.append(Filter[0])
	elif Noun <= 20:
		if (function+identifier) < useless:
			output.append(Filter[1])
		else:
			output.append(Filter[0])
	else:
		output.append(Filter[1])

	print('Noun = {}%, Adjective = {}%, Adverb = {}%, Verb = {}%, function = {}%, identifier = {}%, useless = {}%.'.format(Noun,Adjective,Adverb,Verb,function,identifier,useless))

def CSV():
	title = ['Pow', 'Ach', 'Aff','Unnamed: 6']
	df = pd.read_csv('/home/alvinwong/Desktop/GGD.csv',skipinitialspace=True)
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

################################ MAIN PROGRAM ##############################################################
df = pd.read_csv('/home/alvinwong/Desktop/GGD.csv',skipinitialspace=True)
for element in df['Text']:
	content.append(element)

pos_tag(content)
great_filter(pos_text)
CSV()

df = pd.read_csv('/home/alvinwong/Desktop/WWW.csv',skipinitialspace=True)

Pow_Score, Ach_Score, Aff_Score, NO_Motive, Pass_count, Removed_count = (0 for i in range(6)) 

for i in df['Great Filter']:
	if i == 'Pass':
		Pass_count+=1
	elif i == 'Removed':
		Removed_count+=1

print('Pass_count = {}, Removed_count = {}.'.format(Pass_count,Removed_count))

########################################## POWER ######################################################################
for i, j in zip(df['Great Filter'], df['POW']):
	if i == 'Pass' and j == 'yes':
		Pow_Score+=1		
print('Pow_Score={}'.format(Pow_Score))

precisionPwr = (Pow_Score/Pass_count)*100
recallPwr = (Pow_Score/189)*100
Fmeasure_Power = (2*precisionPwr*recallPwr)/(precisionPwr+recallPwr)

print('Power: [precision = {}, recall = {}, F.measure = {}] '.format(precisionPwr,recallPwr,Fmeasure_Power))

############################################# Achievement #################################################################
for i, j in zip(df['Great Filter'], df['ACH']):
	if i == 'Pass' and j == 'yes':
		Ach_Score+=1		
print('Pow_Score={}'.format(Ach_Score))

precisionAch = (Ach_Score/Pass_count)*100
recallAch = (Ach_Score/113)*100
Fmeasure_Achievement = (2*precisionAch*recallAch)/(precisionAch+recallAch)

print('Achievement: [precision = {}, recall = {}, F.measure = {}] '.format(precisionAch,recallAch,Fmeasure_Achievement))

############################################# Affiliation #################################################################
for i, j in zip(df['Great Filter'], df['AFF']):
	if i == 'Pass' and j == 'yes':
		Aff_Score+=1		
print('Pow_Score={}'.format(Aff_Score))

precisionAff = (Aff_Score/Pass_count)*100
recallAff = (Aff_Score/168)*100
Fmeasure_Affiliation = (2*precisionAff*recallAff)/(precisionAff+recallAff)

print('Affiliation: [precision = {}, recall = {}, F.measure = {}] '.format(precisionAff,recallAff,Fmeasure_Affiliation))

############################################# No-Motive #################################################################
for i, j, k, l in zip(df['Great Filter'], df['POW'], df['ACH'], df['AFF']):
	if i == 'Removed' and j == 'no' and k == 'no' and l == 'no':
		NO_Motive+=1		
print('NO-Motive_Score={}'.format(NO_Motive))

precision_NO = (NO_Motive/Removed_count)*100
recall_NO = (NO_Motive/944)*100
Fmeasure_NO = (2*precision_NO*recall_NO)/(precision_NO+recall_NO)

print('No-Motive: [precision = {}, recall = {}, F.measure = {}] '.format(precision_NO,recall_NO,Fmeasure_NO))

###################################################### Motive ###################################################################
Motive = (1381 - 944)

precisionM = ((Pow_Score+Ach_Score+Aff_Score)/Pass_count)*100
recallM = ((Pow_Score+Ach_Score+Aff_Score)/Motive)*100
Fmeasure_Motive = (2*precisionM*recallM)/(precisionM+recallM)

print('Motive: [precision = {}, recall = {}, F.measure = {}] '.format(precisionM,recallM,Fmeasure_Motive))
