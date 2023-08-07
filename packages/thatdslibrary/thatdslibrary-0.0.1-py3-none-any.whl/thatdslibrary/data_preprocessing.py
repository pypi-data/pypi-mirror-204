import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from statsmodels.tools.tools import add_constant
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler


def get_vif(df,plot_corr=False):
    if plot_corr:
        fig,ax = plt.subplots(figsize=(10,10))
        dataplot = sns.heatmap(np.round(df.corr(),3), cmap="YlGnBu", annot=True)  
        # displaying heatmap
        plt.show()

    df_const = add_constant(df)    
    vif = pd.Series([variance_inflation_factor(df_const.values, i) 
                    for i in range(df_const.shape[1])], 
                index=df_const.columns)
    print(vif)
    return vif


### preprocessing function ###
def process_missing_values(X_train,X_test=None,miss_cols=[],missing_vals=np.NaN,strategy='median',**kwargs):
    if not len(miss_cols):
        return X_train,X_test
    if not isinstance(missing_vals,list):
        missing_vals = [missing_vals for i in range(len(miss_cols))]
    X_train = X_train.copy()
    if X_test is not None: X_test = X_test.copy()
    for i,c in enumerate(miss_cols):
        imp = SimpleImputer(missing_values=missing_vals[i], strategy=strategy)
        X_train[c] = imp.fit_transform(X_train[c].values.reshape(-1,1)).flatten()
        if X_test is not None: X_test[c] = imp.transform(X_test[c].values.reshape(-1,1)).flatten()
    return X_train,X_test

def minmax_scale_num_cols(X_train,X_test=None,num_cols=[],**kwargs):
    if not len(num_cols):
        return X_train,X_test
    X_train = X_train.copy()
    if X_test is not None: X_test = X_test.copy()
    for c in num_cols:
        imp = MinMaxScaler()
        X_train[c] = imp.fit_transform(X_train[c].values.reshape(-1,1)).flatten()
        if X_test is not None: X_test[c] = imp.transform(X_test[c].values.reshape(-1,1)).flatten()
    return X_train,X_test

def one_hot_cat(X_train,X_test=None,cat_cols=[],bi_cols=[],**kwargs):
    if not len(cat_cols) and not len(bi_cols):
        return X_train,X_test
    n_train = X_train.shape[0]
    if X_test is not None:
        X_total = pd.concat([X_train,X_test],axis=0)
    else:
        X_total = X_train.copy()
    if len(cat_cols):
        X_total = pd.get_dummies(X_total,columns=cat_cols,drop_first=False)
    if len(bi_cols):
        X_total = pd.get_dummies(X_total,columns=bi_cols,drop_first=True)
    return X_total.iloc[:n_train].copy(), X_total.iloc[n_train:].copy() if X_test is not None else None

# preprocessing
def preprocessing_general(X_train,X_test=None,**kwargs):
    X_train,X_test = process_missing_values(X_train,X_test,**kwargs)
    X_train,X_test = minmax_scale_num_cols(X_train,X_test,**kwargs)
    X_train,X_test = one_hot_cat(X_train,X_test,**kwargs)
    return X_train,X_test



