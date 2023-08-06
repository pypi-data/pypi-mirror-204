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
