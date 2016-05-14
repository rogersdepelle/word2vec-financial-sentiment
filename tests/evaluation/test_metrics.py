from evaluation.metrics import accuracy, precision, recall, specificity, f1

__author__      = "Edimar Manica"

from unittest import TestCase



class TestMetrics(TestCase):

    def test_accuracy(self):
        assert accuracy(tp=4, tn=3, fp=2, fn=1) == 0.7

    def test_precision(self):
        assert round(precision(tp=4, fp=2), 3) == 0.667

    def test_recall(self):
        assert recall(tp=4, fn=1) == 0.8

    def test_specificity(self):
        assert specificity(tn=3, fp=2) == 0.6

    def test_f1(self):
        assert round(f1(p=0.667, r=0.8), 3) == 0.727
