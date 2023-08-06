import nltk
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
vectorizer = TfidfVectorizer(stop_words='english')

# def extract_related_sentences(text, keyword=None, num_sentences=3):
#
#     if text.strip()=="":
#         return text
#     if keyword==None:
#         return text
#     # tokenize sentences and convert to lowercase
#     origin_sentences = nltk.sent_tokenize(text)
#     sentences = [sentence.lower() for sentence in origin_sentences]
#
#     # create TF-IDF vectorizer
#
#     # fit and transform the sentences into TF-IDF vectors
#     tfidf_vectors = vectorizer.fit_transform(sentences)
#
#     # compute cosine similarity between the keyword and each sentence
#     keyword_vector = vectorizer.transform([keyword.lower()])
#     cos_similarities = cosine_similarity(tfidf_vectors, keyword_vector).flatten()
#
#     # extract top 3 sentences with highest cosine similarity to the keyword
#     related_sentences = [origin_sentences[i] for i in cos_similarities.argsort()[::-1][:num_sentences]]
#     related_sentences = " ".join(related_sentences)
#     print(related_sentences)
#     return related_sentences


import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

from sklearn.metrics.pairwise import cosine_similarity


def extract_related_sentences2(text,keyword,related_words_num=2):

    # nltk.download('wordnet')

    # Tokenize the text and remove stop words
    stop_words = set(stopwords.words('english'))
    sentences = text.split(".")
    lemmatizer = WordNetLemmatizer()

    corpus = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [lemmatizer.lemmatize(word.lower()) for word in words if
                 word.isalpha() and word.lower() not in stop_words]
        corpus.append(" ".join(words))

    # Extract related words

    # Define the corpus of text and the keyword
    processed_corpus = []
    for document in corpus:
        words = nltk.word_tokenize(document.lower())
        words = [lemmatizer.lemmatize(word) for word in words if word.isalpha() and word not in stop_words]
        processed_sents = " ".join(words).replace(keyword, keyword.replace(" ", "_"))
        processed_corpus.append(processed_sents)

    # Create a TF-IDF matrix
    vectorizer = TfidfVectorizer(max_features=1000)

    tfidf_matrix = vectorizer.fit_transform(processed_corpus)
    # Perform LSA
    lsa = TruncatedSVD(n_components=100, random_state=42)
    lsa_matrix = lsa.fit_transform(tfidf_matrix)

    # Identify related terms
    term_matrix = vectorizer.transform([keyword.replace(" ", "_")])
    term_vector = lsa.transform(term_matrix)

    similarities = cosine_similarity(term_vector, lsa_matrix)
    related_indices = similarities.argsort()[0][:related_words_num]

    related_terms = [vectorizer.get_feature_names_out()[i] for i in related_indices]

    print("Related terms for '{}': {}".format(keyword, ", ".join(related_terms)))

    # Get the indices of the sentences containing the keywords
    keyword_indices = []
    keywords = [keyword] + related_terms
    for i, sentence in enumerate(sentences):
        for keyword in keywords:
            if keyword.lower() in sentence.lower():
                keyword_indices.append(i)

    # Extract the relevant content using LSA
    relevant_content = []
    indexes = []
    for i in keyword_indices:
        sentence = sentences[i]
        topic_vector = lsa_matrix[i]
        similarities = lsa_matrix.dot(topic_vector)
        similar_indices = similarities.argsort()[::-1][1:]
        top_sentence_index = similar_indices[0]
        if top_sentence_index not in indexes:
            top_sentence = sentences[top_sentence_index]
            relevant_content.append(top_sentence)
            indexes.append(top_sentence_index)
    return " . ".join(relevant_content) + " ."


import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_related_sentences(text, keyword=None, num_sentences=5):

    if keyword==None:
        return text
    # Split the text into sentences
    sentences = text.split(".")
    # Remove any leading/trailing white space from each sentence
    sentences = [s.strip() for s in sentences]
    # Initialize a TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    # Create a matrix of TF-IDF scores for each sentence
    sentence_matrix = vectorizer.fit_transform(sentences)
    # Get the index of the keyword in the feature vocabulary
    keyword_vector = vectorizer.transform([keyword.lower()])
    cos_similarities = cosine_similarity(sentence_matrix, keyword_vector).flatten()

    # extract top 3 sentences with highest cosine similarity to the keyword
    related_sentences = [sentences[i] for i in cos_similarities.argsort()[::-1][:num_sentences]]


    # Return the top N related sentences
    return " . ".join(related_sentences) + " ."
