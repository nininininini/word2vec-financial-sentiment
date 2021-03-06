__author__ = "Edimar Manica"

# libraries
import json
import os
import csv
from cProfile import run
from pprint import pprint


def compute_all_metrics(execution_id, path_input, path_output, formula, append):
    from metrics import accuracy, precision, recall, f1, specificity
    """
    Computes all metrics and persistes in a csv

    Args:
        execution_id (int): identifier of the execution
        path_input (string): path of the file that contains the classifications
        path_out (string): path of the file that will persist the metrics
        formula (string): mean_max | mean_mean
        append (boolean): true | false
    """

    # loading results
    with open(path_input) as data_file:
        data = json.load(data_file)

    # computing metrics
    tp = tn = fp = fn = 0
    for i in range(0, len(data)):
        if (data[i]['values'][formula]['positive'] >= data[i]['values'][formula]['negative']):
            if data[i]['values']['label'] == 'positive':
                tp += 1
            else:
                fp += 1
        elif (data[i]['values'][formula]['positive'] < data[i]['values'][formula]['negative']):
            if (data[i]['values']['label'] == 'negative'):
                tn += 1
            else:
                fn += 1
        else:
            raise Exception("Positive similarity equals to negative similarity to news " + data[i]['id'])

    accuracy = accuracy(tp, tn, fp, fn)
    recall = recall(tp, fn)
    precision = precision(tp, fp)
    f1 = f1(precision, recall);
    specificity = specificity(tn, fp);

    # persiting the results
    with open(path_output, 'a' if append else 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        if (not append):
            spamwriter.writerow(
                ['execution_id', 'tp', 'tn', 'fp', 'fn', 'accuracy', 'precision', 'recall', 'f1', 'specificity'])
        spamwriter.writerow([execution_id, tp, tn, fp, fn, accuracy, precision, recall, f1, specificity])


#mean_max  com_duplicatas pmi
compute_all_metrics(1, os.getcwd() + '/../files/news_and_similarity01.json',
                    os.getcwd() + '/../files/evaluation.csv', "mean_max", False)

#mean_mean  com_duplicatas pmi
compute_all_metrics(2, os.getcwd() + '/../files/news_and_similarity01.json',
                    os.getcwd() + '/../files/evaluation.csv', "mean_mean", True)

#mean_max com_duplicatas pmi_odds
compute_all_metrics(3, os.getcwd() + '/../files/news_and_similarity02.json',
                    os.getcwd() + '/../files/evaluation.csv', "mean_max", True)

#mean_mean com_duplicatas pmi_odds
compute_all_metrics(4, os.getcwd() + '/../files/news_and_similarity02.json',
                    os.getcwd() + '/../files/evaluation.csv', "mean_mean", True)

# mean_max sem_duplicatas pmi
compute_all_metrics(5, os.getcwd() + '/../files/news_and_similarity03.json',
                    os.getcwd() + '/../files/evaluation.csv', "mean_max", True)

# mean_mean sem_duplicatas pmi
compute_all_metrics(6, os.getcwd() + '/../files/news_and_similarity03.json',
                    os.getcwd() + '/../files/evaluation.csv', "mean_mean", True)

# mean_max sem_duplicatas pmi_odds
compute_all_metrics(7, os.getcwd() + '/../files/news_and_similarity04.json',
                    os.getcwd() + '/../files/evaluation.csv', "mean_max", True)

# mean_mean sem_duplicatas pmi_odds
compute_all_metrics(8, os.getcwd() + '/../files/news_and_similarity04.json',
                    os.getcwd() + '/../files/evaluation.csv', "mean_mean", True)
