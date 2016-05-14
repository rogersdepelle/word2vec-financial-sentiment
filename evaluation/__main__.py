# ctrl + shift + F10
# libraries
import json
import os
import csv
from cProfile import run
from pprint import pprint


def compute_all_metrics(execution_id, path_input, path_output):
    from evaluation.metrics import accuracy, precision, recall, f1, specificity
    """
    Computes all metrics and persistes in a csv

    Args:
        execution_id (int): identifier of the execution
        path_input (string): path of the file that contains the classifications
        path_out (string): path of the file that will persist the metrics
    """

    # loading results
    with open(path_input) as data_file:
        data = json.load(data_file)

    # computing metrics
    tp = tn = fp = fn = 0
    for id_news in data:
        if (data[id_news]["mean_max"]["positive"] > data[id_news]["mean_max"]["negative"]):
            if (data[id_news]["label"] == "positive"):
                tp += 1
            else:
                fp += 1
        elif data[id_news]["mean_max"]["positive"] < data[id_news]["mean_max"]["negative"]:
            if (data[id_news]["label"] == "negative"):
                tn += 1
            else:
                fn += 1
        else:
            raise Exception("Positive similarity equals to negative similarity to news " + id_news)

    accuracy = accuracy(tp, tn, fp, fn)
    recall = recall(tp, fn)
    precision = precision(tp, fp)
    f1 = f1(precision, recall);
    specificity = specificity(tn, fp);

    # persiting the results
    with open(path_output, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(
            ['execution_id', 'tp', 'tn', 'fp', 'fn', 'accuracy', 'precision', 'recall', 'f1', 'specificity'])
        spamwriter.writerow([execution_id, tp, tn, fp, fn, accuracy, precision, recall, f1, specificity])


compute_all_metrics(1, os.getcwd() + '/../tests/evaluation/output_step_03.json',
                os.getcwd() + '/../tests/evaluation/output_step_04.csv')
