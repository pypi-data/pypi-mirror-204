from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_validate, train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier
from sklearn.metrics import f1_score,accuracy_score,classification_report,log_loss
import numpy as np
import pandas as pd
import statsmodels
from chart_plotting import plot_confusion_matrix,plot_permutation_importances

def run_logistic_regression(df,y_col,multi_class='multinomial',solver='newton-cg',max_iter=10000):
    # only for multinomial classification
    y_true = df[y_col].values
    df_trn = df.drop(y_col,axis=1)
    model = LogisticRegression(random_state=0, multi_class=multi_class, penalty=None, solver=solver,max_iter=10000).fit(df_trn, y_true)
    preds = model.predict(df_trn)
    prob_preds = model.predict_proba(df_trn)
    print('-'*100)
    print('Intercept: \n', model.intercept_)
    print('Coefficients: \n', model.coef_)
    print('Coefficients exp :\n',np.exp(model.coef_))

    print('-'*100)
    print('Log loss: ',log_loss(y_true,prob_preds))
    print('-'*100)
    print(classification_report(y_true,preds))

def run_multinomial_statmodel(df,y_col,add_constant=False):
    y_trn = df[y_col].values
    df_trn = df.drop(y_col,axis=1)

    if add_constant:
        df_trn = statsmodels.api.add_constant(df_trn)
    logit_model=statsmodels.api.MNLogit(y_trn,df_trn)
    print(logit_model)
    result=logit_model.fit()
    stats1=result.summary()
    print(stats1)
    prob_preds = logit_model.predict(params = result.params.values)
    print('-'*100)
    print('Log loss: ',log_loss(y_trn,prob_preds))
    print('-'*100)
    print(classification_report(y_trn,np.argmax(prob_preds,axis=1)+1))


def run_sklearn_classification_model(model_name,model_params,df,y_col,y_classes,val_ratio=0.2,seed=42,plot_fea_imp=True):
    df = df.copy().reset_index(drop=True)
    df_trn = df.drop(y_col,axis=1)
    # trn_cols = df.drop(y_col,axis=1).columns.values
    np.random.seed(seed)
    if val_ratio is None:
        y_trn = df[y_col].values
        X_trn = df_trn.values
    else:
        X_trn,X_test,y_trn,y_test = train_test_split(df_trn.values,df[y_col].values,test_size=val_ratio,random_state=seed)
    
    if model_name=='DT':
        _model = DecisionTreeClassifier(random_state=seed,**model_params)
    elif model_name=='AdaBoost':
        dt_params={k.split('__')[1]:v for k,v in model_params.items() if 'base_estimator' in k}
        abc_params={k:v for k,v in model_params.items() if 'base_estimator' not in k}        
        print(f'Decision Tree params: {dt_params}')
        print(f'AdaBoost params: {abc_params}')
        dt = DecisionTreeClassifier(random_state=seed,**dt_params)
        _model = AdaBoostClassifier(base_estimator=dt,random_state=seed,algorithm='SAMME',**abc_params)
    elif model_name=='RF':
        _model = RandomForestClassifier(random_state=seed,**model_params)
    else:
        print('Unsupported model')
        return

    _model = _model.fit(X_trn,y_trn)
    
    pred_trn = _model.predict(X_trn)
    prob_trn = _model.predict_proba(X_trn)

    print('-'*30 + ' Train set ' + '-'*30)
    print(f'Log loss: {log_loss(y_trn,prob_trn)}')
    print(classification_report(y_trn, pred_trn, target_names=y_classes))
    
    if val_ratio is not None:
        pred_val = _model.predict(X_test)
        prob_val = _model.predict_proba(X_test)
        print('-'*30 + ' Test set ' + '-'*30)
        print(f'Log loss: {log_loss(y_test,prob_val)}')
        print(classification_report(y_test, pred_val, target_names=y_classes))

        print('-'*100)
        df2 = pd.DataFrame({'Class': y_classes,
                            'True Distribution':pd.Series(y_test).value_counts(normalize=True).sort_index(),
                           'Prediction Distribution':pd.Series(pred_val).value_counts(normalize=True).sort_index()}
                          )
        print(df2)
        plot_confusion_matrix(y_test,pred_val,y_classes)
    
    if plot_fea_imp:
        # plot_feature_importances(_model.feature_importances_,trn_df.columns.values)
        _ = plot_permutation_importances(_model,df_trn,
                                y_trn)
    
    return _model,prob_trn


