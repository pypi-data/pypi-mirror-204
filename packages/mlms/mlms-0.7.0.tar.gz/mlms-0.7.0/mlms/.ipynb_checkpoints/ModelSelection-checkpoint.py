
# Load libraries

import pandas as pd

# import plotly
# import plotly.express as px
# import plotly.graph_objects as go
# import chart_studio.plotly as py
# import plotly.figure_factory as ff
# import plotly.offline as py
# py.init_notebook_mode()
# import cufflinks

from time import time

# from plotly.offline import iplot
# import cufflinks as cf
# cf.go_offline()
# # colab plot display
# import plotly.io as pio



# # Metrics
# from sklearn.metrics import classification_report, confusion_matrix, \
#       accuracy_score,plot_confusion_matrix,\
      # plot_roc_curve, roc_curve, roc_auc_score,auc
from tqdm.notebook import tqdm
from sklearn.metrics import mean_squared_error, accuracy_score, f1_score, precision_score,\
                            recall_score, roc_auc_score

# import pyLDAvis
# import pyLDAvis.gensim_models as gensimvis
# pyLDAvis.enable_notebook()
#Libraries for feature extraction and topic modeling

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation



# others

import IPython.display
from tqdm.notebook import tqdm
tqdm.pandas()
# self design module
# import pymssql
# from MSSQL import Acamar
from sklearn.pipeline import Pipeline
# Machine learning algos
from xgboost import XGBClassifier
# from lightgbm import LGBMClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler, QuantileTransformer
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
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

#Diable the warnings
import warnings
warnings.filterwarnings("ignore") 

def Select_Classifier(scoring, K_folds,X_train, X_test, y_train, y_test):

        models = []
        # models.append(('LR', LinearRegression()))
        # models.append(('Lasso', Lasso()))
        # models.append(('Ridge', Ridge()))
        # models.append(('EN', ElasticNet()))
        models.append(('LGR', LogisticRegression(n_jobs=-1)))
        # Boosting methods
        models.append(('AB',  AdaBoostClassifier()))
        models.append(('CART',DecisionTreeClassifier()))
        # models.append(('LGBM', LGBMClassifier()))
        models.append(('GBC', GradientBoostingClassifier()))
        models.append(('XGBC', XGBClassifier(eval_metric=['logloss','auc','error'])))
        # Bagging methods
        models.append(('RFC', RandomForestClassifier()))
        models.append(('ETC', ExtraTreeClassifier()))
        # models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier(n_jobs=-1)))
        models.append(('NB',  GaussianNB()))
        models.append(('SVC', SVC()))
        # Neural Network
        models.append(('MLP', MLPClassifier()))
        # others
        models.append(('SGDC',SGDClassifier(n_jobs=-1)))
        models.append(('GPC', GaussianProcessClassifier(n_jobs=-1)))
        models.append(('PAC', PassiveAggressiveClassifier(n_jobs=-1)))

        names = []
        kfold_results = []
        test_results = []
        train_results = []

        if scoring == 'accuracy':
            metrics = accuracy_score      
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

            # results = "{}: {} ({}) {} {} {}".format(name, cv_results.mean(), \
            #                                         cv_results.std(),\
            #                                               train_result, \
            #                                                 test_result,\
            #                                                     looptime)
            # print(results)    

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