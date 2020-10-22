import os.path
import time
from collections import defaultdict

# import ray
import cv2
import numpy as np
import pandas as pd
import utils.metrics as metrics
from joblib import Parallel, delayed
from scipy import spatial
from tqdm import tqdm
from utils.hpatch import get_patch
from utils.misc import green


PARALLEL_EVALUATION = True

id2t = {0: {'e': 'ref', 'h': 'ref', 't': 'ref'},
        1: {'e': 'e1', 'h': 'h1', 't': 't1'},
        2: {'e': 'e2', 'h': 'h2', 't': 't2'},
        3: {'e': 'e3', 'h': 'h3', 't': 't3'},
        4: {'e': 'e4', 'h': 'h4', 't': 't4'},
        5: {'e': 'e5', 'h': 'h5', 't': 't5'}}

tp = ['e', 'h', 't']

moddir = os.path.dirname(os.path.abspath(__file__))
tskdir = os.path.normpath(os.path.join(moddir, "..", "..", "tasks"))


def seqs_lengths(seqs):
    """ Helper method to return length for all seqs"""
    N = {}
    for seq in seqs:
        N[seq] = seqs[seq].N
    return N


def dist_matrix(D1, D2, distance):
    """ Distance matrix between two sets of descriptors"""
    if distance == 'L2':
        D = spatial.distance.cdist(D1, D2, 'euclidean')
    elif distance == 'HAMMING':
        from utilities import libupmboost_algs
        # D = spatial.distance.cdist(D1, D2, 'cityblock')
        # D = spatial.distance.cdist(np.unpackbits(D1, axis=1), np.unpackbits(D2, axis=1), 'hamming')
        D = libupmboost_algs.cpp_numpy_popcount(np.bitwise_xor(D1[:, np.newaxis], D2[np.newaxis]), 2)
        D = D.astype(np.float32) / 256.0
    elif distance == 'L1':
        D = spatial.distance.cdist(D1, D2, 'cityblock')
    else:
        raise ValueError('Unknown distance - valid options are |L2|L1|HAMMING|')
    return D


#####################
# Verification task #
#####################
def get_verif_dists(descr, pairs, op):
    d = {}
    for t in ['e', 'h', 't']:
        d[t] = np.empty((pairs.shape[0], 1))
    idx = 0
    pbar = tqdm(pairs)
    pbar.set_description("Processing verification task %i/3 " % op)

    # TODO Use BFMatcher to calculate this distance
    for p in pbar:
        [t1, t2] = [id2t[p[1]], id2t[p[4]]]
        for t in tp:
            d1 = getattr(descr[p[0]], t1[t])[p[2]]
            d2 = getattr(descr[p[3]], t2[t])[p[5]]
            distance = descr['distance']
            if distance == 'L2':
                dist = spatial.distance.euclidean(d1, d2)
            elif distance == 'HAMMING':
                # dist = spatial.distance.cityblock(d1, d2)
                # dist = np.unpackbits(np.bitwise_xor(d1, d2)).sum()
                from utilities import libupmboost_algs
                dist = libupmboost_algs.cpp_numpy_popcount(np.bitwise_xor(d1, d2))
            elif distance == 'L1':
                dist = spatial.distance.cityblock(d1, d2)
            else:
                raise ValueError('Unknown distance - valid options are |L2|L1|HAMMING|')
            d[t][idx] = dist
        idx += 1
    return d


def eval_verification(descr, split):
    print('>> Evaluating %s task' % green('verification'))

    start = time.time()
    pos = pd.read_csv(os.path.join(tskdir, 'verif_pos_split-' + split['name'] + '.csv')).values
    neg_intra = pd.read_csv(os.path.join(tskdir, 'verif_neg_intra_split-' + split['name'] + '.csv')).values
    neg_inter = pd.read_csv(os.path.join(tskdir, 'verif_neg_inter_split-' + split['name'] + '.csv')).values

    d_pos = get_verif_dists(descr, pos, 1)
    d_neg_intra = get_verif_dists(descr, neg_intra, 2)
    d_neg_inter = get_verif_dists(descr, neg_inter, 3)

    results = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    for t in tp:
        l = np.vstack((np.zeros_like(d_pos[t]), np.ones_like(d_pos[t])))
        d_intra = np.vstack((d_neg_intra[t], d_pos[t]))
        d_inter = np.vstack((d_neg_inter[t], d_pos[t]))

        # get results for the balanced protocol: 1M Positives - 1M Negatives
        _, _, auc = metrics.roc(-d_intra, l)
        results[t]['intra']['balanced']['auc'] = auc
        results[t]['inter']['balanced']['auc'] = auc

        # get results for the imbalanced protocol: 0.2M Pos - 1M Negs
        N_imb = d_pos[t].shape[0] + int(d_pos[t].shape[0] * 0.2)  # 1M + 0.2*1M
        _, _, ap = metrics.pr(-d_intra[0:N_imb], l[0:N_imb])
        results[t]['intra']['imbalanced']['ap'] = ap

        _, _, ap = metrics.pr(-d_inter[0:N_imb], l[0:N_imb])
        results[t]['inter']['imbalanced']['ap'] = ap
    end = time.time()
    print(">> %s task finished in %.0f secs  " % (green('Verification'),
                                                  end - start))
    return results


