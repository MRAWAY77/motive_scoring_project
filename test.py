import nltk
import numpy as np
import os 
import re
import pandas as pd
import csv

files = open ("/home/alvinwong/Desktop/All_Input.txt", 'r')
content = files.readlines()

D = pd.read_csv("/home/alvinwong/Desktop/AAA.csv")
#data manipulation

D.to_csv("/home/alvinwong/Desktop/AAA.csv")
A = []
for sentence in content:
	text = nltk.word_tokenize(sentence)
	new_sentence = nltk.pos_tag(text)
	for filtered in new_sentence:
		KW =(filtered[1])
		A.append(KW)
	# print(new_sentence)
	
print(sorted(A))


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
