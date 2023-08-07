import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import learning_curve,validation_curve
import matplotlib.pyplot as plt
from sklearn.inspection import PartialDependenceDisplay, permutation_importance
import pandas as pd
import plotly.express as px
from dtreeviz.trees import *
from sklearn.tree import export_graphviz
import graphviz
from matplotlib.cm import get_cmap
import plotly.graph_objects as go

def plot_learning_curve(
    estimator,
    title,
    X,
    y,
    axes=None,
    ylim=None,
    cv=None,
    n_jobs=-1,
    scoring=None,
    train_sizes=np.linspace(0.1, 1.0, 5),
    save_fig=False,
    figsize=(20,5),
    seed=42
):
    if axes is None:
        _, axes = plt.subplots(1, 2, figsize=figsize)

    axes[0].set_title(title)
    if ylim is not None:
        axes[0].set_ylim(*ylim)
    axes[0].set_xlabel("Training examples")
    axes[0].set_ylabel("Score")

    train_sizes, train_scores, test_scores, fit_times, _ = learning_curve(
        estimator,
        X,
        y,
        scoring=scoring,
        cv=cv,
        n_jobs=n_jobs,
        train_sizes=train_sizes,
        return_times=True,
        random_state=seed
    )
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    fit_times_mean = np.mean(fit_times, axis=1)
    fit_times_std = np.std(fit_times, axis=1)

    # Plot learning curve
    axes[0].grid()
    axes[0].fill_between(
        train_sizes,
        train_scores_mean - train_scores_std,
        train_scores_mean + train_scores_std,
        alpha=0.1,
        color="r",
    )
    axes[0].fill_between(
        train_sizes,
        test_scores_mean - test_scores_std,
        test_scores_mean + test_scores_std,
        alpha=0.1,
        color="g",
    )
    axes[0].plot(
        train_sizes, train_scores_mean, "o-", color="r", label="Training score"
    )
    axes[0].plot(
        train_sizes, test_scores_mean, "o-", color="g", label="Cross-validation score"
    )
    axes[0].legend(loc="best")

    # Plot n_samples vs fit_times
    axes[1].grid()
    axes[1].plot(train_sizes, fit_times_mean, "o-")
    axes[1].fill_between(
        train_sizes,
        fit_times_mean - fit_times_std,
        fit_times_mean + fit_times_std,
        alpha=0.1,
    )
    axes[1].set_xlabel("Training examples")
    axes[1].set_ylabel("fit_times")
    axes[1].set_title("Scalability of the model")

    plt.grid()
    if save_fig:
        plt.savefig(f'img/learning_curve_{str(estimator)}.png')
    return plt


# # Cross validation with 50 iterations to get smoother mean test and train
# # score curves, each time with 20% data randomly selected as a validation set.
# cv = ShuffleSplit(n_splits=50, test_size=0.2, random_state=0)
def plot_validation_curve(
    estimator,
    title,
    X,
    y,
    ylim=None,
    cv=None,
    param_range=None,
    param_name=None,
    is_log=False,
    n_jobs=-1,
    scoring=None,
    save_fig=False,
    figsize=(20,5),
    fill_between=True,
    enumerate_x=False
):
    train_scores, test_scores = validation_curve(
            estimator,
            X,
            y,
            param_name=param_name,
            param_range=param_range,
            scoring=scoring,
            n_jobs=n_jobs,
            cv=cv,
            )
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.figure(figsize=figsize)
    plt.title(title)
    plt.xlabel(param_name)
    plt.ylabel("Score")
    if is_log:
        plt.semilogx(param_range, train_scores_mean, marker="o",label="Training score", color="r")
        plt.semilogx(param_range, test_scores_mean, marker="o",label="Cross-validation score", color="g")

    else:
        tmp = param_range
        if enumerate_x:
            tmp = np.arange(1,len(tmp)+1)
        plt.plot(tmp, train_scores_mean, "o-", color="r", label="Training score")
        plt.plot(tmp, test_scores_mean, "o-", color="g", label="Cross-validation score")


    if fill_between:
        plt.fill_between(
            param_range,
            train_scores_mean - train_scores_std,
            train_scores_mean + train_scores_std,
            alpha=0.1,
            color="r",
        )
        plt.fill_between(
            param_range,
            test_scores_mean - test_scores_std,
            test_scores_mean + test_scores_std,
            alpha=0.1,
            color="g",
        )
    if ylim is not None:
        plt.ylim(*ylim)
    plt.grid()
    plt.legend(loc="best")
    if save_fig:
        plt.savefig(f'img/val_curve_{str(estimator)}_{param_name}.png')
    return plt

