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
        self._vectorizer = DictVectorizer(dtype=float, sparse=True)
        self.X, self.y = self.prepare_scikit_x_and_y(self.featuresets)
        self.classifier = OneVsRestClassifier(MultinomialNB())

    def prepare_scikit_x_and_y(self, labeled_featuresets):
        X, y = list(compat.izip(*labeled_featuresets))
        X = self._vectorizer.fit_transform(X)

        set_of_labels = []
        for label in y:
            set_of_labels.append(set(label))

        y = self.mlb.fit_transform(set_of_labels)

        return X, y

    def train_classifier(self):
        self.classifier.fit(self.X, self.y)

    def test_classifier(self):
        scores = cross_validation.cross_val_score(
            self.classifier, self.X, self.y, cv=10
        )
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    def predict_for_random(self, doc_with_bag_of_words):
        doc, bag_of_words = doc_with_bag_of_words
        print("Predicting for:", doc.title)
        print("Item is labeled to:")
        print(set(doc.topic_titles()))
        print("====> Predictions:")

        X = self._vectorizer.fit_transform(bag_of_words)
        predicted_labels = (self.classifier.predict(X))[0]
        probabilities =  self.classifier.predict_proba(X)[0]
        named_classes = self.mlb.classes_

        # If no labels are predicted for the item:
        if not 1 in predicted_labels:
            print("No label suggested for item")
            return

        for idx, label in enumerate(predicted_labels):
            confidence = round(float(probabilities[idx] * 100), 2)
            if confidence > 10:
                print(named_classes[idx] + " - Confidence: ", end="")
                print(str(confidence) + "%")
