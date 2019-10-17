import pandas as pd
import numpy as np



# Create functions to do cross validation on the training set of data for different models
import xgboost as xgb
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate, KFold, StratifiedKFold, learning_curve, GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV, LogisticRegression, LogisticRegressionCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, LabelEncoder, normalize, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, precision_score, recall_score
from sklearn.metrics import confusion_matrix, f1_score, roc_auc_score, roc_curve, precision_recall_curve
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)



def cross_metrics_simple(n_folds, X_train, y_train):
    '''
    Function that outputs the 4 scoring metrics: [accuracy, precision, recall, and f1]
        for each of the classifiers in list clf_models
    args:
        n_folds: enter number of cross validation folds to test on. Integer value defaults to StratifiedKFolds
        X_train: Features separate from the hold-out/test set
        y_train: Predictor class separate from the hold-out/test set
    '''
    clf_models = [
        LogisticRegression(),
        DecisionTreeClassifier(),
        RandomForestClassifier(),
        GaussianNB(),

    ]

    for clf in clf_models:
        pipe = Pipeline([('scalar', StandardScaler()),
                         ('clf', clf)
                        ])

        print(type(clf).__name__,'Cross Validation Scores')
        print('Accuracy : {:4.6f}'.format(np.mean(cross_val_score(pipe, X_train, y_train, cv = n_folds, scoring = 'accuracy'))))
        print('Precision: {:4.6f}'.format(np.mean(cross_val_score(pipe, X_train, y_train, cv = n_folds, scoring = 'precision'))))
        print('Recall   : {:4.6f}'.format(np.mean(cross_val_score(pipe, X_train, y_train, cv = n_folds, scoring = 'recall'))))
        print('F1 Score : {:4.6f}'.format(np.mean(cross_val_score(pipe, X_train, y_train, cv = n_folds, scoring = 'f1'))),'\n')
    return None


def cross_metrics_detailed(n_folds, X_train, y_train):
    '''
    Function that outputs the 4 scoring metrics: [accuracy, precision, recall, and f1]
        for each of the classifiers in list clf_models. Lists metrics for both the test and training set
        along with the fit and score times for each model
    args:
        n_folds: enter number of cross validation folds to test on. Integer value defaults to StratifiedKFolds
        X_train: Features separate from the hold-out/test set
        y_train: Predictor class separate from the hold-out/test set
    '''

    clf_models = [
        LogisticRegression(),
        DecisionTreeClassifier(),
        RandomForestClassifier(),
        GaussianNB()
    ]

    for clf in clf_models:
        pipe = Pipeline([('scalar', StandardScaler()),
                         ('clf', clf)
                        ])

        print(type(clf).__name__,'Cross Validation Scores')
        print(pd.DataFrame(cross_validate(clf, X_train, y_train, cv = n_folds, scoring = ['accuracy', 'precision', 'recall', 'f1'],
                                          return_train_score = True)).mean(),'\n')
    return None


def cross_metrics_poly(n_folds, poly_deg, X_train, y_train):
    '''
    Function that outputs the 4 scoring metrics: [accuracy, precision, recall, and f1]
        for each of the classifiers in list clf_models
    args:
        n_folds: enter number of cross validation folds to test on. Integer value defaults to StratifiedKFolds
        X_train: Features separate from the hold-out/test set
        y_train: Predictor class separate from the hold-out/test set
    '''
    clf_models = [
        LogisticRegression(),
        DecisionTreeClassifier(),
        RandomForestClassifier(),
        SVC(),
        GaussianNB()
    ]

    for clf in clf_models:
        pipe = Pipeline([('polynomial', PolynomialFeatures(degree = poly_deg)),
                         ('scalar', StandardScaler()),
                         ('clf', clf)
                        ])

        print(type(clf).__name__,'Cross Validation Scores')
        print('Accuracy : {:4.6f}'.format(np.mean(cross_val_score(pipe, X_train, y_train, cv = n_folds, scoring = 'accuracy'))))
        print('Precision: {:4.6f}'.format(np.mean(cross_val_score(pipe, X_train, y_train, cv = n_folds, scoring = 'precision'))))
        print('Recall   : {:4.6f}'.format(np.mean(cross_val_score(pipe, X_train, y_train, cv = n_folds, scoring = 'recall'))))
        print('F1 Score : {:4.6f}'.format(np.mean(cross_val_score(pipe, X_train, y_train, cv = n_folds, scoring = 'f1'))),'\n')
    return None