def tune_sklearn_classification_model(model_name,param_grid,df,y_col,custom_cv=5,random_cv_iter=None,seed=42,rank_show=10):
    y_trn = df[y_col].values
    df_trn = df.drop(y_col,axis=1)

    if model_name=='DT':
        _model = DecisionTreeClassifier(random_state=seed)
    elif model_name=='AdaBoost':
        dt = DecisionTreeClassifier(random_state=seed)
        _model = AdaBoostClassifier(base_estimator= dt,random_state=seed,algorithm='SAMME')
    elif model_name=='RF':
        _model = RandomForestClassifier(random_state=seed)
    else:
        print('Unsupported model')
        return
    
    search_cv,default_cv = do_param_search(df_trn,y_trn,_model,param_grid,cv=custom_cv,scoring=['f1_macro','accuracy'],random_cv_iter = random_cv_iter,seed=seed)
    show_both_cv(search_cv,default_cv,'f1_macro',rank_show)
    return search_cv


### hyperparam tuning

def do_param_search(
    X_train,y_train,
    estimator,
    param_grid,
    random_cv_iter=None,
    include_default=True,
    cv=None,
    scoring=None,
    seed=42
    
):
    search_cv,default_cv=None,None
    if random_cv_iter:
        search_cv = RandomizedSearchCV(estimator=estimator,
                                      n_iter=random_cv_iter,
                                      param_distributions=param_grid,
                                      scoring=scoring,
                                      n_jobs=-1,
                                      cv=cv,
                                        return_train_score=True,
                                      verbose=1,refit=False,random_state=seed)
        search_cv.fit(X_train,y_train)
    else:
        search_cv = GridSearchCV(estimator,param_grid,scoring=scoring,n_jobs=-1,cv=cv,verbose=1,
                                 return_train_score=True,refit=False)
        search_cv.fit(X_train,y_train)
    if include_default:
        default_cv = cross_validate(estimator,X_train,y_train,scoring=scoring,cv=cv,n_jobs=-1,verbose=1,
                                   return_train_score=True)
    return search_cv,default_cv
        

def summarize_cv_results(search_cv,scoring,top_n=10):
    search_cv = pd.DataFrame(search_cv.cv_results_)
    search_cv = search_cv.sort_values(f'rank_test_{scoring}')
    for rec in search_cv[['params',f'mean_train_{scoring}',f'std_train_{scoring}',f'mean_test_{scoring}',f'std_test_{scoring}',f'rank_test_{scoring}']].values[:top_n]:
        print('-'*10)
        print(f'Rank {rec[-1]}')
        print(f'Params: {rec[0]}')
        print(f'Mean train score: {rec[1]:.3f} +- {rec[2]:.3f}')
        print(f'Mean test score: {rec[3]:.3f} +- {rec[4]:.3f}')

def summarize_default_cv(default_cv,s):
    print('-'*10)
    print("Default Params")
    print(f"Mean train score: {round(default_cv[f'train_{s}'].mean(),3)} +- {round(default_cv[f'train_{s}'].std(),3)}")
    print(f"Mean test score: {round(default_cv[f'test_{s}'].mean(),3)} +- {round(default_cv[f'test_{s}'].std(),3)}")

def show_both_cv(search_cv,default_cv,scoring,top_n=10):
    summarize_cv_results(search_cv,scoring,top_n)
    summarize_default_cv(default_cv,scoring)
    
def get_adaboost_info(dt_params,ada_params,X,y,seed=42):
    dt = DecisionTreeClassifier(random_state=seed,**dt_params)
    abc = AdaBoostClassifier(base_estimator=dt,random_state=seed,**ada_params)
    abc.fit(X,y)
    for i,t in enumerate(abc.estimators_):
        print(f'{t}\n\tTree depth: {t.tree_.max_depth}, Weight: {abc.estimator_weights_[i]}, Error: {abc.estimator_errors_[i]}')
    return abc
