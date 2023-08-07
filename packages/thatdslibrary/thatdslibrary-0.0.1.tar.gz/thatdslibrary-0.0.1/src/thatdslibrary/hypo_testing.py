import pingouin as pt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_pvalue_ci_range_v2(df,t_before,t_after):
    a = df.loc[:,t_before]
    b = df.loc[:,t_after]
    _tmp = pt.ttest(b,a, paired=True)
    ci_range = _tmp['CI95%'].values[0]
    p_v = _tmp['p-val'].values[0]
    return ci_range,p_v
    

def plot_hypo_testing_confidence_interval(df,col_before,col_after,filter_col=None,filter_vals=None, n_hypo_run=10,
                                          sample_size=600,alpha=0.05,x_y_limit=None):
    fig,ax = plt.subplots(figsize=(8,5))
    if x_y_limit:
        plt.axis(x_y_limit)

    c_sig='green'
    c_notsig='red'
    gap=2

    if filter_col is not None and filter_vals is not None:
        for nt,n_type in enumerate(filter_vals):
            for i in range(n_hypo_run):
                _df = df.loc[df[filter_col]==n_type].sample(sample_size)
                ci_range,p_v = get_pvalue_ci_range_v2(_df,col_before,col_after)
                _color = c_sig if p_v < alpha else c_notsig
                _gap = nt*gap + 0.1*i
                ax.plot(np.mean(ci_range),_gap, marker="x", markersize=5, color=_color)
                ax.plot(ci_range,[_gap,_gap],marker="o",markersize=3 ,color=_color)
            ax.axhline(y = nt*gap + 0.1*filter_vals + 0.5, color = 'black', linestyle = '-')

    else:
        for i in range(n_hypo_run):
            _df = df.sample(sample_size)
            ci_range,p_v = get_pvalue_ci_range_v2(_df,col_before,col_after)
            _color = c_sig if p_v < alpha else c_notsig
            _gap = nt*gap + 0.1*i
            ax.plot(np.mean(ci_range),_gap, marker="x", markersize=5, color=_color)
            ax.plot(ci_range,[_gap,_gap],marker="o",markersize=3 ,color=_color)

    ax.axvline(x= 0, color= 'black')
    ax.grid(True)
    ax.set_title(f'Hypothesis testing with alpha {alpha}: {col_before} vs {col_after}')
    return ax
