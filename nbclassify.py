vocab={}
with open("nbmodel.txt", "r+")  as f:
    for line in f:
    	(key, val) = line.split(" ",1)
       	vocab[key] = map(float,val.split())
#for word in vocab.keys():
	#print word," ",vocab[word]

prior=vocab['prior']

print("prior",prior)

nboutput=open("nboutput.txt", "w+")

import math
import sys
import os
input_dir=sys.argv[1]

punctuations ={".",",","...","!","?","(",")",";","/","\\"}
numbers ={"0","1","2","3","4","5","6","7","8","9"}

for filename in os.listdir(input_dir):
	if(filename.endswith(".txt")):
		print(filename)

		review=open(input_dir+"\\"+filename,'r+')
		words=review.read().lower()
		for punctuation in punctuations :
			words = words.replace(punctuation," ")
		for number in numbers :
			words = words.replace(number,"")

		words=words.split()

		posterior=[0,0,0,0] #initialize to prior
		for i in range(0,4):
			posterior[i]=math.log(prior[i])
		print(posterior)
		#print truthful," ",deceptive
		#print positive," ",negative
		for word in words:
			if(word in vocab.keys()):
				#print word
				for i in range(0,4):
					posterior[i]+=math.log(vocab[word][i+4])

		print("posterior:",posterior)
		maxindex = max( (v, i) for i, v in enumerate(posterior) )[1]
		print(maxindex)
		if maxindex==0:
			nboutput.write("truthful positive "+filename+"\n")
		elif maxindex==1:
			nboutput.write("truthful negative "+filename+"\n")
		elif maxindex==2:
			nboutput.write("deceptive positive "+filename+"\n")
		elif maxindex==3:
			nboutput.write("deceptive negative "+filename+"\n")

nboutput.close()
