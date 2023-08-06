import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import seaborn as sns
import time, os, sys
from scipy.optimize import minimize
fmt = mtick.FuncFormatter(lambda x,pos:"{:.1%}".format(x))

# -----------------------------------------------------------------------------------------------------------------
# Loads some real world sklearn toy datasets
from sklearn.datasets import load_breast_cancer, load_iris
# Loads some artificial sklearn toy dataset generators
from sklearn.datasets import make_blobs, make_circles, make_classification, make_moons

# Some basic imputer
from sklearn.impute import SimpleImputer

# Model selection functions and classes
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score

# -----------------------------------------------------------------------------------------------------------------
# Preprocessors
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures, MinMaxScaler

# Preprocess pandas DataFrame columns
from sklearn.compose import make_column_selector, make_column_transformer
# Acts like a preprocessor for the target variable. It's also a wrapper for your regular regressor
from sklearn.compose import TransformedTargetRegressor

# Pipeline
from sklearn.pipeline import make_pipeline

# -----------------------------------------------------------------------------------------------------------------
# Used to create custom regressor/classifier classes
from sklearn.base import BaseEstimator, TransformerMixin

# Naive classifier to act as a baseline
from sklearn.dummy import DummyClassifier

# k-nearest neighbors classifier
from sklearn.neighbors import KNeighborsClassifier

# -----------------------------------------------------------------------------------------------------------------
# Sklearn linear regression models
from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression

# SVM kernel-based classifier
from sklearn.svm import SVC

# Decision tree
from sklearn.tree import DecisionTreeRegressor, plot_tree

# Some ensemble methods 
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, VotingClassifier

# Neural networks
from sklearn.neural_network import MLPClassifier, MLPRegressor

# -----------------------------------------------------------------------------------------------------------------
# Some metrics to evaluate the model
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, max_error
from sklearn.metrics import mean_absolute_percentage_error as MAPE, mean_squared_error as MSE
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix

# Used together with the warnings package
from sklearn.exceptions import ConvergenceWarning