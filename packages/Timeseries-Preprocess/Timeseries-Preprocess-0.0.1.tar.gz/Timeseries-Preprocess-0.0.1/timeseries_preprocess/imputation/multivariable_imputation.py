# import necessary modules
import pandas as pd
import numpy as np

def multivariable_mean_imputation(dataframe):
    """
    Imputes missing values in all columns with the mean of the non-missing values.
    """
    mean = dataframe.mean()
    dataframe.fillna(mean, inplace=True)
    return dataframe

def multivariable_median_imputation(dataframe):
    """
    Imputes missing values in all columns with the median of the non-missing values.
    """
    median = dataframe.median()
    dataframe.fillna(median, inplace=True)
    return dataframe