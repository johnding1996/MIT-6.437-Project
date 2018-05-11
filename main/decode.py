import numpy as np
from util import *
from solver import solve

def decode(ciphertext, output_file_name): 
    lp = load_prob('./data/ngrams')
    wlp = load_word_prob('./data/word')
    num = 10
    order = 28
    maxiter = 5000
    verbose_interval = 100
    w = [1, 0.3, 16]
    threshold = 0.8
    use_mask = True
    fix_interval = 200
    testcc = to_code(ciphertext)
    testdc, f_pred = solve(testcc, lp, wlp, num, order, maxiter, verbose_interval, 
                           w, threshold, use_mask, fix_interval)
    decipheredtext = ''.join(to_text(testdc))
    f = open(output_file_name, 'w')
    f.write(decipheredtext)
    f.close()
