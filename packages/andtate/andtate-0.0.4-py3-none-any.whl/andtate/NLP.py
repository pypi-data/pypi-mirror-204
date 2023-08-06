################### Tokenization using Python’s split() function ###################
################### P1A ###################

#Word tokenization
text = """Founded in 2002, SpaceX’s mission is to enable humans to become a spacefaring civilization and a multi-planet species by building a self-sustaining city on Mars. In 2008, SpaceX’s Falcon 1 became the first privately developed liquid-fuel launch vehicle to orbit the Earth."""
# Splits at space 
a=text.split()
print(a)

#Sentence Tokenization
text = """Founded in 2002, SpaceX’s mission is to enable humans to become a spacefaring civilization and a multi-planet species by building a self-sustaining city on Mars. In 2008, SpaceX’s Falcon 1 became the first privately developed liquid-fuel launch vehicle to orbit the Earth."""
# Splits at '.' 
text.split('. ')

################### Tokenization using Regular Expressions (RegEx) ###################
################### P1B ###################

#Word Tokenization
import re
text = """Founded in 2002, SpaceX’s mission is to enable humans to become a spacefaring civilization and a multi-planet species by building a self-sustaining city on Mars. In 2008, SpaceX’s Falcon 1 became the first privately developed liquid-fuel launch vehicle to orbit the Earth."""
tokens = re.findall("[\w']+", text)
print(tokens)

#Sentence Tokenization
import re
text = """Founded in 2002, SpaceX’s mission is to enable humans to become a spacefaring civilization and a multi-planet species by building a self-sustaining city on, Mars. In 2008, SpaceX’s Falcon 1 became the first privately developed liquid-fuel launch vehicle to orbit the Earth."""
sentences = re.compile('[.!?] ').split(text)
sentences

################### Tokenization using NLTK ###################
################### P1C ###################

#Word Tokenization
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize 
text = """Founded in 2002, SpaceX’s mission is to enable humans to become a spacefaring civilization and a multi-planet species by building a self-sustaining city on Mars. In 2008, SpaceX’s Falcon 1 became the first privately developed liquid-fuel launch vehicle to orbit the Earth."""
a=word_tokenize(text)
print(a)

#Sentence Tokenization
from nltk.tokenize import sent_tokenize
text = """Founded in 2002, SpaceX’s mission is to enable humans to become a spacefaring civilization and a multi-planet species by building a self-sustaining city on Mars. In 2008, SpaceX’s Falcon 1 became the first privately developed liquid-fuel launch vehicle to orbit the Earth."""
sent_tokenize(text)

################### Tokenization using the spaCy library ###################
################### P1D ###################

# Word Tokenization
from spacy.lang.en import English
# Load English tokenizer, tagger, parser, NER and word vectors
nlp = English()
text = """Founded in 2002, U.S.A. SpaceX’s mission is to enable humans to become a spacefaring civilization and a multi-planet species by building a self-sustaining city on Mars. In 2008, SpaceX’s Falcon 1 became the first privately developed liquid-fuel launch vehicle to orbit the Earth."""

#  "nlp" Object is used to create documents with linguistic annotations.
my_doc = nlp(text)
# Create list of word tokens
token_list = []
for token in my_doc:
    token_list.append(token.text)
token_list

#Sentence Tokenization
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("""Founded in 2002, SpaceX’s mission is to enable humans to become a spacefaring civilization and a multi-planet species by building a self-sustaining city on Mars. In 2008, SpaceX’s Falcon 1 became the first privately developed liquid-fuel launch vehicle to orbit the Earth.""")
for sent in doc.sents:
  print(sent.text)

################### Tokenization using Gensim ###################
################### P1E ###################

#Word Tokenization
from gensim.utils import tokenize
text="""On January 12, 1958, NACA organized a "Special Committee on Spa
ce Technology", headed by Guyford Stever.[7] On January 14, 1958, NACA
Director Hugh Dryden published "A National Research Program for Space T
echnology", stating,[45]
It is of great urgency and importance to our country."""
list(tokenize(text))

#Sentence Tokenization
from gensim.summarization.textcleaner import split_sentences
text = """Beginning in 1946, the National Advisory Committee for Aeronauti
cs (NACA) began experimenting with rocket planes such as the supersonic Be
ll X1.[43] In the early 1950s, there was challenge to launch an artificial sat
ellite for the International Geophysical Year """
result = split_sentences(text)
result

################### Write a program to Implement stemming and lemmatization ###################
################### P2 ###################

#Stemming LancasterStemmer
import nltk
from nltk.stem import LancasterStemmer
lancaster_stemmer  = LancasterStemmer()
text = "studies studying cries cry"
tokenization = nltk.word_tokenize(text)
for w in tokenization:
  print("Stemming for {} is - {}".format(w,lancaster_stemmer.stem(w)))


