# -*- coding: cp1254 -*-

# Onur Yilmaz

# Imports
import bisect        
import random        
import yaml           
import textwrap 
from nltk.tokenize import BlanklineTokenizer
from nltk.corpus.reader import TaggedCorpusReader
from random import shuffle
from nltk.corpus import treebank 
from nltk import tag 
from nltk.tag import brill
from nltk.tag import brill_trainer
import pickle


# Brill tagger parameters
max_rules=300
min_score=3

# Training parameters
development_size=5110
train=.85


# Read data from development.sdx
data = TaggedCorpusReader('.', r'.*\.sdx', sep='|', sent_tokenizer=BlanklineTokenizer())

# Get the list of tagged sentences
tagged_data = data.tagged_sents()


# Lower words and return as a list
tagged_data_list  = [[t for t in sent] for sent in tagged_data] 
tagged_data_list = [[(w.lower(),t) for (w,t) in s] for s in tagged_data_list]

## print "Data is read! " 

# Randomize training and evaluation set
random.seed(len(tagged_data_list)) 
random.shuffle(tagged_data_list) 
cutoff = int(development_size*train)

# Training set
training_data = tagged_data_list[:cutoff] 

# Evaluation set
evaulation_data = tagged_data_list[cutoff:development_size] 
 
# print "Data is splitted!" 


# Regular expression tagger
nn_cd_tagger = tag.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'PUNC'), (r'.*', 'NOUN_NOM')])


# Unigram tagger 
unigram_tagger = tag.UnigramTagger(training_data, backoff=nn_cd_tagger) 
print("Unigram accuracy: ")
print(unigram_tagger.evaluate(evaulation_data))

# Bigram tagger 
bigram_tagger = tag.BigramTagger(training_data, backoff=unigram_tagger)
print("Bigram accuracy: ")
print(bigram_tagger.evaluate(evaulation_data))

# Trigram tagger 
trigram_tagger = tag.TrigramTagger(training_data, backoff=bigram_tagger)
print("Trigram accuracy: ")
print(trigram_tagger.evaluate(evaulation_data))

# Brill tagger templates
templates = brill.fntbl37()

# First iteration
trainer = brill_trainer.BrillTaggerTrainer(trigram_tagger, templates)
brill_tagger = trainer.train(training_data, max_rules, min_score) 
print("Initial Brill accuracy:")
print(brill_tagger.evaluate(evaulation_data))

# 10 Folding
for i in range(1,5):

    # Random splitting
    random.seed(len(tagged_data_list)) 
    random.shuffle(tagged_data_list,random.random) 
    cutoff = int(development_size*train) 
    training_data = tagged_data_list[:cutoff] 
    evaulation_data = tagged_data_list[cutoff:development_size] 
     
    print("Fold: ")
    print(i)

    # Training
    brill_tagger = trainer.train(training_data, max_rules, min_score) 

    # Evaluation 
    print("Accuracy: ")
    print(brill_tagger.evaluate(evaulation_data))

    i = i+1

# Saving my tagger
pickle.dump(brill_tagger, open('my_tagger.txt','wb'))

print("Done!")

# End of code