def gen_verif(seqs, split, N_pos=1e6, N_neg=1e6):
    np.random.seed(42)

    # positives
    s = np.random.choice(split['test'], int(N_pos))
    seq2len = seqs_lengths(seqs)
    s_N = [seq2len[k] for k in s]
    s_idx = np.array(
        [np.random.choice(np.arange(k), 2, replace=False) for k in s_N])
    s_type = np.array(
        [np.random.choice(np.arange(5), 2, replace=False) for k in s_idx])
    df = pd.DataFrame({'s1': pd.Series(s, dtype=object),
                       's2': pd.Series(s, dtype=object),
                       'idx1': pd.Series(s_idx[:, 0], dtype=int),
                       'idx2': pd.Series(s_idx[:, 0], dtype=int),
                       't1': pd.Series(s_type[:, 0], dtype=int),
                       't2': pd.Series(s_type[:, 1], dtype=int)})
    df = df[['s1', 't1', 'idx1', 's2', 't2',
             'idx2']]  # updated order for matlab comp.
    df.to_csv(
        os.path.join(tskdir, 'verif_pos_split-' + split['name'] + '.csv'),
        index=False)

    # intra-sequence negatives
    df = pd.DataFrame({'s1': pd.Series(s, dtype=object),
                       's2': pd.Series(s, dtype=object),
                       'idx1': pd.Series(s_idx[:, 0], dtype=int),
                       'idx2': pd.Series(s_idx[:, 1], dtype=int),
                       't1': pd.Series(s_type[:, 0], dtype=int),
                       't2': pd.Series(s_type[:, 1], dtype=int)})
    df = df[['s1', 't1', 'idx1', 's2', 't2',
             'idx2']]  # updated order for matlab comp.
    df.to_csv(
        os.path.join(tskdir,
                     'verif_neg_intra_split-' + split['name'] + '.csv'),
        index=False)

    # inter-sequence negatives
    s_inter = np.random.choice(split['test'], int(N_neg))
    s_N_inter = [seq2len[k] for k in s_inter]
    s_idx_inter = np.array([np.random.randint(k) for k in s_N_inter])
    df = pd.DataFrame({'s1': pd.Series(s, dtype=object),
                       's2': pd.Series(s_inter, dtype=object),
                       'idx1': pd.Series(s_idx[:, 0], dtype=int),
                       'idx2': pd.Series(s_idx_inter, dtype=int),
                       't1': pd.Series(s_type[:, 0], dtype=int),
                       't2': pd.Series(s_type[:, 1], dtype=int)})
    df = df[['s1', 't1', 'idx1', 's2', 't2',
             'idx2']]  # updated order for matlab comp.
    df.to_csv(
        os.path.join(tskdir,
                     'verif_neg_inter_split-' + split['name'] + '.csv'),
        index=False)


#################
# Matching task #
#################
def eval_matching(descr, split):
    print('>> Evaluating %s task' % green('matching'))
    start = time.time()

    binary = descr['distance'] == 'HAMMING'

    if descr['distance'] == 'L2':
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    elif descr['distance'] == 'HAMMING':
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    elif descr['distance'] == 'L1':
        bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=False)
    else:
        raise ValueError('Unknown distance - valid options are |L2|L1|HAMMING|')

    results = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    pbar = tqdm(split['test'])
    small = 1e-10
    for seq in pbar:
        d_ref = getattr(descr[seq], 'ref')
        if not binary:
            d_ref = d_ref.astype(np.float32)
        correspondences = np.maximum(d_ref.shape[0], small)
        n_patches_at_ptn = np.maximum(np.arange(correspondences + 1), small)
        for t in tp:
            for i in range(1, 6):
                d = getattr(descr[seq], t + str(i))
                if not binary:
                    d = d.astype(np.float32)

                matches1 = bf.match(d_ref, d)
                matches1.sort(key=lambda m: m.distance)
                m_l = np.array(list(map(lambda m: m.trainIdx == m.queryIdx, matches1)))
                my_tp = np.append(0, np.cumsum(m_l))
                # compute precision and recall
                recall = my_tp / correspondences
                precision = np.maximum(my_tp, small) / n_patches_at_ptn
                # Calculate the average precision using trapezoidal area
                ap = np.trapz(precision, recall)
                # An approximation: np.sum(precision[1:][m_l] / correspondences)
                results[seq][t][i]['ap'] = ap

    end = time.time()
    print(">> %s task finished in %.0f secs  " % (green('Matching'), end - start))
    return results


##################
# Retrieval task #
##################

def get_query_intra_dists(descr, d, query, t):
    idx = query[1]
    seq = query[0]
    D = np.empty(5)
    d = np.expand_dims(d, axis=0)

    for i in range(1, 6):
        d_ = getattr(descr[seq], t + str(i))[idx]
        d_ = np.expand_dims(d_, axis=0)
        D[i - 1] = dist_matrix(d, d_, descr['distance'])[0]
    return D


