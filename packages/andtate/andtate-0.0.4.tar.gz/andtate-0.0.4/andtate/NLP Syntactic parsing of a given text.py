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