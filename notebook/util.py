import numpy as np
import csv
import string

def _read_csv(data_dir, file_name):
    with open(data_dir + '/' + file_name + '.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        return list(reader)
def _read_text(data_dir, file_name):
    with open(data_dir + '/' + file_name + '.txt', 'r') as textfile:
        return textfile.readlines()

def load_text(data_dir):
    pt1 = _read_text(data_dir, 'russell')[0]
    pt2 = _read_text(data_dir, 'paradiselost')[0]
    pt3 = _read_text(data_dir, 'feynman')[0]
    pt4 = _read_text(data_dir, 'warandpeace')[0]
    return pt1+pt2+pt3+pt4

def load_prob(data_dir):
    lp1 = np.load(data_dir + '/' + 'lp1.npy')
    lp2 = np.load(data_dir + '/' + 'lp2.npy')
    lp3 = np.load(data_dir + '/' + 'lp3.npy')
    return [lp1, lp2, lp3]

def to_code(text):
    alphabet = [a for a in string.ascii_lowercase] + [' ', '.']
    d = dict(zip(alphabet, range(len(alphabet))))
    return np.array([d[t] for t in text])

def to_text(code):
    alphabet = [a for a in string.ascii_lowercase] + [' ', '.']
    d = dict(zip(range(len(alphabet)), alphabet))
    return [d[c] for c in code]
