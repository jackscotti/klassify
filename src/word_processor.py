from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

class WordProcessor():
    def __init__(self, documents):
        self.documents = documents
        self.stemmer = PorterStemmer()
        self.vocabulary = self.make_vocabulary()

    def extract_words(self, document=None):
        '''
        Take all documents content, tokenize it and put it in a `contents` variable
        '''
        if document:
            documents = [document]
        else:
            documents = self.documents

        words = []

        for doc in documents:
            # tokenize
            tokens = word_tokenize(doc.content)

            for token in tokens:
                words.append(token)
        return words

    def downcase_words(self, words):
        return [w.lower() for w in words]

    def remove_stopwords(self, words):
        # remove stop words
        ADDITIONAL_STOP_WORDS = {"-", ".", ",", "if", "good", "what", "within", "https", ".mb"}
        stop_words = set(stopwords.words("english"))
        return [w for w in words if not w in (stop_words | ADDITIONAL_STOP_WORDS)]

    def stem_words(self, words):
        # stem
        return [self.stemmer.stem(w) for w in words]

    def remove_long_words(self, words):
        # remove anything that is not a word (js script that haven't been removed by previous parsing)
        return [w for w in words if len(w) < 25]

    def remove_short_words(self, words):
        filtered_words = []
        for w in words:
            if w.isalpha:
                if len(w) > 1:
                    filtered_words.append(w)
            else:
                filtered_words.append(w)

        return filtered_words

    def make_vocabulary(self, document=None):
        if document:
            v = self.extract_words(document)
        else:
            v = self.extract_words()

        v = self.downcase_words(v)
        v = self.remove_stopwords(v)
        v = self.stem_words(v)
        v = self.remove_short_words(v)
        v = self.remove_long_words(v)

        return v

    def bag_of_words(self, document):
        vocabulary = self.top_words(self.freq_dist(self.vocabulary))

        doc_words = set(self.make_vocabulary(document))
        bag_of_words = {}

        for w in vocabulary:
            bag_of_words[w] = (w in doc_words)

        return bag_of_words

    def freq_dist(self, vocabulary):
        return nltk.FreqDist(vocabulary)

    def top_words(self, freq_dist, number=500):
        # problem number one: this creates a long list
        # number of features needs to be reduced
        return list(freq_dist.keys())[:number]
