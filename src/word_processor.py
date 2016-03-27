from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

class WordProcessor():
    def __init__(self, documents):
        self.documents = documents
        self.stemmer = PorterStemmer()
        self.vocabulary = self.top_words(self.freq_dist(self.make_vocabulary()))

    def tokenize(self, document=None):
        '''
        Take all documents content, tokenize it and put it in a `contents` variable
        '''
        if document:
            documents = [document]
        else:
            documents = self.documents

        return [token for doc in documents for token in word_tokenize(doc.content)]

    def process(self, vocabulary):
        ADDITIONAL_STOP_WORDS = {"-", ".", ",", "if", "good", "what", "within", "https", ".mb"}
        stop_words = set(stopwords.words("english"))

        processed_words = []

        for word in vocabulary:
            # select only words shorter than 20 char
            if len(word) < 20:
                word = word.lower()
                # do not select stopwords
                if word not in (stop_words | ADDITIONAL_STOP_WORDS):
                    # stem words
                    word = self.stemmer.stem(word)
                    # do not select words shorter than 2 characters
                    if word.isalpha:
                        if len(word) > 1:
                            processed_words.append(word)
                    else:
                        processed_words.append(word)

        return processed_words

    def make_vocabulary(self, document=None):
        if document:
            vocabulary = self.tokenize(document)
        else:
            vocabulary = self.tokenize()

        vocabulary = self.process(vocabulary)

        return vocabulary

    def bag_of_words(self, document):
        doc_words = set(self.make_vocabulary(document))
        bag_of_words = {}

        for word in self.vocabulary:
            bag_of_words[word] = (word in doc_words)

        return bag_of_words

    def freq_dist(self, vocabulary):
        return nltk.FreqDist(vocabulary)

    def top_words(self, freq_dist, number=500):
        # problem number one: this creates a long list
        # number of features needs to be reduced
        return list(freq_dist.keys())[:number]
