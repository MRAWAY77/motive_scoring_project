import nltk
import numpy as np
import os 
import re
import pandas as pd
import csv
import collections

files = open ("/home/alvinwong/Desktop/All_Input.txt", 'r')
content = files.readlines()

D = pd.read_csv("/home/alvinwong/Desktop/AAA.csv")
#data manipulation

D.to_csv("/home/alvinwong/Desktop/AAA.csv")

POS = []
input_text = []
motive = []
non_motive = []
filt_Motive = []
num_M = 0
num_N = 0
score = 0

def pos_tag(inputs):
	for sentence in inputs:
		text = nltk.word_tokenize(sentence)
		new_sentence = nltk.pos_tag(text)
		input_text.append(new_sentence)
		for filtered in new_sentence:
			KW =(filtered[1])
			POS.append(KW)

def count():
	counter = collections.Counter(POS)
	print(counter)


def PRP_removal(scanning,useful,useless,counts_M,counts_N):
	for sent in scanning:
		for word in sent:
			# print(word)
			if word[1] == "PRP":
				useful.append(sent)
				counts_M+=1
			if word[1] != "PRP":
				useless.append(sent)
				counts_N+=1
			break
	# useful = '\n'.join(useful)
	# print(useful)
	# print(counts_M)
	# print(useless)
	# print(counts_N)

def point_sys(scanning,points):
	switcher ={
	1: 'JJ',
	2: 'VBD',
	3: 'VB',
	4: 'NN',
	5: 'PRP',
	6: 'RB',
	7: 'CC'
	}
	for pos in scanning:
		for tag in pos:
			for posttag in switcher:
				if tag[1] == switcher[7]:
					points*=-1
				if tag[1] == switcher[6]:
					points*=-1
					break
				if tag[1] == switcher[5]:
					points+=5
					break
				if tag[1] == switcher[4]:
					points+=4
					break
				if tag[1] == switcher[3]:
					points+=3
					break
				if tag[1] == switcher[2]:
					points+=2
					break
				if tag[1] == switcher[1]:
					points+=1
					break
		pos.append(int(points))
		points = 0

def pts_filt(judge,correct,wrong):
	print(motive)
	print('\n')
	print(non_motive)
	print('\n')
	for words in correct:
		if words[-1] >= 7:
			filt_Motive.append((words))
	
	print(filt_Motive)
	print('\n')

	for words in correct:
		if words[-1] >= 7:
			motive.remove(words)
	
	print(motive)
	print('\n')
			
		
	# [motive.pop(motive.index(words)) for words in correct if words[-1]>=8]
	# print(motive)
	# print('\n')

		# for RB in words:
		# 	if RB[1] == 'VBD' and (RB[1]+1) == 'RB':
		# 		motive.pop(words)
		# 		print(motie.size)


def main_method():
	pos_tag(content)
	count()
	PRP_removal(input_text,motive,non_motive,num_M,num_N)
	point_sys(input_text,score)
	pts_filt(input_text,motive,non_motive)
	print(input_text)
	# print(motive)
	# print(non_motive)


main_method()

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