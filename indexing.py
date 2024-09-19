#-------------------------------------------------------------------------
# AUTHOR: Brandon Tang
# FILENAME: indexing.py
# SPECIFICATION: The program will read the file collection.csv and output the tf-idf document-term matrix with the requirements of question 7.
# FOR: CS 4250- Assignment #1
# TIME SPENT: 3 hours
#-----------------------------------------------------------*/

#Importing some Python libraries
import csv
import math
from collections import defaultdict

#Reading the data in a csv file
documents = []
with open('collection.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i > 0:  # skipping the header
            documents.append (row[0])

#Conducting stopword removal for pronouns/conjunctions. Hint: use a set to define your stopwords.
#--> add your Python code here
stopWords = {"i", "me", "my", "we", "you", "he", "she", "him", "her", "it", "they", "their", "this", "that", "is", "are", "was", "were", "be", "has", "have", "had", "and", "or", "but"}

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
stemming = {
    "cats" : "cat",
    "dogs" : "dog",
    "loves" : "love", 
    "loving" : "love"
}

# Process the documents (stopword removal and stemming)
processed_documents = []
for doc in documents:
    words = doc.split()
    filtered_stemmed_words = []
    for word in words:
        lower_word = word.lower()
        if lower_word not in stopWords:
            # Apply stemmming if word has a stem
            stemmed_word = stemming.get(lower_word, lower_word)
            filtered_stemmed_words.append(stemmed_word)
    processed_documents.append(filtered_stemmed_words)

#Identifying the index terms.
#--> add your Python code here
terms = set()
for doc in processed_documents:
    for word in doc:
        terms.add(word)
        
terms = sorted(terms) # Sort the terms


# Calculate the term frequency (TF)
tf = []
for doc in processed_documents:
    term_freq = defaultdict(int)
    total_terms = len(doc)
    for word in doc:
        term_freq[word] += 1
        
    tf.append({term: count / total_terms for term, count in term_freq.items()})
    
    
# Calculate inverse document frequency (IDF)
idf = {}
total_documents = len(processed_documents)
for term in terms:
    doc_count = sum(1 for doc in processed_documents if term in doc)
    idf[term] = math.log10((total_documents + 1) / (1 + doc_count))


#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here
docTermMatrix = []
for doc_tf in tf:
    doc_tfidf = []
    for term in terms:
        tf_value = doc_tf.get(term, 0)      # Term frequency
        idf_value = idf.get(term, 0)        # Inverse document frequency
        doc_tfidf.append(tf_value * idf_value)
    docTermMatrix.append(doc_tfidf)

#Printing the document-term matrix.
#--> add your Python code here
print(f"{'Document':<10} {' '.join([f'{term:<10}' for term in terms])}")
for i, row in enumerate(docTermMatrix):
    print(f"Document {i+1:<3} {' '.join(f'{value:<10.3f}' for value in row)}")