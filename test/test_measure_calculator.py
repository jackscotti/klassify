from klassify.src.measure_calculator import MeasureCalculator
from klassify.src.tables import Topic, Subtopic

first_set = {
    "BernoulliNB": { "cross score": 3, "precision": 1, "cross variance": 1 },
    "MultinomialNB": { "cross score": 2, "precision": 2, "cross variance": 2 }
}
second_set = {
    "BernoulliNB": {"recall": 3, "f1": 1},
    "MultinomialNB": {"recall": 2, "f1": 2}
}

# Groups two sets of measures by the algorithm type
def test_combine_measures():
    CALC = MeasureCalculator()

    assert CALC.combine_measures(first_set, second_set) == {
        "BernoulliNB": {"cross score": 3, "precision": 1, "recall": 3, "f1": 1, "cross variance": 1},
        "MultinomialNB": {"cross score": 2, "precision": 2, "recall": 2, "f1": 2, "cross variance": 2}
    }

# Store sets of measures
def test_add_measures():
    CALC = MeasureCalculator()

    CALC.add_measures(first_set, second_set)

    assert CALC.measures == {
        "BernoulliNB": {"cross score": [3], "precision": [1], "recall": [3], "f1": [1], "cross variance": [1]},
        "MultinomialNB": {"cross score": [2], "precision": [2], "recall": [2], "f1": [2], "cross variance": [2]}
    }
