from src.db_handler import DBHandler
from src.tables import Topic, Subtopic, Document
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

DBH = DBHandler(echo=False)

topics = DBH.session.query(Topic).all()
def find_documents_for_topic(topic):
    documents = []
    for subtopic in topic.subtopics:
        for document in subtopic.documents:
            documents.append(document)

    return documents

document_sets = []
for topic in topics:
    document_sets.append(find_documents_for_topic(topic))

class Classifier():
    def __init__(self, documents):
        self.documents = documents
        self.stemmer = PorterStemmer()
        self.words = []
        self.features = []

    def extract_words(self):
        '''
        Take all documents content, tokenize it and put it in a `contents` variable
        '''
        for doc in self.documents:
            # tokenize
            tokens = word_tokenize(doc.content)

            for token in tokens:
                self.words.append(token)

    def downcase_words(self, words):
        return [w.lower() for w in words]

    def remove_stopwords(self, words):
        # remove stop words
        ADDITIONAL_STOP_WORDS = {"-", ".", ",", "if", "good", "what", "within", "https"}
        stop_words = set(stopwords.words("english"))
        return [w for w in words if not w in (stop_words | ADDITIONAL_STOP_WORDS)]

    def stem_words(self, words):
        # stem
        return [self.stemmer.stem(w) for w in words]

    def remove_long_words(self, words):
        # remove anything that is not a word (js script that haven't been removed by previous parsing)
        return [w for w in words if len(w) < 25]

    def extract_features(self):
        self.extract_words()

        words = self.downcase_words(self.words)
        words = self.remove_stopwords(words)
        words = self.stem_words(words)
        words = self.remove_long_words(words)

        return words

for document_set in document_sets:
    print(document_set[0].title)
    c = Classifier(document_set)
    features = c.extract_features()
    print("Number of features:", len(features))
    # Convert in nltk frequency distribution object
    all_words = nltk.FreqDist(features)
    # print 15 most common words
    print(all_words.most_common(15))

    # top 3000 words
    word_features = list(all_words.keys())[:3000]

def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

# print(find_features(documents[0].content))

# import pdb; pdb.set_trace()
'''
http://scikit-learn.org/stable/modules/multiclass.html
Multilabel classification assigns to each sample a set of target labels. This can be thought as predicting properties of a data-point that are not mutually exclusive, such as topics that are relevant for a document. A text might be about any of religion, politics, finance or education at the same time or none of these.
http://scikit-learn.org/stable/auto_examples/plot_multilabel.html
'''
