# Importing the warnings
import warnings as w

w.filterwarnings("ignore")
# Importing the Classification Libraries
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB

# Importing the metrics
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve,
    f1_score,
    precision_score,
    recall_score,
)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Importing Basic Libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.float_format", lambda x: "%.2f" % x)


# List of tuples of model name and models


def classification_model_comparison(X, y, scaling=None):
    """This function takes in the X , y dataframes and Scaling method and returns a dataframe with the metrics of the models.

    Args:
        X (pd.DataFrame): _description_
        y (pd.DataFrame): _description_
        scaling (str, optional): _description_. Defaults to None. (ss: StandardScaler, mm: MinMaxScaler)

    Returns:
        pd.DataFrame: The dataframe with the metrics of the models.
    """

    model_list = [
        ("LR", LogisticRegression()),
        ("DT", DecisionTreeClassifier()),
        ("RFC", RandomForestClassifier(n_estimators=200)),
        ("KNN", KNeighborsClassifier()),
        ("SVM", SVC()),
        ("XGB", XGBClassifier(verbosity=0)),
        ("CB", CatBoostClassifier(verbose=0)),
        ("GNB", GaussianNB()),
        ("BNB", BernoulliNB()),
    ]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=69, stratify=y
    )

    numerical_features = [feature for feature in X.columns if X[feature].nunique() > 10]

    if scaling == "ss":
        sc = StandardScaler()
        X_train[numerical_features] = sc.fit_transform(X_train[numerical_features])
        X_test[numerical_features] = sc.transform(X_test[numerical_features])
        pass
    elif scaling == "mm":
        mm = MinMaxScaler()
        X_train[numerical_features] = mm.fit_transform(X_train[numerical_features])
        X_test[numerical_features] = mm.transform(X_test[numerical_features])
        pass

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=69)

    df_metrics = {}

    for name, model in model_list:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        df_metrics[name] = {
            "Train Score": model.score(X_train, y_train),
            "Test Score": model.score(X_test, y_test),
            "Accuracy Score": accuracy_score(y_test, y_pred),
            "ROC AUC Score": roc_auc_score(y_test, y_pred),
            "F1 Score": f1_score(y_test, y_pred),
            "Precision Score": precision_score(y_test, y_pred),
            "Recall Score": recall_score(y_test, y_pred),
        }
        pass
    comparsion = pd.DataFrame(df_metrics).T
    comparsion.sort_values(by="ROC AUC Score", ascending=False, inplace=True)
    return comparsion


def report_print(model, X, y):
    """This function takes in the model name, X and y dataframes and prints
    the classification report, confusion matrix and ROC curve."""
    model_list = [
        ("LR", LogisticRegression()),
        ("DT", DecisionTreeClassifier()),
        ("RFC", RandomForestClassifier(n_estimators=200)),
        ("KNN", KNeighborsClassifier()),
        ("SVM", SVC()),
        ("XGB", XGBClassifier(verbosity=0)),
        ("CB", CatBoostClassifier(verbose=0)),
        ("GNB", GaussianNB()),
        ("BNB", BernoulliNB()),
    ]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=69, stratify=y
    )

    for model_name, model_object in model_list:
        if model_name == model:
            print(f"Model Name: {model}")
            model_object.fit(X_train, y_train)
            y_pred = model_object.predict(X_test)

            # Classification Report

            print(
                f"Classification Report for \n{classification_report(y_test, y_pred)}"
            )

            # Confusion Matrix
            
            plt.figure(figsize=(6, 6))
            cm = confusion_matrix(y_test, y_pred)
            sns.heatmap(cm, annot=True, fmt="d")
            plt.xlabel("Predicted")
            plt.ylabel("Truth")
            plt.title("Confusion Matrix")
            plt.show()

            # ROC Curve
            
            plt.figure(figsize=(6, 6))
            tpr, fpr, thresholds = roc_curve(y_test, y_pred)
            plt.plot(tpr, fpr, label="ROC")
            plt.plot([0, 1], [0, 1], "k--")
            plt.fill_between(tpr, fpr, alpha=0.5, color="blue")
            plt.fill_between([0, 1], [0, 1], color="white")
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate")
            plt.title("ROC Curve")
            plt.legend()
            plt.show()
