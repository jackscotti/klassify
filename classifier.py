from src.doc_operator import DocumentOperator
from src.ovr_handler import OvrHandler

doc_op = DocumentOperator()
doc_op.build_feature_sets()

ovs = OvrHandler(doc_op.featuresets)
ovs.train_classifier()
ovs.test_classifier()

# import pdb; pdb.set_trace()
ovs.predict_for_random(doc_op.random_document())

# TODO
# - Select only topics with most documents
# - Use pickle and store files somewhere
# - split training/testing data 80-20 http://stackoverflow.com/questions/13610074/is-there-a-rule-of-thumb-for-how-to-divide-a-dataset-into-training-and-validatio http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.33.1337&rep=rep1&type=pdf https://en.wikipedia.org/wiki/Pareto_principle
# - add scikit to requirements
