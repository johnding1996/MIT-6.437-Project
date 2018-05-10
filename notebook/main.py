from solver import *

def main(testcc, lp, num, order, maxiter, verbose_interval, w, threshold, use_mask, fix_interval, testpc=None, f_true=None):
    c = count(testcc, order)
    x = initialize(lp, c, num, order)
    rlp = reshape_lp(lp, num)
    rs_cum = np.zeros((num,1))
    xmj_cum = np.zeros((1,order))
    m, xmj = mask(x, threshold)
    it = 0
    for it in range(maxiter):
        m, xmjp = mask(x, threshold)
        if use_mask:
            m, xmj_cum = cumulate(xmj, xmjp, xmj_cum, m, fix_interval)
        xmj = xmjp
        if np.mean(m) == 0:
            break
        if use_mask:
            x, xp = change_with_mask(x, m, xmj)
        else:
            x, xp = change_without_mask(x, m, xmj)
        p_x = log_prob(x, rlp, c, w)
        xb = best(x, p_x)
        p_xp = log_prob(xp, rlp, c, w)
        p_delta = p_xp - p_x
        x, rs = update(x, xp, p_delta)
        rs_cum += rs
        if testpc is None and f_true is None:
            acc = map_acc = gm_v = mj_macc = np.nan
        else:     
            acc = accuracy(x, testcc, testpc)
            map_acc = mapping_accuracy(x, f_true)
            gm_v = grammar_validity(x, testcc)
            mj_macc = mapping_accuracy(xmj, f_true)
            b_macc = mapping_accuracy(xb, f_true)
            er_map = error_map(xmj, f_true)
        if verbose_interval > 0 and it % verbose_interval == 0:
            print("it:{}, log_p:{:1.3e}, acpt_r:{:1.3e}, acc:{:1.3e}, macc:{:1.3e}, p_fix:{:1.3e}, b_macc:{:1.3e}".format(
                  str(it).zfill(4), np.mean(p_x), np.mean(rs_cum)/verbose_interval, acc, map_acc, 1-np.mean(m), b_macc))
            rs_cum = np.zeros((num,1))
    xmj = xmj.reshape(xmj.shape[-1])
    xb = xb.reshape(xb.shape[-1])
    return np.argsort(xb)[testcc], xb
