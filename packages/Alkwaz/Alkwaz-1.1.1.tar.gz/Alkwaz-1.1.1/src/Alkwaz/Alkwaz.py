import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.utils import resample

class Alkwaz:
    
    @staticmethod
    def check_outliers(column):
        desc = column.describe()
        q1 = desc['25%']
        q3 = desc['75%']
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        outliers = column[(column < lower_bound) | (column > upper_bound)]
        return len(outliers)

    @staticmethod
    def check_balance(df, target_column):
        class_counts = df[target_column].value_counts()
        num_classes = len(class_counts)
        if num_classes < 2:
            return False, "Target column should have at least 2 classes"
        min_count = class_counts.min()
        max_count = class_counts.max()
        imbalance_ratio = max_count / min_count
        if imbalance_ratio > 10:
            return True, f"Target column is imbalanced with imbalance ratio of {imbalance_ratio}"
        else:
            return False, "Target column is balanced"

    @staticmethod
    def predict_missing(df):
        df_copy = df.copy()
        numeric_cols = df_copy.select_dtypes(include=['float', 'int']).columns
        numeric_data = df_copy[numeric_cols].to_numpy()
        n_neighbors = 5
        imputer = KNNImputer(n_neighbors=n_neighbors)
        imputed_data = imputer.fit_transform(numeric_data)
        imputed_df = pd.DataFrame(imputed_data, columns=numeric_cols)
        df_copy[numeric_cols] = imputed_df
        return df_copy

    @staticmethod
    def remove_outliers(df, column):
        desc_col = df[column].describe()
        min_value = desc_col['min']
        max_value = desc_col['max']
        q1 = desc_col['25%']
        q3 = desc_col['75%']
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        df_cleaned = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        return df_cleaned

    @staticmethod
    def missing_outliers(df, col_name):
        desc_col = df[col_name].describe()
        min_val = desc_col['min']
        max_val = desc_col['max']
        q1 = desc_col['25%']
        q3 = desc_col['75%']
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        df.loc[(df[col_name] < lower_bound) | (df[col_name] > upper_bound), col_name] = np.nan
        return df

    @staticmethod
    def remove_balance(df, target_column):
        """
        This function balances the target column of a pandas DataFrame by downsampling the majority class.
        """
        class_counts = df[target_column].value_counts()
        min_count = class_counts.min()
        df_balanced = pd.concat([
            resample(df[df[target_column] == i], replace=False, n_samples=min_count, random_state=42)
            for i in class_counts.index
            ])
        return df_balanced

    @staticmethod
    def add_balance(df, target_col):
        counts = df[target_col].value_counts()
        minority_class = counts.idxmin()
        minority_count = counts[minority_class]
        minority_indices = df[df[target_col] == minority_class].index
        oversample_indices = np.random.choice(minority_indices, size=len(df)-minority_count, replace=True)
        oversampled_df = pd.concat([df, df.loc[oversample_indices]])
        return oversampled_df