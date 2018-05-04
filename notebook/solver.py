import numpy as np
import scipy.stats as stats

def shuffle(plaincode, length):
    return plaincode[:length]

def encrypt(plaincode, order):
    f_true = np.random.permutation(order)
    ciphercode = f_true[plaincode]
    return ciphercode, f_true

def initialize(num, order):
    x = np.zeros((num, order), dtype=np.int)
    for i in range(num):
        x[i,] = np.random.permutation(order)
    return x

def change(x):
    def _roll(_x):
        idx = np.random.choice(_x.shape[0], 2, replace=False)
        _x[idx] = _x[np.roll(idx, 1)]
        return _x
    xp = np.apply_along_axis(_roll, 1, np.copy(x))
    return xp

def count(ciphercode, order):
    c1 = np.zeros(order)
    np.add.at(c1, ciphercode, 1)
    c2 = np.zeros((order, order))
    np.add.at(c2, (ciphercode[:-1], ciphercode[1:]), 1)
    c3 = np.zeros((order, order, order))
    np.add.at(c3, (ciphercode[:-2], ciphercode[1:-1], ciphercode[2:]), 1)
    return [c1, c2, c3]

def log_prob(x, lp, c, w, num, order):
    x_lp = np.sum(c[0][x] * np.repeat(np.expand_dims(lp[0], axis=0), num, axis=0),
                  axis=1)*w[0]
    x_lp += np.sum(c[1][np.tile(x.reshape((num,order,1)), (1,1,order)), 
                        np.tile(x.reshape((num,1,order)), (1,order,1))
                       ]*np.tile(np.expand_dims(lp[1], axis=0), (num,1,1)), 
                   axis=(1,2))*w[1]
    x_lp += np.sum(c[2][np.tile(x.reshape((num,order,1,1)), (1,1,order,order)),
                        np.tile(x.reshape((num,1,order,1)), (1,order,1,order)),
                        np.tile(x.reshape((num,1,1,order)), (1,order,order,1))
                       ]*np.tile(np.expand_dims(lp[2], axis=0), (num,1,1,1)), 
                 axis=(1,2,3))*w[2]
    return x_lp

def step(delta_lp):
    #pr = np.exp(np.clip(logpr, -np.inf, 0))
    #return (np.random.rand(pr.shape[0]) < pr).astype(np.int)
    return (delta_lp > 0).astype(np.int)

def update(x, xp, rs):
    rs = rs.reshape((rs.shape[0],1))
    return rs*xp+(1-rs)*x

def accuracy(x, ciphercode, plaincode):
    xinv = np.argsort(x, axis=1)
    plaincode = np.repeat(plaincode.reshape((1,-1)), x.shape[0], axis=0)
    return np.sum((xinv[:,ciphercode] == plaincode).astype(np.int))/x.shape[0]/ciphercode.shape[0]

def kendalltau(x, f_true):
    ktau = np.zeros(x.shape[0])
    for i in range(x.shape[0]):
        ktau[i] = stats.kendalltau(x[i,], f_true)[0]
    return np.mean(ktau)

def mapping_accuracy(x, f_true, order):
    x = np.argsort(x, axis=1)
    f_true = np.argsort(f_true)
    func_acc = np.zeros(x.shape[0])
    error_map = np.zeros((order, order))
    for i in range(x.shape[0]):
        func_acc[i] = np.mean(x[i,] == f_true)
        error_map[f_true[x[i,] != f_true].astype(np.int), x[i,][x[i,] != f_true].astype(np.int)] += 1
    return np.mean(func_acc), error_map

def grammar_validity(x, ciphercode):
    xinv = np.argsort(x, axis=1)
    plaincode = xinv[:,ciphercode]
    return 1-np.mean(np.any(np.logical_and(plaincode[:,:-1] == 27, plaincode[:,1:] != 26), axis=1))

def show_errormap(errormap):
    plt.figure(figsize=(16,14))
    sns.heatmap(error_map)
    plt.show()