#Stemming PorterStemmer
import nltk
from nltk.stem.porter import PorterStemmer
porter_stemmer  = PorterStemmer()
text = "Pythoners are very intelligent and work very pythonly"
tokenization = nltk.word_tokenize(text)
for w in tokenization:
  print("Stemming for {} is - {}".format(w,porter_stemmer.stem(w)))


#Stemming SnowballStemmer
nltk.download('stopwords')
from nltk.stem import SnowballStemmer
snowball = SnowballStemmer(language='english', ignore_stopwords=True)
words = ['generous','generate','generously','generation','having']
for word in words:
    print(word,"--->",snowball.stem(word))

#Lemmatizaion NLTK
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
text = "The striped bats are hanging on their feet for best"
tokenization = nltk.word_tokenize(text)
for w in tokenization:
  print("{0:20}{1:20}".format(w, wordnet_lemmatizer.lemmatize(w))) 


#Lemmatizaion Spacy
#python -m spacy download en_core_web_sm  #For IDLE
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("eating eats eat ate ability adjustable rafting meeting better")
for token in doc:
    print(token, " | ", token.lemma_, " | ", token.lemma)


################### Write a program to Implement a tri-gram model ###################
################### P3 ###################

#N-gram Language Model
import nltk
nltk.download('reuters')
nltk.download('punkt')
from nltk.corpus import reuters
from nltk import bigrams, trigrams
from collections import Counter, defaultdict
# Create a placeholder for model
model = defaultdict(lambda: defaultdict(lambda: 0))
# Count frequency of co-occurance  
for sentence in reuters.sents():
    for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
        model[(w1, w2)][w3] += 1
# Let's transform the counts to probabilities
for w1_w2 in model:
    total_count = float(sum(model[w1_w2].values()))
    for w3 in model[w1_w2]:
        model[w1_w2][w3] /= total_count


dict(model["today", "the"])
#.................................................................................#

#Generating a random piece of text using above n-gram model
import random
# starting words
text = ["today", "the"]
sentence_finished = False
 
while not sentence_finished:
  # select a random probability threshold  
  r = random.random()
  accumulator = .0

  for word in model[tuple(text[-2:])].keys():
      accumulator += model[tuple(text[-2:])][word]
      # select words that are above the probability threshold
      if accumulator >= r:
          text.append(word)
          break

  if text[-2:] == [None, None]:
      sentence_finished = True
 
print (' '.join([t for t in text if t]))

################### Write a program to Implement a POS tagging using HMM ###################
################### P4 ###################

################### Write a program to Implement syntactic parsing of a given text ###################
################### P5 ###################


# Import required libraries
import nltk
nltk.download('punkt')          #pre-trained Punkt tokenizer, which is used to tokenize the words.
nltk.download('averaged_perceptron_tagger')       #averaged_perceptron_tagger: is used to tag those tokenized words to Parts of Speech
from nltk import pos_tag, word_tokenize, RegexpParser
  
# Example text
sample_text = "Reliance Retail acquires majority stake in designer brand Abraham & Thakore."
  
# Find all parts of speech in above sentence
tagged = pos_tag(word_tokenize(sample_text))
  
#Extract all parts of speech from any text
chunker = RegexpParser("""
                       NP: {<DT>?<JJ>*<NN>}    #To extract Noun Phrases
                       P: {<IN>}               #To extract Prepositions
                       V: {<V.*>}              #To extract Verbs
                       PP: {<p> <NP>}          #To extract Prepositional Phrases
                       VP: {<V> <NP|PP>*}      #To extract Verb Phrases
                       """)
 
# Print all parts of speech in above sentence
output = chunker.parse(tagged)
print("After Extracting\n", output)
#output.draw()  #Only works on IDLE


################### Write a program to Implement dependency parsing of a given text ###################
################### P6 ###################

import spacy

# Loading the model
nlp=spacy.load('en_core_web_sm')
text = "Reliance Retail acquires majority stake in designer brand Abraham & Thakore."

# Creating Doc object
doc=nlp(text)
print ("{:<15} | {:<8} | {:<15} | {:<20}".format('Token','Relation','Head', 'Children'))
print ("-" * 70)	

for token in doc:
  # Print the token, dependency nature, head and all dependents of the token
  print ("{:<15} | {:<8} | {:<15} | {:<20}"
         .format(str(token.text), str(token.dep_), str(token.head.text), str([child for child in token.children])))

#.................................................................................#
# Importing visualizer
from spacy import displacy

# Visualizing dependency tree
displacy.render(doc, style='dep', jupyter=True, options={'distance': 120})


################### Write a program to implement Named Entity Recognition (NER) ###################
################### P7 ###################

sentence = 'Peterson first suggested the name "open source" at Palo Alto, California'

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

