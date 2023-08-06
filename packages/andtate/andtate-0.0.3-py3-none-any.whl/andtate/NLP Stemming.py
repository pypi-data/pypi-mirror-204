#Stemming LancasterStemmer
import nltk
from nltk.stem import LancasterStemmer
lancaster_stemmer  = LancasterStemmer()
text = "studies studying cries cry"
tokenization = nltk.word_tokenize(text)
for w in tokenization:
  print("Stemming for {} is - {}".format(w,lancaster_stemmer.stem(w)))


#Lemmatization PorterStemmer
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
