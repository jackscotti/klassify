from src.doc_operator import DocumentOperator
from src.ovr_handler import OvrHandler

doc_op = DocumentOperator()
doc_op.build_feature_sets()

ovs = OvrHandler(doc_op.featuresets)
ovs.train_classifier()
ovs.test_classifier()
ovs.predict_for_random(doc_op.random_document())
