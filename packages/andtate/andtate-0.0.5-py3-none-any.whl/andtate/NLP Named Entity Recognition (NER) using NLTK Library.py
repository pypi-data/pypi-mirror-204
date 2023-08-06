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