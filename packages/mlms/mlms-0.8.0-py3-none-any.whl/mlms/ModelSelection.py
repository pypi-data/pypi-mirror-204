
# Load libraries

import pandas as pd
from time import time

from tqdm.notebook import tqdm
from sklearn.metrics import mean_squared_error, accuracy_score, f1_score, precision_score,\
                            recall_score, roc_auc_score, r2_score, balanced_accuracy_score
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import IPython.display
from tqdm.notebook import tqdm
tqdm.pandas()

from sklearn.pipeline import Pipeline
# Machine learning algos
from xgboost import XGBClassifier
# from lightgbm import LGBMClassifier
# from sklearn.preprocessing import StandardScaler, MinMaxScaler, QuantileTransformer
from sklearn.model_selection import KFold, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import SGDClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier, ExtraTreesClassifier

import xgboost as xgb
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.neural_network import MLPRegressor



#Diable the warnings
import warnings
warnings.filterwarnings("ignore") 

def Select_Classifier(scoring, K_folds,X_train, X_test, y_train, y_test,MODELS):

        # models.append(('LR', LinearRegression()))
        # models.append(('Lasso', Lasso()))
        # models.append(('Ridge', Ridge()))
        # models.append(('EN', ElasticNet()))


        ML_MODELS = [('LGR', LogisticRegression(max_iter=10000,solver= 'saga',random_state=42,n_jobs=-1,class_weight='balanced')),
                     ('AB',  AdaBoostClassifier()),
                     ('CART',DecisionTreeClassifier(class_weight='balanced',random_state=42)),
                      ('GBC', GradientBoostingClassifier(random_state=42)),
                      ('XGBC', XGBClassifier(eval_metric=['logloss','auc','error'])),
                      ('RFC', RandomForestClassifier(n_jobs=-1,random_state=42,class_weight='balanced')),
                      ('ETC', ExtraTreeClassifier(random_state=42,class_weight='balanced')),
                      ('KNN', KNeighborsClassifier(n_jobs=-1)),
                      ('NB',  GaussianNB()),
                      ('SVC', SVC(max_iter=10000,class_weight='balanced', random_state=42)),
                      ('MLP', MLPClassifier()),
                      ('SGDC',SGDClassifier(n_jobs=-1,class_weight='balanced', random_state=42)),
                      ('GPC', GaussianProcessClassifier(n_jobs=-1,random_state=42)),
                      ('PAC', PassiveAggressiveClassifier(n_jobs=-1,class_weight='balanced', random_state=42))
                      ]

        abb = []
        for m in ML_MODELS:
            abb.append(m[0])

        for m in MODELS:
            if m not in abb:
                print('ERROR: {m} is not a valid model!'.format(m=m))
            else:
                pass


        models = []
        for index,m in enumerate(ML_MODELS):
            # print(index, m[0])
            for M in MODELS:
                if M == m[0]:
                    models.append(ML_MODELS[index])
                else:
                    pass
        
   
        names = []
        kfold_results = []
        test_results = []
        train_results = []

        if scoring == 'accuracy':
            metrics = accuracy_score      
        if scoring == 'balanced_accuracy':
            metrics = balanced_accuracy_score   
        elif scoring == 'f1_score':
            metrics = f1_score
        elif scoring == 'precision':
            metrics = precision_score
        elif scoring == 'recall':
            metrics = recall_score
        elif scoring == 'roc_auc':
            metrics = roc_auc_score
        elif scoring == 'neg_mean_squared_error':
            metrics = mean_squared_error

        df_results = pd.DataFrame(columns=['names','train_results','test_results','time_secs','kfold_results'])

        for name, model in tqdm(models):

            start = time()
            names.append(name)     
            ## K Fold analysis:  
            kfold = KFold(n_splits=K_folds, random_state=42,shuffle=True)

            if scoring == 'neg_mean_squared_error':
                # converted mean square error to positive. The lower the beter
                cv_results = -1* cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
            else:
                cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)

            kfold_results.append(cv_results)

            # Full Training period
            res = model.fit(X_train, y_train)
            train_result = metrics(res.predict(X_train), y_train)
            train_results.append(train_result)

            # validation results 
            test_result = metrics(res.predict(X_test), y_test)
            test_results.append(test_result)

            looptime = time() - start 

            df_results = df_results.append({'names':name,
                                            'train_results':train_result,
                                            'test_results':test_result,
                                            'kfold_results':cv_results,
                                            'time_secs':looptime},
                                            ignore_index=True)

            df_results['kfold_mean'] = df_results['kfold_results'].apply(lambda x: x.mean())
            df_results['kfold_std'] = df_results['kfold_results'].apply(lambda x: x.std())     
        # IPython.display.clear_output()

        return df_results.set_index('names'), models



def Select_Regressor(scoring, K_folds,time_series,X_train, X_test, y_train, y_test):

    models = []

    models.append(('KNN', KNeighborsRegressor()))
    models.append(('CART', DecisionTreeRegressor()))
    models.append(('SVR', SVR()))
    #Neural Network
    models.append(('MLP', MLPRegressor()))

    models.append(('ABR', AdaBoostRegressor()))
    models.append(('GBR', GradientBoostingRegressor()))
    models.append(('XGB', xgb.XGBRegressor(n_jobs=-1)))
    # models.append(('LGBM',lightgbm.LGBMRegressor(n_jobs=-1)))
    # Bagging methods
    models.append(('RFR', RandomForestRegressor()))
    models.append(('ETR', ExtraTreesRegressor()))

    names = []
    kfold_results = []
    test_results = []
    train_results = []

    if scoring == 'r2_score':
        metrics = r2_score     
    elif scoring == 'neg_mean_squared_error':
        metrics = mean_squared_error

    df_results = pd.DataFrame(columns=['names','train_results','test_results','time_secs','kfold_results'])

    for name, model in tqdm(models):

        start = time()
        names.append(name)     
        ## K Fold analysis:  
        if time_series == True:
            kfold = KFold(n_splits=K_folds, random_state=None,shuffle=False)
        else:
            kfold = KFold(n_splits=K_folds, random_state=42,shuffle=True)

        if scoring == 'neg_mean_squared_error':
            # converted mean square error to positive. The lower the beter
            cv_results = -1* cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
        else:
            cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)

        kfold_results.append(cv_results)

        # Full Training period
        res = model.fit(X_train, y_train)
        train_result = metrics(res.predict(X_train), y_train)
        train_results.append(train_result)

        # validation results 
        test_result = metrics(res.predict(X_test), y_test)
        test_results.append(test_result)

        looptime = time() - start 

        df_results = df_results.append({'names':name,
                                        'train_results':train_result,
                                        'test_results':test_result,
                                        'kfold_results':cv_results,
                                        'time_secs':looptime},
                                        ignore_index=True)

        df_results['kfold_mean'] = df_results['kfold_results'].apply(lambda x: x.mean())
        df_results['kfold_std'] = df_results['kfold_results'].apply(lambda x: x.std())     
    # IPython.display.clear_output()

    return df_results.set_index('names'), models