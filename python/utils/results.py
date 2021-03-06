import itertools
import operator
import os.path
from collections import defaultdict

import dill
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
from utils.config import desc_info, figure_attributes

ft = {'e': 'Easy', 'h': 'Hard', 't': 'Tough'}


class DescriptorMatchingResult:
    def __init__(self, desc, splt, results_dir='results'):
        matching_results = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        res = dill.load(open(os.path.join(results_dir, desc + "_matching_" + splt['name'] + ".p"), "rb"))

        for seq in res:
            seq_type = seq.split("_")[0]
            for t in ft.keys():
                APs = [res[seq][t][idx]['ap'] for idx in range(1, 6)]
                mAP = np.mean(APs)
                matching_results[t][seq_type][seq] = mAP

        cases = list(itertools.product(ft.keys(), ['v', 'i']))
        self.avg_v, self.avg_i = 0, 0

        for itm in cases:
            noise_type, seq_type = itm[0], itm[1]
            val = 100 * np.mean(
                list(matching_results[noise_type][seq_type].values()))
            setattr(self, str(itm), val)
            setattr(self, "avg_" + seq_type, getattr(self, "avg_" + seq_type) + val)

        n_samples = float(len(cases)) / 2.0
        self.avg_i = self.avg_i / n_samples
        self.avg_v = self.avg_v / n_samples
        self.avg = (self.avg_i + self.avg_v) / 2.0


class DescriptorRetrievalResult:
    def __init__(self, desc, splt, results_dir='results'):
        self.e, self.h, self.t = None, None, None
        res = dill.load(open(os.path.join(results_dir, desc + "_retrieval_" + splt['name'] + ".p"), "rb"))

        retrieval_results = defaultdict(lambda: defaultdict(dict))
        pool_sizes = [100, 500, 1000, 5000, 10000, 15000, 20000]
        for psize in pool_sizes:
            for t in ft.keys():
                retrieval_results[t][psize] = []

        for q_idx in res.keys():
            for t in ft.keys():
                for psize in pool_sizes:
                    retrieval_results[t][psize].append(
                        100 * res[q_idx][t][psize]['ap'])

        for t in ft.keys():
            avg_t = 0
            for psize in pool_sizes:
                avg_t += np.mean(retrieval_results[t][psize])
            setattr(self, t, avg_t / float(len(pool_sizes)))
        self.avg = (self.e + self.h + self.t) / 3.0


class DescriptorVerificationResult:
    def __init__(self, desc, splt, results_dir='results'):
        metric = {'balanced': 'auc', 'imbalanced': 'ap'}
        self.desc = desc
        self.splt = splt

        file_path = os.path.join(results_dir, self.desc + "_verification_" + self.splt['name'] + ".p")
        res = dill.load(open(file_path, "rb"))
        cases = list(itertools.product(ft.keys(), ['intra', 'inter'], ['balanced', 'imbalanced']))

        self.avg_balanced = 0
        self.avg_imbalanced = 0

        for itm in cases:
            noise_type, negs_type, balance_type = itm[0], itm[1], itm[2]
            val = 100 * res[noise_type][negs_type][balance_type][metric[balance_type]]
            setattr(self, str(itm), val)
            setattr(self, "avg_" + balance_type, getattr(self, "avg_" + balance_type) + val)

        n_samples = float(len(cases)) / 2.0
        self.avg_balanced = self.avg_balanced / n_samples
        self.avg_imbalanced = self.avg_imbalanced / n_samples


class DescriptorHPatchesResult:
    def __init__(self, desc, splt, results_dir='results'):
        self.desc = desc
        self.splt = splt
        self.verification = DescriptorVerificationResult(desc, splt, results_dir)
        self.matching = DescriptorMatchingResult(desc, splt, results_dir)
        self.retrieval = DescriptorRetrievalResult(desc, splt, results_dir)