words = nltk.word_tokenize(sentence)
pos_tagged = nltk.pos_tag(words)

# maxent_ne_chunker contains two pre-trained English named entity chunkers trained on an ACE corpus.
nltk.download('maxent_ne_chunker') 
nltk.download('words')

ne_tagged = nltk.ne_chunk(pos_tagged)
print("NE tagged text:")
print(ne_tagged)
print()

print("Recognized named entities:")
for ne in ne_tagged:
    if hasattr(ne, "label"):
        print(ne.label(), ne[0:])
#ne_tagged.draw() #Only works on IDLE


#Implement Ner Using Spacy
import spacy
from spacy import displacy
NER = spacy.load("en_core_web_sm")
raw_text="The Indian Space Research Organisation or is the national space agency of India, headquartered in Bengaluru. It operates under Department of Space which is directly overseen by the Prime Minister of India while Chairman of ISRO acts as executive of DOS as well."
text1= NER(raw_text)
for word in text1.ents:
    print(word.text,word.label_)

#.......................................................................#
displacy.render(text1,style="ent",jupyter=True) 


################### Write a program to Implement Text Summarization for the given sample text ###################
################### P8 ###################

#using nltk library
nltk.download('stopwords')

# importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
   
# Input text - to summarize 
text = """There are many techniques available to generate extractive summarization to keep it simple, I will be using an unsupervised learning approach to find the sentences similarity and rank them. Summarization can be defined as a task of producing a concise and fluent summary while preserving key information and overall meaning. One benefit of this will be, you don’t need to train and build a model prior start using it for your project. It’s good to understand Cosine similarity to make the best use of the code you are going to see. Cosine similarity is a measure of similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them. Its measures cosine of the angle between vectors. The angle will be 0 if sentences are similar. """
   
# Tokenizing the text
stopWords = set(stopwords.words("english"))
words = word_tokenize(text)
   
# Creating a frequency table to keep the 
# score of each word
   
freqTable = dict()
for word in words:
    word = word.lower()
    if word in stopWords:
        continue
    if word in freqTable:
        freqTable[word] += 1
    else:
        freqTable[word] = 1
   
# Creating a dictionary to keep the score
# of each sentence
sentences = sent_tokenize(text)
sentenceValue = dict()
   
for sentence in sentences:
    for word, freq in freqTable.items():
        if word in sentence.lower():
            if sentence in sentenceValue:
                sentenceValue[sentence] += freq
            else:
                sentenceValue[sentence] = freq
  
sumValues = 0
for sentence in sentenceValue:
    sumValues += sentenceValue[sentence]
   
# Average value of a sentence from the original text
   
average = int(sumValues / len(sentenceValue))
   
# Storing sentences into our summary.
summary = ''
for sentence in sentences:
    if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
        summary += " " + sentence
print("Original String\n"+ text)
print("\n\nSummarized text\n"+ summary)


#using Spacy Library
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

doc ="""Machine learning (ML) is the scientific study of algorithms and statistical models that computer systems use to progressively improve their performance on a specific task. Machine learning algorithms build a mathematical model of sample data, known as "training data", in order to make predictions or decisions without being explicitly programmed to perform the task. Machine learning algorithms are used in the applications of email filtering, detection of network intruders, and computer vision, where it is infeasible to develop an algorithm of specific instructions for performing the task. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a field of study within machine learning, and focuses on exploratory data analysis through unsupervised learning.In its application across business problems, machine learning is also referred to as predictive analytics."""
nlp = spacy.load('en_core_web_sm')
doc = nlp(doc)
len(list(doc.sents)) # to find the number of sentences in the given string

#..............................................................................#
keyword = []
stopwords = list(STOP_WORDS)
pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
for token in doc:
    if(token.text in stopwords or token.text in punctuation):
        continue
    if(token.pos_ in pos_tag):
        keyword.append(token.text)
#Calculating frequency of each token using the Counter function
freq_word = Counter(keyword)
print(freq_word.most_common(5))
type(freq_word)

#..............................................................................#
#Normalization
max_freq = Counter(keyword).most_common(1)[0][1]
for word in freq_word.keys():  
        freq_word[word] = (freq_word[word]/max_freq)
freq_word.most_common(5)

#..............................................................................#
#Weighing sentences
sent_strength={}
for sent in doc.sents:
    for word in sent:
        if word.text in freq_word.keys():
            if sent in sent_strength.keys():
                sent_strength[sent]+=freq_word[word.text]
            else:
                sent_strength[sent]=freq_word[word.text]
print(sent_strength)

#..............................................................................#
#Summarizing the string
summarized_sentences = nlargest(3, sent_strength, key=sent_strength.get)
print(summarized_sentences)
print(type(summarized_sentences[0]))
final_sentences = [ w.text for w in summarized_sentences ]
summary = ' '.join(final_sentences)
print(summary)