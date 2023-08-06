import pandas as pd
import plotly.graph_objects as go
# plot ROC AUC curve 
from sklearn.metrics import roc_curve, auc
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
import chart_studio.plotly as py
import plotly.offline as py
py.init_notebook_mode()
import cufflinks

from sklearn.metrics import roc_curve, roc_auc_score

def Multiclass_ROC_Curve(X_test, y_test, fitted_model, chart_title:str):
    # This function is to plot ROC Curce

    y_scores = fitted_model.predict_proba(X_test)
    # One hot encode the labels in order to plot them
    y_onehot = pd.get_dummies(y_test, columns=fitted_model.classes_)
    
    # Create an empty figure, and iteratively add new lines
    # every time we compute a new class
    fig = go.Figure()
    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0=0, x1=1, y0=0, y1=1)

    for i in range(y_scores.shape[1]):
        y_true = y_onehot.iloc[:, i]
        y_score = y_scores[:, i]

        fpr, tpr, _ = roc_curve(y_true, y_score)
        auc_score = roc_auc_score(y_true, y_score)

        name = f"{y_onehot.columns[i]} (AUC={auc_score:.3f})"
        fig.add_trace(go.Scatter(x=fpr, y=tpr, name=name, mode='lines'))

    fig.update_layout(
        title = '{title}'.format(title=chart_title),
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        yaxis=dict(scaleanchor="x", scaleratio=1),
        xaxis=dict(constrain='domain'),
        width=700, height=600)
    fig.show()



def Binary_ROC_Curve(y_true, y_pred,chart_name:str):
    
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)

    fig = px.area(
        x=fpr, y=tpr,
        title=f'{chart_name} ROC Curve (AUC={auc(fpr, tpr):.4f})'.format(chart_name=chart_name),
        labels=dict(x='False Positive Rate', y='True Positive Rate'),
        width=700, height=500)
    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0=0, x1=1, y0=0, y1=1)

    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.update_xaxes(constrain='domain')
    fig.show()