def eval_retrieval(descr, split):
    print('>> Evaluating %s task' % green('retrieval'))
    start = time.time()

    q = pd.read_csv(os.path.join(tskdir, 'retr_queries_split-' + split['name'] + '.csv')).values
    d = pd.read_csv(os.path.join(tskdir, 'retr_distractors_split-' + split['name'] + '.csv')).values

    desc_q = np.array([descr[scene_name].ref[kp_idx] for scene_name, kp_idx in q])
    desc_d = np.array([descr[scene_name].ref[kp_idx] for scene_name, kp_idx in d])

    # distractor masking per sequence
    m = dict((seq, d[:, 0] != seq) for seq in split['test'])

    print(">> Please wait, computing distance matrix...")
    D = dist_matrix(desc_q, desc_d, descr['distance'])
    print(">> Distance matrix done.")

    results = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    # at_ranks = [int(x*N_distractors) for x in [0.25,0.5,0.75,1]]
    at_ranks = [100, 500, 1000, 5000, 10000, 15000, 20000]

    pbar = tqdm(range(desc_q.shape[0]))
    pbar.set_description("Processing retrieval task")

    def eval_retrieval_seq(i):
        for t in tp:
            D_intra = get_query_intra_dists(descr, desc_q[i], q[i], t)
            D_ = D[i, :]
            D_ = D_[m[q[i][0]]]
            gt = np.zeros_like(D_)
            D_ = np.hstack((D_intra, D_))
            gt = np.hstack((np.array([1, 1, 1, 1, 1]), gt))
            for k in at_ranks:
                _, _, ap = metrics.pr(-D_[0:k], gt[0:k])
                results[i][t][k]['ap'] = ap

    if PARALLEL_EVALUATION:
        # Call the function train_ith_wl_in_parallel using all the CPUs but one
        Parallel(n_jobs=-2,
                 backend='threading',
                 require='sharedmem',
                 prefer='threads')(delayed(eval_retrieval_seq)(i) for i in pbar)
    else:
        list(map(eval_retrieval_seq, pbar))
    end = time.time()
    print(">> %s task finished in %.0f secs  " % (green('Retrieval'), end - start))
    return results


def gen_retrieval(seqs, split, N_queries=0.5 * 1e4, N_distractors=2 * 1e4):
    np.random.seed(42)
    seq2len = seqs_lengths(seqs)

    s_q = np.random.choice(split['test'], int(N_queries * 4))
    s_q_N = [seq2len[k] for k in s_q]
    s_q_idx = [np.random.randint(k) for k in s_q_N]
    s_q_idx = np.array(s_q_idx)

    s_d = np.random.choice(split['test'], int(N_distractors * 10))
    s_d_N = [seq2len[k] for k in s_d]
    s_d_idx = [np.random.randint(k) for k in s_d_N]
    s_d_idx = np.array(s_d_idx)

    msk = np.zeros((s_q.shape[0],))
    for i in range(s_q.shape[0]):
        p = get_patch(seqs[s_q[i]], 'ref', s_q_idx[i])
        if np.std(p) > 10:
            msk[i] = 1

    msk = np.where(msk == 1)
    s_q = s_q[msk]
    s_q_idx = s_q_idx[msk]

    msk = np.zeros((s_d.shape[0],))
    for i in range(s_d.shape[0]):
        p = get_patch(seqs[s_d[i]], 'ref', s_d_idx[i])
        if np.std(p) > 10:
            msk[i] = 1

    msk = np.where(msk == 1)
    s_d = s_d[msk]
    s_d_idx = s_d_idx[msk]
    q_ = np.stack((s_q, s_q_idx), axis=-1)
    d_ = np.stack((s_d, s_d_idx), axis=-1)

    df_q = pd.DataFrame({'s': pd.Series(q_[:, 0], dtype=object),
                         'idx': pd.Series(q_[:, 1], dtype=int)})
    df_q = df_q[['s', 'idx']]  # updated order for matlab comp.

    df_d = pd.DataFrame({'s': pd.Series(d_[:, 0], dtype=object),
                         'idx': pd.Series(d_[:, 1], dtype=int)})
    df_d = df_d[['s', 'idx']]  # updated order for matlab comp.

    df_q = df_q.drop_duplicates()
    df_d = df_d.drop_duplicates()
    df_q = df_q.head(N_queries)
    df_q_ = df_q.copy()

    df_q_.set_index(['s', 'idx'], inplace=True)
    df_d.set_index(['s', 'idx'], inplace=True)
    df_d = df_d[~df_d.index.isin(df_q_.index)].reset_index()
    df_d = df_d.head(N_distractors)

    df_q.to_csv(
        os.path.join(tskdir, 'retr_queries_split-' + split['name'] + '.csv'),
        index=False)
    df_d.to_csv(
        os.path.join(tskdir,
                     'retr_distractors_split-' + split['name'] + '.csv'),
        index=False)


methods = {'verification': eval_verification,
           'matching': eval_matching,
           'retrieval': eval_retrieval}
