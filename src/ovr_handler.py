from nltk import compat
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction import DictVectorizer
from sklearn import cross_validation

class OvrHandler():
    def __init__(self, featuresets):
        self.mlb = MultiLabelBinarizer()
        self.featuresets = featuresets
        self.training_featuresets, self.testing_sets = self.split_list(featuresets)
        self._vectorizer = DictVectorizer(dtype=float, sparse=True)
        self.classifier = OneVsRestClassifier(MultinomialNB())

    def split_list(self, featuresets):
        half = int(len(featuresets)/2)
        length = int(len(featuresets))
        training_length = int(length / 100 * 80)
        testing_length =  length - training_length

        return featuresets[:training_length], featuresets[testing_length:]

    def prepare_scikit_x_and_y(self, labeled_featuresets):
        X, y = list(compat.izip(*labeled_featuresets))
        X = self._vectorizer.fit_transform(X)

        set_of_labels = []
        for label in y:
            set_of_labels.append(set(label))

        y = self.mlb.fit_transform(set_of_labels)

        return X, y

    def train_classifier(self):
        X, y = self.prepare_scikit_x_and_y(self.featuresets)
        self.classifier.fit(X, y)

    def test_classifier(self):
        X, y = self.prepare_scikit_x_and_y(self.featuresets)
        scores = cross_validation.cross_val_score(
            self.classifier, X, y, cv=10
        )
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    def predict_for_random(self, doc_with_bag_of_words):
        doc, bag_of_words = doc_with_bag_of_words
        print("Predicting for:", doc.title)
        print("Item is labeled to:")
        current_labels = []
        for subtopic in doc.subtopics:
            current_labels.append(subtopic.topic.title)

        print(set(current_labels))
        print("====> Predictions:")

        X = self._vectorizer.fit_transform(bag_of_words)
        predicted_labels = (self.classifier.predict(X))[0]
        probabilities =  self.classifier.predict_proba(X)[0]
        named_classes = self.mlb.classes_

        if not 1 in predicted_labels:
            print("No label suggested for item")
            return

        for idx, label in enumerate(predicted_labels):
            confidence = round(float(probabilities[idx] * 100), 2)
            if confidence > 10:
                print(named_classes[idx] + " - Confidence: ", end="")
                print(str(confidence) + "%")
