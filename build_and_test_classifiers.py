# Appendix C8 - build_and_train_classifiers.py

from src.doc_operator import DocumentOperator
from src.ovr_handler import OvrHandler
from src.measure_calculator import MeasureCalculator
import time

# Install nltk modules
import nltk
nltk.download('punkt')
nltk.download('stopwords')

calc = MeasureCalculator()
start_time = time.time()

count = 1
while count <= 100:
    doc_op = DocumentOperator(n=5, min_docs=400, max_docs=400, n_features=7500)
    doc_op.build_feature_sets()

    ovs = OvrHandler(doc_op.featuresets)

    cross_validation_measures = ovs.cross_validate()
    accuracy_measures = ovs.calculate_accuracy()

    calc.add_measures(cross_validation_measures, accuracy_measures)

    count += 1

calc.averaged_measures()

print("Total time: %0.2fs " % (time.time() - start_time))
