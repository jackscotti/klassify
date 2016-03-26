from nltk import compat
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction import DictVectorizer

class OvrHandler():
    def __init__(self, featuresets):
        self.mlb = MultiLabelBinarizer()
        self.training_featuresets, self.testing_sets = self.split_list(featuresets)
        self._vectorizer = DictVectorizer(dtype=float, sparse=True)
        self.classifier = OneVsRestClassifier(MultinomialNB())

    def split_list(self, featuresets):
        half = int(len(featuresets)/2)
        length = int(len(featuresets))
        training_length = int(length / 100 * 90)
        testing_length =  int(length / 100 * 10)

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
        X, y = self.prepare_scikit_x_and_y(self.training_featuresets)
        self.classifier.fit(X, y)

    def test_classifier(self):
        try:
            X, y = self.prepare_scikit_x_and_y(self.testing_sets)
            print("Classifier accuracy against test data:", str(round(float(self.classifier.score(X, y) * 100), 2)) + "%")
        except Exception:
            # this raises because of inconsistent shapes, still need to find out why
            import pdb; pdb.set_trace()

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
            if predicted_labels[idx]:
                print(named_classes[idx] + " - Confidence: ", end="")
                print(str(round(float(probabilities[idx] * 100), 2)) + "%")
