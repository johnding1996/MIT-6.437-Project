import numpy as np
import scipy.stats as stats

def shuffle(plaincode, length):
    start_index = np.random.randint(plaincode.shape[0]-length)
    return plaincode[start_index:start_index+length]

def encrypt(plaincode, order):
    f_true = np.random.permutation(order)
    ciphercode = f_true[plaincode]
    return ciphercode, f_true

def initialize(num, order):
    x = np.zeros((num, order), dtype=np.int)
    for i in range(num):
        x[i,] = np.random.permutation(order)
    return x

def reshape_lp(lp, num):
    return [np.tile(np.expand_dims(lp[0], axis=0), (num,1)),
            np.tile(np.expand_dims(lp[1], axis=0), (num,1,1)),
            np.tile(np.expand_dims(lp[2], axis=0), (num,1,1,1))]

def mask(x, threshold):
    m = np.empty(x.shape[1], dtype=np.bool)
    xmj = np.zeros(x.shape[1])
    for j in range(x.shape[1]):
        count = np.bincount(x[:,j], minlength=x.shape[1])
        m[j] = (np.max(count) < x.shape[0]*threshold)
        xmj[j] = np.argmax(count)
    return m, xmj.reshape((1,x.shape[1]))

def cumulate(xmj, xmjp, xmj_cum, m, fix_interval):
    for j in range(xmj.shape[1]):
        if xmj[0,j] != xmjp[0,j]:
            xmj_cum[0,j] = 0
        else:
            xmj_cum[0,j] += 1
    return ~np.logical_and(~m, xmj_cum > fix_interval).reshape(xmj.shape[1]), xmj_cum

def change_without_mask(x, m, xmj):
    def _swap(_x):
        idx = np.random.choice(x.shape[1], 2, replace=False)
        _x[idx] = _x[idx[::-1]]
        return _x
    xp = np.apply_along_axis(_swap, 1, np.copy(x))
    return x, xp

def change_with_mask(x, m, xmj):
    def _fix(_x):
        conflict_idx = np.logical_and(~m, xmj[0,]!=_x)
        if np.any(conflict_idx):
            required_codes = list(set(xmj[0,conflict_idx]) - set(_x[conflict_idx]))
            extra_codes = list(set(_x[conflict_idx]) - set(xmj[0,conflict_idx]))
            change_mask = np.empty(xmj.shape[1], dtype=np.bool)
            for j in range(xmj.shape[1]):
                change_mask[j] =  (_x[j] in required_codes)
            _x[~m] = xmj[0,~m]
            _x[change_mask] = np.random.permutation(np.array(extra_codes))
        return _x
    def _swap(_x):
        idx = np.random.choice(x.shape[1], 2, replace=False)
        _x[idx] = _x[idx[::-1]]
        return _x
    x = np.apply_along_axis(_fix, 1, x)
    xp = np.apply_along_axis(_swap, 1, np.copy(x))
    return x, xp

def count(ciphercode, order):
    c1 = np.zeros(order)
    np.add.at(c1, ciphercode, 1)
    c2 = np.zeros((order, order))
    np.add.at(c2, (ciphercode[:-1], ciphercode[1:]), 1)
    c3 = np.zeros((order, order, order))
    np.add.at(c3, (ciphercode[:-2], ciphercode[1:-1], ciphercode[2:]), 1)
    return [c1, c2, c3]

def log_prob(x, lp, c, w):
    num = x.shape[0]
    order = x.shape[1]
    x_lp = np.sum(c[0][x]*lp[0], axis=1)*w[0]
    x_lp += np.sum(c[1][np.tile(x.reshape((num,order,1)), (1,1,order)), 
                        np.tile(x.reshape((num,1,order)), (1,order,1))
                       ]*lp[1], axis=(1,2))*w[1]
    x_lp += np.sum(c[2][np.tile(x.reshape((num,order,1,1)), (1,1,order,order)),
                        np.tile(x.reshape((num,1,order,1)), (1,order,1,order)),
                        np.tile(x.reshape((num,1,1,order)), (1,order,order,1))
                       ]*lp[2], axis=(1,2,3))*w[2]
    return x_lp

def update(x, xp, p_delta):
    rs = (p_delta > 0).reshape((x.shape[0],1)).astype(np.int)
    return rs*xp+(1-rs)*x, rs

def accuracy(x, ciphercode, plaincode):
    if np.isnan(x).any():
        return np.nan
    xinv = np.argsort(x, axis=1)
    plaincode = np.repeat(plaincode.reshape((1,-1)), x.shape[0], axis=0)
    return np.mean((xinv[:,ciphercode] == plaincode).astype(np.int))

def kendalltau(x, f_true):
    ktau = np.zeros(x.shape[0])
    for i in range(x.shape[0]):
        ktau[i] = stats.kendalltau(x[i,], f_true)[0]
    return np.mean(ktau)

def mapping_accuracy(x, f_true):
    func_acc = np.zeros(x.shape[0])
    for i in range(x.shape[0]):
        func_acc[i] = np.mean(x[i,] == f_true)
    return np.mean(func_acc)

def error_map(x, f_true):
    xinv = np.argsort(x, axis=1)
    f_true_inv = np.argsort(f_true)
    error_map = np.zeros((x.shape[1], x.shape[1]))
    for i in range(x.shape[0]):
        error_map[f_true_inv[xinv[i,] != f_true_inv].astype(np.int), 
                  xinv[i,][xinv[i,] != f_true_inv].astype(np.int)] += 1
    return error_map

def grammar_validity(x, ciphercode):
    xinv = np.argsort(x, axis=1)
    plaincode = xinv[:,ciphercode]
    return 1-np.mean(np.any(np.logical_and(plaincode[:,:-1] == 27, plaincode[:,1:] != 26), axis=1))

def show_errormap(errormap):
    plt.figure(figsize=(16,14))
    sns.heatmap(error_map)
    plt.show()