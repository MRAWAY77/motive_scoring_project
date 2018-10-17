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

files = open ("/home/alvinwong/Desktop/ExcelInput.txt", 'r')
content = files.readlines()

files = open ("/home/alvinwong/Desktop/ExcelMotive.txt", 'r')
valid = files.readlines()

files = open ("/home/alvinwong/Desktop/ExcelNOMotive.txt", 'r')
invalid = files.readlines()

Pow, Ach, Aff, Unnamed, temp, POS, input_text, pos_text, token, checking, Sent = ([] for i in range(11))
synonyms, antonyms, result, output = ([] for i in range(4))

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

def count():
	counter = collections.Counter(POS)
	print(counter)
	print('\n')

def chunker(taggings):
	filtering = ['Pass', 'Removed']
	c = len(taggings)
	patterns = "Exclude: {<VBD><RB>|<CC><VBD>|<VBZ><JJ>|<VBG><IN>}"
	Pchunker = nltk.RegexpParser(patterns)
	for elements in taggings[:]:
		A = Pchunker.parse(elements)
		if A.height() > 2:
			temp.append(elements)
			checking.append(filtering[1])
			taggings.remove(elements)
			c-=1
		else:
			checking.append(filtering[0])
		print(A.height())
		
	print(c)
	print(checking)
	print(taggings)

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

	df['Unnamed: 6'] = Unnamed
	fields = ['Input Sentence', 'Tokenizer', 'POS', 'Great Filter', 'POW', 'ACH', 'AFF', 'Unnamed']
	original = pd.DataFrame(data = [Sent, token, pos_text, checking, Pow, Ach, Aff, Unnamed], index = fields).transpose()
	original.to_csv('/home/alvinwong/Desktop/BBB.csv')

def powerDict():
	PowWord = ['good', 'better', 'best']
	for pWrd in PowWord:
		for syn in wordnet.synsets(pWrd): 
		    for l in syn.lemmas(): 
		        synonyms.append(l.name()) 
		        if l.antonyms(): 
		            antonyms.append(l.antonyms()[0].name()) 

	seen = set()
	for item in synonyms:
	    if item not in seen:
	        seen.add(item)
	        result.append(item)
	done = set()
	for item in antonyms:
	    if item not in done:
	        done.add(item)
	        output.append(item)


def main_method(subject):
	pos_tag(subject)
	count()
	chunker(input_text)
	CSV()
	print('\n')
	
main_method(content)