def params_2D_heatmap(search_cv,param1,param2,scoring,log_param1=False,log_param2=False,figsize=(20,10),min_hm=None,max_hm=None, negative_score=False):
    rs_df = pd.DataFrame(search_cv.cv_results_)
    cm = plt.cm.get_cmap('RdYlBu')
    z = rs_df[f'mean_test_{scoring}'].values
    if negative_score:
        z*=-1
    x = rs_df[f'param_{param1}'].values
    y = rs_df[f'param_{param2}'].values
    plt.figure(figsize=figsize)
    sc = plt.scatter(x, y, c=z, vmin=z.min() if not min_hm else min_hm, vmax=z.max() if not max_hm else max_hm, s=20, cmap=cm)
    if log_param2:
        plt.yscale('log')
    if log_param1:
        plt.xscale('log')
    plt.colorbar(sc)
    plt.xlabel(param1)
    plt.ylabel(param2)
    plt.grid()
    plt.show()

def params_3D_heatmap(search_cv,param1,param2,param3,scoring,log_param1=False,log_param2=False,log_param3=False):
    rs_df = pd.DataFrame(search_cv.cv_results_)
    scores = rs_df[f'mean_test_{scoring}'].values
    fig = px.scatter_3d(rs_df, x=f'param_{param1}', y=f'param_{param2}', z=f'param_{param3}',
                    color=f'mean_test_{scoring}',range_color=[scores.min(),scores.max()],
                       log_x = log_param1, log_y=log_param2, log_z=log_param3)
    fig.show()


def plot_tree_dtreeviz(estimator,X,y,target_name,class_names,depth_range_to_display=None,fancy=False,new_window=False):
    viz = dtreeviz(estimator,X,y,target_name=target_name,feature_names=X.columns.values,
                   class_names=class_names,depth_range_to_display=depth_range_to_display,
                  orientation='LR',instance_orientation='LR',fancy=fancy)
    if new_window:
        viz.view()
    return viz

def plot_tree_sklearn(estimator,feature_names,class_names,size=30,ratio=0.2,rotate=True,fname='tmp'):
    s = export_graphviz(estimator,out_file=None,feature_names=feature_names,filled=True,class_names=class_names,
                       special_characters=True,rotate=rotate,rounded=True)
    graph = graphviz.Source(s,format='png')
    graph.render(Path('images')/fname)

def plot_feature_importances(importances,col_names,figsize=(20,10),top_n=None):
    fea_imp_df = pd.DataFrame(data={'Feature':col_names,'Importance':importances}).set_index('Feature')
    fea_imp_df = fea_imp_df.sort_values('Importance', ascending=False)
    if top_n is not None:
        fea_imp_df = fea_imp_df.head(top_n)
    fea_imp_df.plot(kind='barh',figsize=figsize)
    return fea_imp_df


def plot_permutation_importances(best_model,X,y,scoring=['f1_macro'],n_repeats=10,seed=42,top_n=None,figsize=(20,10)):
    r_multi = permutation_importance(best_model, X, y, n_repeats=n_repeats, random_state=42, scoring=scoring)
    fea_imp_dfs=[]
    for metric in r_multi.keys():
        print(f"{metric}")
        r = r_multi[metric]        
        fea_imp_df  = pd.DataFrame(data={'Feature':X.columns.values,'Importance':r['importances_mean'],'STD':r['importances_std']}).set_index('Feature')
        fea_imp_df = fea_imp_df.sort_values(['Importance'],ascending=True)
        if top_n is not None:
            fea_imp_df = fea_imp_df.head(top_n)
        fig, ax = plt.subplots()
        fea_imp_df['Importance'].plot(kind='barh',figsize=figsize,xerr=r['importances_std'],ax=ax)
        ax.set_title("Feature importances using permutation on full model")
        ax.set_ylabel("Mean metric decrease")
        fig.tight_layout()
        plt.show()
        fea_imp_dfs.append(fea_imp_df)
    return fea_imp_dfs

