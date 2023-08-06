# Importing the Regression Libraries
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

# Importing the metrics and preprocessing libraries for regression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler


# Importing Basic Libraries
import numpy as np
import pandas as pd
import warnings as w

w.filterwarnings("ignore")
pd.set_option("display.float_format", lambda x: "%.2f" % x)


# Making a dataframe to store metrics and comparing the models
def regression_model_comparison(X, y, scaling=None):
    """This function takes in the X , y dataframes and Scaling method and Returns a dataframe with the metrics of the models.

    Args:
        X (pd.DataFrame): _description_
        y (pd.DataFrame): _description_
        scaling (str, optional): _description_. Defaults to None. (ss: StandardScaler, mm: MinMaxScaler)

    Returns:
        pd.DataFrame: The dataframe with the metrics of the models.
    """
    # Making a list of model names and model objects

    model_list = [
        ("Linear Regression", LinearRegression()),
        ("Ridge Regression", Ridge()),
        ("Lasso Regression", Lasso()),
        ("Decision Tree", DecisionTreeRegressor()),
        ("Random Forest", RandomForestRegressor()),
        ("KNN", KNeighborsRegressor()),
        ("SVR", SVR()),
        ("XGBoost", XGBRegressor()),
        ("CatBoost", CatBoostRegressor(verbose=False)),
    ]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=69
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

    df_metrics = {}

    # Fitting the models and storing the metrics
    for name, model in model_list:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        df_metrics[name] = {
            "Train Score": model.score(X_train, y_train),
            "Test Score": model.score(X_test, y_test),
            "MSE": mean_squared_error(y_test, y_pred),
            "MAE": mean_absolute_error(y_test, y_pred),
            "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
            "R2 Score": r2_score(y_test, y_pred),
        }
    # Comparing the models
    comparison = pd.DataFrame(df_metrics).T
    comparison.sort_values(by="R2 Score", ascending=False, inplace=True)
    return comparison
