from __future__ import division
import sys
import os
import glob


input_dir=sys.argv[1]

# 4-Class Classification
vocab={}

punctuations ={".",",","...","!","?","(",")",";","/","\\","\""}
numbers ={"0","1","2","3","4","5","6","7","8","9"}
#omitted : "aren't","wouldn't""won't","can't", "cannot" "against" "again"  "couldn't", "didn't","don't", "doesn't", "few", "hadn't "hasn't",, "haven't" "weren't",  "shouldn't""isn't", "mustn't", "shan't", "wasn't" , "too"
#"more", "most",  "no", "nor", "not",
stopwords = {"a", "about", "above", "after", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did",  "do", "does", "doing", "down", "during", "each",  "for", "from", "further", "had", "has","have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is",  "it", "it's", "its", "itself", "let's", "me", "my", "myself", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"}

docs=[0,0,0,0]
tokens=[0,0,0,0]

#for review in zf.namelist():
paths=["positive_polarity/truthful_from_TripAdvisor/","negative_polarity/truthful_from_Web/","positive_polarity/deceptive_from_MTurk/","negative_polarity/deceptive_from_MTurk/"]

for x in range(0,4): #tru_pos,tru_neg,dec_pos,dec_neg
	input_path=input_dir+paths[x]
	print(input_path)
	for foldname in os.listdir(input_path):
	#can add text to truthful and deceptive simultaneously
		if(foldname.startswith("fold")):
			print(foldname)
			complete_path=input_path+foldname+"/"
			#print len(os.listdir(complete_path))
			docs[x]+=len(os.listdir(complete_path))
			for filename in os.listdir(complete_path):
				review=open(complete_path+"/"+filename,"r+")
				text=review.read()
				review.close()
				text=text.lower()

				#remove punctuations
				for punctuation in punctuations :
					text = text.replace(punctuation," ")
				for number in numbers :
					text = text.replace(number,"")

				#count tokens in each class
				words=text.split()

				for word in words:
					if (word not in stopwords): #omit stopwords
						if (
							word not in vocab.keys()
							) :
							vocab.update({word:[0,0,0,0,0,0,0,0]})

						tokens[x]+=1
						vocab[word][x]+=1


print ("tokens in tru_pos, tru_neg, dec_pos, dec_neg ")
print (tokens)

len_vocab=len(vocab)
print ("vocab len",len_vocab)

nbmodel= open("nbmodel.txt", "w+")
for word in vocab.keys():
	#print "count in tru pos:",vocab[word][0]
	#print "tokens in tru pos:",tokens_truthful_pos
	vocab[word][4]=((1+vocab[word][0])/(len_vocab+tokens[0]))
	vocab[word][5]=((1+vocab[word][1])/(len_vocab+tokens[1]))
	vocab[word][6]=((1+vocab[word][2])/(len_vocab+tokens[2]))
	vocab[word][7]=((1+vocab[word][3])/(len_vocab+tokens[3]))
	vocabstr=str(vocab[word]).replace(","," ")
	vocabstr=vocabstr.replace("[","")
	vocabstr=vocabstr.replace("]","")
	#print word," ",vocabstr
	nbmodel.write(word+" "+vocabstr+"\n")


total_docs=docs[0]+docs[1]+docs[2]+docs[3]
print ("total_docs:",total_docs)
print ("docs in tru_pos, tru_neg, dec_pos, dec_neg ")
print(docs)

prior=[0,0,0,0]

for i in range(0,4):
	prior[i]=docs[i]/total_docs

print(prior)
priorstr=str(prior).replace(","," ")
priorstr=priorstr.replace("[","")
priorstr=priorstr.replace("]","")

nbmodel.write("prior "+priorstr+"\n")

nbmodel.close()