def plot_verification(hpatches_results, ax, use_balanced=False, **kwargs):
    balance_type = 'balanced' if use_balanced else 'imbalanced'
    hpatches_results.sort(
        key=operator.attrgetter('verification.avg_' + balance_type), reverse=True)
    descrs = [x.desc for x in hpatches_results]
    y_pos = np.arange(len(descrs))

    avg_verifs = [getattr(x.verification, "avg_" + balance_type) for x in hpatches_results]

    cases = list(
        itertools.product(ft.keys(), ['intra', 'inter'], [balance_type]))
    verification_results = {}
    for case in cases:
        case_results = []
        for descr_result in hpatches_results:
            case_results.append(getattr(descr_result.verification, str(case)))
        verification_results[str(case)] = case_results

    ax.set_axisbelow(True)
    ax.xaxis.grid(color='gray', linestyle='dashed')
    ax.yaxis.grid(color='gray', linestyle='dashed')

    ax.set_yticks(y_pos)
    ax.set_yticklabels([desc_info[x].name for x in descrs], fontsize=14)
    ax.tick_params(axis='both', which='both', length=0)
    # ax.set_xticklabels(np.arange(0, 101, 20), fontsize=12)

    ax.barh(
        y_pos,
        avg_verifs,
        color=[desc_info[x].color for x in descrs],
        edgecolor='k',
        linewidth=1.5,
        alpha=0.8)

    ax.plot(
        verification_results[str(('e', 'inter', balance_type))],
        y_pos,
        marker=figure_attributes['inter_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['easy_colour'])
    ax.plot(
        verification_results[str(('e', 'intra', balance_type))],
        y_pos,
        marker=figure_attributes['intra_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['easy_colour'])
    ax.plot(
        verification_results[str(('h', 'inter', balance_type))],
        y_pos,
        marker=figure_attributes['inter_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['hard_colour'])
    ax.plot(
        verification_results[str(('h', 'intra', balance_type))],
        y_pos,
        marker=figure_attributes['intra_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['hard_colour'])
    ax.plot(
        verification_results[str(('t', 'inter', balance_type))],
        y_pos,
        marker=figure_attributes['inter_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['tough_colour'])
    ax.plot(
        verification_results[str(('t', 'intra', balance_type))],
        y_pos,
        marker=figure_attributes['intra_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['tough_colour'])
    ax.set_xlim([0, 100])

    for i, v in enumerate(avg_verifs):
        ax.text(
            101,
            y_pos[i] - 0.13,
            r"{:.2f}".format(v),
            color='black',
            fontsize=14)

    inter_symbol = mlines.Line2D([], [],
                                 color='black',
                                 marker=figure_attributes['inter_marker'],
                                 linestyle='None',
                                 markersize=5,
                                 label=r'\textsc{Inter}')
    intra_symbol = mlines.Line2D([], [],
                                 color='black',
                                 marker=figure_attributes['intra_marker'],
                                 linestyle='None',
                                 markersize=5,
                                 label=r'\textsc{Intra}')
    ax.legend(
        handles=[inter_symbol, intra_symbol],
        loc='lower center',
        ncol=2,
        bbox_to_anchor=(0.34, 1, .3, .0),
        handletextpad=-0.5,
        columnspacing=0,
        fontsize=12,
        frameon=False)

    return ax


def plot_matching(hpatches_results, ax, **kwargs):
    hpatches_results.sort(
        key=operator.attrgetter('matching.avg'), reverse=True)
    descrs = [x.desc for x in hpatches_results]
    y_pos = np.arange(len(descrs))

    avg_verifs = [getattr(x.matching, "avg") for x in hpatches_results]

    cases = list(itertools.product(ft.keys(), ['v', 'i']))
    matching_results = {}
    for case in cases:
        case_results = []
        for descr_result in hpatches_results:
            case_results.append(getattr(descr_result.matching, str(case)))
        matching_results[str(case)] = case_results

    ax.set_axisbelow(True)
    ax.xaxis.grid(color='gray', linestyle='dashed')
    ax.yaxis.grid(color='gray', linestyle='dashed')

    ax.set_yticks(y_pos)
    ax.set_yticklabels([desc_info[x].name for x in descrs], fontsize=14)
    ax.tick_params(axis='both', which='both', length=0)
    # ax.set_xticklabels(np.arange(0, 101, 20), fontsize=12)

    ax.barh(
        y_pos,
        avg_verifs,
        color=[desc_info[x].color for x in descrs],
        edgecolor='k',
        linewidth=1.5,
        alpha=0.8)

    ax.plot(
        matching_results[str(('e', 'v'))],
        y_pos,
        marker=figure_attributes['viewp_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['easy_colour'])
    ax.plot(
        matching_results[str(('e', 'i'))],
        y_pos,
        marker=figure_attributes['illum_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['easy_colour'])
    ax.plot(
        matching_results[str(('h', 'v'))],
        y_pos,
        marker=figure_attributes['viewp_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['hard_colour'])
    ax.plot(
        matching_results[str(('h', 'i'))],
        y_pos,
        marker=figure_attributes['illum_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['hard_colour'])
    ax.plot(
        matching_results[str(('t', 'v'))],
        y_pos,
        marker=figure_attributes['viewp_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['tough_colour'])
    ax.plot(
        matching_results[str(('t', 'i'))],
        y_pos,
        marker=figure_attributes['illum_marker'],
        linestyle="",
        alpha=0.8,
        color=figure_attributes['tough_colour'])
    ax.set_xlim([0, 100])

    for i, v in enumerate(avg_verifs):
        ax.text(
            101,
            y_pos[i] - 0.13,
            r"{:.2f}".format(v),
            color='black',
            fontsize=14)

    view_symbol = mlines.Line2D([], [],
                                color='black',
                                marker=figure_attributes['viewp_marker'],
                                linestyle='None',
                                markersize=5,
                                label=r'\textsc{Viewp}')
    illum_symbol = mlines.Line2D([], [],
                                 color='black',
                                 marker=figure_attributes['illum_marker'],
                                 linestyle='None',
                                 markersize=5,
                                 label=r'\textsc{Illum}')
    ax.legend(
        handles=[view_symbol, illum_symbol],
        loc='lower center',
        ncol=2,
        bbox_to_anchor=(0.34, 1, .3, .0),
        handletextpad=-0.5,
        columnspacing=0,
        fontsize=12,
        frameon=False)
    return ax


def plot_retrieval(hpatches_results, ax, **kwargs):
    hpatches_results.sort(
        key=operator.attrgetter('retrieval.avg'), reverse=True)
    descrs = [x.desc for x in hpatches_results]
    y_pos = np.arange(len(descrs))

    avg_verifs = [getattr(x.retrieval, "avg") for x in hpatches_results]

    retrieval_results = {}
    for case in ft.keys():
        case_results = []
        for descr_result in hpatches_results:
            case_results.append(getattr(descr_result.retrieval, str(case)))
        retrieval_results[str(case)] = case_results

    ax.set_axisbelow(True)
    ax.xaxis.grid(color='gray', linestyle='dashed')
    ax.yaxis.grid(color='gray', linestyle='dashed')

    ax.set_yticks(y_pos)
    ax.set_yticklabels([desc_info[x].name for x in descrs], fontsize=14)
    ax.tick_params(axis='both', which='both', length=0)
    # ax.set_xticklabels(np.arange(0, 101, 20), fontsize=12)

    ax.barh(
        y_pos,
        avg_verifs,
        color=[desc_info[x].color for x in descrs],
        edgecolor='k',
        linewidth=1.5,
        alpha=0.8)

    ax.plot(
        retrieval_results[str(('e'))],
        y_pos,
        marker="o",
        linestyle="",
        alpha=0.8,
        markersize=4,
        color=figure_attributes['easy_colour'])
    ax.plot(
        retrieval_results[str(('h'))],
        y_pos,
        marker="o",
        linestyle="",
        alpha=0.8,
        markersize=4,
        color=figure_attributes['hard_colour'])
    ax.plot(
        retrieval_results[str(('t'))],
        y_pos,
        marker="o",
        linestyle="",
        alpha=0.8,
        markersize=4,
        color=figure_attributes['tough_colour'])
    ax.set_xlim([0, 100])

    for i, v in enumerate(avg_verifs):
        ax.text(
            101,
            y_pos[i] - 0.13,
            r"{:.2f}".format(v),
            color='black',
            fontsize=14)

    return ax


def plot_hpatches_results(hpatches_results, out_dir='.', balanced_verification=False):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    # plt.rc('text.latex', preamble=r'\usepackage{amssymb} \usepackage{color}')
    n_descrs = len(hpatches_results)
    # The height of the plot for descriptors depend on number of descriptors
    # The 0.8 is absolute value for blank space at the bottom
    bar_width = 0.3
    descr_height = n_descrs * bar_width + 0.8

    # Figure height is descriptor plot height plus fixed 1.2 for header
    figh = 1.2 + descr_height
    f, (ax_verification, ax_matching, ax_retrieval) = plt.subplots(1, 3)
    f.set_size_inches(15, figh)
    f.suptitle(r'{\bf HPatches Results}', fontsize=22, x=0.5, y=0.98)

    easy_marker = mlines.Line2D([], [],
                                color=figure_attributes['easy_colour'],
                                marker='s',
                                linestyle='None',
                                markersize=4,
                                label=r'\textsc{Easy}')
    hard_marker = mlines.Line2D([], [],
                                color=figure_attributes['hard_colour'],
                                marker='s',
                                linestyle='None',
                                markersize=4,
                                label=r'\textsc{Hard}')
    tough_marker = mlines.Line2D([], [],
                                 color=figure_attributes['tough_colour'],
                                 marker='s',
                                 linestyle='None',
                                 markersize=4,
                                 label=r'\textsc{Tough}')
    plt.figlegend(
        handles=[easy_marker, hard_marker, tough_marker],
        loc='lower center',
        ncol=3,
        bbox_to_anchor=(0.45, 1 - 0.8 / figh, 0.1, 0.0),
        handletextpad=-0.5,
        fontsize=12,
        columnspacing=0)

    # As this is relative, to have fixed bottom/top space we divide by figh
    # We will have then bottom_margin = bottom * figh = 0.8
    # Same for top, top_margin = figh*(1-top) = figh - descr_size = 1.2
    # And the descriptor plot height will then be 
    # figh - top_margin - bottom_margin = n_descrs * bar_height
    # So descriptor plot height will be directly proportional to n_descr
    plt.subplots_adjust(
        left=0.2, bottom=(0.8 / figh), right=None, top=(descr_height / figh),
        wspace=1.8, hspace=None)

    plot_verification(hpatches_results, ax_verification, use_balanced=balanced_verification)
    plot_matching(hpatches_results, ax_matching)
    plot_retrieval(hpatches_results, ax_retrieval)

    if balanced_verification:
        ax_verification.set_xlabel(r'Patch Verification AUC [\%]', fontsize=15)
    else:
        ax_verification.set_xlabel(r'Patch Verification mAP [\%]', fontsize=15)

    ax_matching.set_xlabel(r'Image Matching mAP [\%]', fontsize=15)
    ax_retrieval.set_xlabel(r'Patch Retrieval mAP [\%]', fontsize=15)

    f.savefig(os.path.join(out_dir, 'hpatches_results.pdf'))
