from src.doc_operator import DocumentOperator
from src.ovr_handler import OvrHandler

count = 0

while count < 1:
    doc_op = DocumentOperator(n=5, min_docs=400, max_docs=500)
    doc_op.build_feature_sets()

    ovs = OvrHandler(doc_op.featuresets)
    ovs.train_classifiers()
    ovs.test_classifiers()
    count += 1

ovs.predict_for_random(doc_op.random_document())

# TODO
# - split training/testing data 80-20 http://stackoverflow.com/questions/13610074/is-there-a-rule-of-thumb-for-how-to-divide-a-dataset-into-training-and-validatio http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.33.1337&rep=rep1&type=pdf https://en.wikipedia.org/wiki/Pareto_principle
# - replace synonims
# - Replacing negations with antonyms
