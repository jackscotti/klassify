from src.doc_operator import DocumentOperator
from src.ovr_handler import OvrHandler
import time

all_results = {
    "BernoulliNB": {"cross score": [], "cross variance": [], "precision": [], "recall": [], "f1": []},
    "MultinomialNB": {"cross score": [], "cross variance": [], "precision": [], "recall": [], "f1": []}
}

def add_results(base, to_add):
    for algo_type, results in to_add.items():
        for result, value in results.items():
            base[algo_type][result].append(value)
    return base

def calculate_averages(all_results):
    for algo_type, results in all_results.items():
        print(algo_type + ":")
        cross_score = (sum(results["cross score"]) / len(results["cross score"]))
        cross_precision = (sum(results["cross variance"]) / len(results["cross variance"]))
        print("Cross evaluation accuracy: %1.3f (+/- %1.3f)" % (cross_score, cross_precision))
        results.pop("cross score")
        results.pop(("cross variance"))

        for result, values in results.items():
            print("%s: %1.3f" % (result, (sum(values) / len(values))))

start_time = time.time()
count = 1
while count <= 100:
    print("#%d:" % count)
    doc_op = DocumentOperator(n=10, min_docs=200, max_docs=200, n_features=10000)
    doc_op.build_feature_sets()

    ovs = OvrHandler(doc_op.featuresets)

    test_results = ovs.test_classifiers()
    accuracy_results = ovs.calculate_accuracy()
    to_add = {}
    to_add["BernoulliNB"] =  dict(list(test_results["BernoulliNB"].items()) + list(accuracy_results["BernoulliNB"].items()))
    to_add["MultinomialNB"] =  dict(list(test_results["MultinomialNB"].items()) + list(accuracy_results["MultinomialNB"].items()))
    all_results = add_results(all_results, to_add)
    count += 1

calculate_averages(all_results)

print("Total time: %0.2fs " % (time.time() - start_time))
