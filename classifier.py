from src.doc_operator import DocumentOperator
from src.ovr_handler import OvrHandler
import time

class MeasureCalculator():
    def __init__(self):
        self.measures = {
            "BernoulliNB": {"cross score": [], "cross variance": [], "precision": [], "recall": [], "f1": []},
            "MultinomialNB": {"cross score": [], "cross variance": [], "precision": [], "recall": [], "f1": []}
        }

    def add_results(self, cross_validation_results, accuracy_results):
        measures = self.combine_results(cross_validation_results, accuracy_results)
        for algo_type, results in measures.items():
            for result, value in results.items():
                self.measures[algo_type][result].append(value)

    def combine_results(self, cross_validation_results, accuracy_results):
        current_measures = {}
        current_measures["BernoulliNB"] =  dict(list(cross_validation_results["BernoulliNB"].items())
            + list(accuracy_results["BernoulliNB"].items()))
        current_measures["MultinomialNB"] =  dict(list(cross_validation_results["MultinomialNB"].items())
            + list(accuracy_results["MultinomialNB"].items()))
        return current_measures

    def averaged_results(self):
        for algo_type, results in self.measures.items():
            print(algo_type + ":")
            cross_score = (sum(results["cross score"]) / len(results["cross score"]))
            cross_precision = (sum(results["cross variance"]) / len(results["cross variance"]))
            print("Cross evaluation accuracy: %1.3f (+/- %1.3f)" % (cross_score, cross_precision))
            results.pop("cross score")
            results.pop(("cross variance"))

            for result, values in results.items():
                print("%s: %1.3f" % (result, (sum(values) / len(values))))

calc = MeasureCalculator()
start_time = time.time()
count = 1
while count <= 20:
    print("#%d:" % count)
    doc_op = DocumentOperator(n=5, min_docs=400, max_docs=400, n_features=7500)
    doc_op.build_feature_sets()

    ovs = OvrHandler(doc_op.featuresets)

    cross_validation_results = ovs.cross_validate()
    accuracy_results = ovs.calculate_accuracy()

    calc.add_results(cross_validation_results, accuracy_results)

    count += 1

calc.averaged_results()

print("Total time: %0.2fs " % (time.time() - start_time))