def plot_confusion_matrix(y_true,y_pred,labels=None):
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=labels)
    disp.plot()
    plt.show()

def draw_sankey(data, target,chart_name,save_name=None):
    PATH = Path('sk_reports')
    unique_source_target = list(pd.unique(data[['source', 'target']].values.ravel('K')))
    mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
    data = data.copy()
    data['source'] = data['source'].map(mapping_dict)
    data['target'] = data['target'].map(mapping_dict)
    links_dict = data.to_dict(orient='list')

    nodes = np.unique(data[["source", "target"]], axis=None)
    nodes = pd.Series(index=nodes, data=range(len(nodes)))


    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = unique_source_target,
          # color = [px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i in nodes.loc[data["source"]]]
        ),
        link = dict(
          source = links_dict["source"],
          target = links_dict["target"],
          value = links_dict[target],
          color = [px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i in nodes.loc[data["source"]]],
      ))])
    fig.update_layout(title_text=chart_name, font_size=10)
    fig.show()
    if save_name: fig.write_html(str(PATH/save_name)+ '.html')

    
def pdp_numerical_only(best_model,df,num_features,y_class,y_colors=None,ncols=2,nrows=2,figsize=(20,16)):
    common_params = {
    "subsample": 40,
    "n_jobs": 2,
    "grid_resolution": 100,
    "random_state": 42,
    }

    features_info = {
        # features of interest
        "features": num_features,
        # type of partial dependence plot
        "kind": "average",
        # information regarding categorical features
        "categorical_features": None,
    }

    _, ax = plt.subplots(ncols=ncols, nrows=nrows, figsize=figsize, constrained_layout=True)
    if y_colors is None:
        y_colors = get_cmap('tab10').colors

    for i in range(len(y_class)):
        _display = PartialDependenceDisplay.from_estimator(
                            best_model,
                            df,
                            **features_info,
                            target=i,
                            line_kw={"label": y_class[i],'color':y_colors[i]},
                            ax=ax,
                            **common_params
        )

def pdp_categorical_only(best_model,df,cat_feature,y_class,y_colors=None,ymax=0.5,figsize=(20,8)):
    common_params = {
    "subsample": 40,
    "n_jobs": 2,
    "grid_resolution": 100,
    "random_state": 42,
    }

    features_info = {
        # features of interest
        "features": [cat_feature],
        # type of partial dependence plot
        "kind": "average",
        # information regarding categorical features
        "categorical_features": [cat_feature],
    }
    if y_colors is None:
        y_colors = get_cmap('tab10').colors

    # axs=[]
    displays=[]
    for i in range(len(y_class)): 
        _, ax = plt.subplots(figsize=(1,1))

        _display = PartialDependenceDisplay.from_estimator(
            best_model,
            df,
            **features_info,
            target=i,
            line_kw={"label": y_class[i],'color':y_colors[i]},
            ax=ax,
            **common_params,
        );
        displays.append(_display)
        # axs.append(ax)
    

    
    fig, axes = plt.subplots(1, len(displays), figsize=figsize,sharey=True)
#     ax1.set_ylim([0, ymax])
#     ax2.set_ylim([0, ymax])
#     ax3.set_ylim([0, ymax])
    for i in range(len(displays)):
        displays[i].plot(ax=axes[i],pdp_lim={1: (0, ymax)})
        axes[i].set_title(y_class[i])
    

def plot_ice_pair(best_model,df,pair_features,class_idx,figsize=(10,4)):
    common_params = {
        "subsample": 40,
        "n_jobs": 2,
        "grid_resolution": 100,
        "random_state": 42,
    }
    fea_to_plot = pair_features
    features_info = {
        # features of interest
        "features": [fea_to_plot[0],fea_to_plot[1], fea_to_plot],
        # type of partial dependence plot
        "kind": "average",
        # information regarding categorical features
        "categorical_features": None,
    }

    _, ax = plt.subplots(ncols=3, figsize=figsize, constrained_layout=True)

    _display = PartialDependenceDisplay.from_estimator(
        best_model,
        df,
        **features_info,
        target=class_idx,
        ax=ax,
        **common_params,
    )
    plt.setp(_display.deciles_vlines_, visible=False)
