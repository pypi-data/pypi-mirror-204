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
