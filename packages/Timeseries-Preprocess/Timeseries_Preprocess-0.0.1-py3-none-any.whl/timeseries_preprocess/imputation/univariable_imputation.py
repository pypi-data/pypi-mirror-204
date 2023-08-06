import pandas as pd
import numpy as np

def mean_imputation(dataframe, column):
    """
    Imputes missing values in a column with the mean of the non-missing values.
    """
    mean = np.mean(dataframe[column])
    dataframe[column].fillna(mean, inplace=True)
    return dataframe

def median_imputation(dataframe, column):
    """
    Imputes missing values in a column with the median of the non-missing values.
    """
    median = np.median(dataframe[column])
    dataframe[column].fillna(median, inplace=True)
    return dataframe
