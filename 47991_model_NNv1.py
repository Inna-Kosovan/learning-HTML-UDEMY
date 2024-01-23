import matplotlib.pyplot as plt
import logging
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import time
from sklearn.preprocessing import MinMaxScaler
import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score, TimeSeriesSplit
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

logging.basicConfig(level=logging.INFO)

def log_execution_time(start_time, message="Execution time"):
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"{message}: {minutes} minutes and {seconds} seconds")

class TimeSeriesForecasting:
    def __init__(self, data, save_directory):
        self.save_directory = save_directory
        self.df = data
        self.models = {}
        self.feature_names = {}
        self.tscv = TimeSeriesSplit(n_splits=5)
        self.train = pd.DataFrame()
        self.val = pd.DataFrame()


    def data_quality_check(self):
        # Check for missing values
        missing_values = self.df.isnull().sum()
        columns_with_missing_values = missing_values[missing_values > 0].index.tolist()  # Initialized the missing values columns list

        # Fill NaN values in each column with its mean
        for column in columns_with_missing_values:
            self.df[column].fillna(self.df[column].mean(), inplace=True)
        print("Missing Values:\n", missing_values)

        # Check for duplicates
        duplicates = self.df.duplicated().sum()
        print("\nNumber of duplicate rows:", duplicates)

        # Drop duplicates if any
        if duplicates > 0:
            self.df.drop_duplicates(inplace=True)
            print("Dropped duplicates.")

        # Check data types after conversion
        data_types_after_conversion = self.df.dtypes
        print("\nData Types after conversion:\n", data_types_after_conversion)

    def generate_future_data(self, timestamps):
        future_data = pd.DataFrame({'EVENT_TIME': timestamps})
        missing_cols = set(self.train.columns) - set(future_data.columns)
        for col in missing_cols:
            future_data[col] = np.nan
        for col in future_data.columns:
            if future_data[col].isnull().any():
                future_data[col].fillna(self.train[col].mean(), inplace=True)
        if 'EVENT_TIME' in future_data.columns:
            future_data['EVENT_TIME'] = pd.to_datetime(future_data['EVENT_TIME'])
            future_data.set_index('EVENT_TIME', inplace=True)
            for time_feature in ['year', 'month', 'day', 'hour', 'minute', 'second']:
                future_data[f'EVENT_TIME_{time_feature}'] = getattr(future_data.index, time_feature)
        return future_data

    def preprocess_data(self):
        print("Preprocessing data...")
        if 'EVENT_TIME' in self.df.columns:
            self.df['EVENT_TIME'] = pd.to_datetime(self.df['EVENT_TIME'], errors='coerce')
            self.df['EVENT_TIME_year'] = self.df['EVENT_TIME'].dt.year
            self.df['EVENT_TIME_month'] = self.df['EVENT_TIME'].dt.month
            self.df['EVENT_TIME_day'] = self.df['EVENT_TIME'].dt.day
            self.df['EVENT_TIME_hour'] = self.df['EVENT_TIME'].dt.hour
            self.df['EVENT_TIME_minute'] = self.df['EVENT_TIME'].dt.minute
            self.df['EVENT_TIME_second'] = self.df['EVENT_TIME'].dt.second
            self.df.drop(columns='EVENT_TIME', inplace=True)  # Drop the 'EVENT_TIME' column

        # Convert any string values to numeric
        for col in self.df.columns:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        # Handle non-numeric columns here (if any)

        print("Data types after preprocessing:")
        print(self.df.dtypes)

    def inverse_scale_data(self, data):
        scaler = MinMaxScaler()
        scaler.fit(self.train)
        return scaler.inverse_transform(data)

    def _split_data(self, target_col):
        train, val = train_test_split(self.df, test_size=0.2, shuffle=False)
        print(f"Training data length: {len(train)}")
        print(f"Validation data length: {len(val)}")
        return train, val

    def train_models(self, target_col, model_types=['GradientBoosting', 'RandomForest', 'XGBoost']):
        start_time = time.time()

        self.data_quality_check()  # Call data_quality_check method first
        self.preprocess_data()  # Then call preprocess_data method

        self.train, self.val = self._split_data(target_col)

        X_train, y_train = self.train.drop(columns=target_col), self.train[target_col]
        X_test, y_test = self.val.drop(columns=target_col), self.val[target_col]

        for model_type in model_types:
            self._hyperparameter_tuning_and_training(target_col, X_train, y_train, X_test, y_test, model_type)

        self.log_execution_time(start_time, "Total training time")

    def _hyperparameter_tuning_and_training(self, target_col, X_train, y_train, X_test, y_test, model_type='GradientBoosting'):
        start_time = time.time()
        model, param_grid = self._get_model_and_param_grid(model_type)
        grid_search = GridSearchCV(model, param_grid, cv=KFold(n_splits=5), n_jobs=-1)
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_
        best_model.fit(X_train, y_train)
        self.models[target_col] = best_model
        self.feature_names[target_col] = list(X_train.columns)
        cv_scores = cross_val_score(best_model, X_test, y_test, cv=KFold(n_splits=5))
        print(f'Cross-validation scores for {target_col}: {cv_scores}')
        print(f'Mean cross-validation score for {target_col}: {np.mean(cv_scores)}')
        importance = best_model.feature_importances_
        importance_dict = dict(zip(X_train.columns, importance))
        sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        print(f"Top 5 important features for {target_col}: {sorted_importance[:5]}")
        self.log_execution_time(start_time, "Hyperparameter tuning and training completed in")

    def _get_model_and_param_grid(self, model_type):
        if model_type == 'GradientBoosting':
            model = GradientBoostingRegressor()
            param_grid = {
                'n_estimators': [50, 100, 150, 200],
                'max_depth': [3, 5, 7, 9],
                'learning_rate': [0.001, 0.01, 0.1, 0.5],
                'subsample': [0.8, 0.9, 1.0],
                'max_features': ['sqrt', 'log2', None]
            }
        elif model_type == 'RandomForest':
            model = RandomForestRegressor()
            param_grid = {
                'n_estimators': [10, 50, 100, 150],
                'max_depth': [3, 5, 7, None],
                'max_features': ['sqrt', 'log2', None]
            }
        elif model_type == 'XGBoost':
            model = XGBRegressor()
            param_grid = {
                'n_estimators': [50, 100, 150, 200],
                'max_depth': [3, 5, 7, 9],
                'learning_rate': [0.001, 0.01, 0.1, 0.5],
                'subsample': [0.8, 0.9, 1.0],
                'colsample_bytree': [0.8, 0.9, 1.0],
                'gamma': [0, 0.1, 0.2, 0.3]
            }
        else:
            raise ValueError("Invalid model_type. Choose 'GradientBoosting', 'RandomForest' or 'XGBoost'")
        return model, param_grid

    def predict(self, target_col, X):
        model = self.models[target_col]
        feature_names = self.feature_names[target_col]
        if 'EVENT_TIME' in X.columns:
            X = X.drop(columns='EVENT_TIME')
        X = X[feature_names]
        predictions = model.predict(X)
        return predictions

    def evaluate_all_models(self, target_col):
        X_test, y_test = self.val.drop(columns=target_col), self.val[target_col]
        for target_col, model in self.models.items():
            y_pred = model.predict(X_test)
            self.evaluate_model(y_test, y_pred, target_col)

    def evaluate_model(self, y_true, y_pred, model_type):
        mse = mean_squared_error(y_true, y_pred)
        print(f"Mean squared error for {model_type}: {mse}")

    def save_model(self, target_col):
        model = self.models[target_col]
        model_file_path = f"{self.save_directory}/{target_col}_model.pkl"
        joblib.dump(model, model_file_path)
        print(f"Saved {target_col} model to {model_file_path}")

    def log_execution_time(self, start_time, message):
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{message}: {elapsed_time} seconds")

    def load_models(self):
        for target_col in self.models.keys():
            self.models[target_col] = joblib.load(f"{self.save_directory}/{target_col}_model.pkl")

    def future_predictions(self, target_col, timestamps):
        future_data = self.generate_future_data(timestamps)
        predictions = self.predict(target_col, future_data)
        future_data['predictions'] = predictions
        return future_data

    def plot_future_predictions(self, target_col, timestamps):
        future_data = self.future_predictions(target_col, timestamps)
        plt.figure(figsize=(10, 5))
        plt.plot(future_data.index, future_data['predictions'])
        plt.xlabel('Timestamp')
        plt.ylabel(target_col)
        plt.title(f'Future Predictions for {target_col}')
        plt.show()

    def print_memory_usage(self):
        total_memory_bytes = self.df.memory_usage(deep=True).sum()
        total_memory_megabytes = total_memory_bytes / 1_048_576
        print(f"DataFrame memory usage: {total_memory_megabytes:.2f} MB")

def main():
    main_start_time = time.time()
    save_directory = "/data/works/codes/neiron4_model_ML/"  # Update this path as needed
    data = pd.read_csv("/data/works/codes/neiron4_model_ML/TRADE_1H/47991_DataProcessor_v3.csv")  # Update this path to your data file
    forecasting = TimeSeriesForecasting(data, save_directory=save_directory)

    target_col = 'PRICE'  # Use the correct target column name

    # Train models (if not already trained)
    forecasting.train_models(target_col)

    # Check if the model and feature names for the target column are available
    if target_col not in forecasting.models:
        print(f"Model for {target_col} is not available.")
    if target_col not in forecasting.feature_names:
        print(f"Feature names for {target_col} are not available.")

    # Get the last timestamp in the dataframe
    last_timestamp = forecasting.df['EVENT_TIME'].max()

    # Generate a range of timestamps starting from the last timestamp, extending 60 values into the future
    timestamps = pd.date_range(start=last_timestamp, periods=61, freq='H')[1:]

    # Make future predictions
    forecasting.future_predictions(target_col, timestamps)
    forecasting.plot_future_predictions(target_col, timestamps)

    end_time = time.time()
    elapsed_time = end_time - main_start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"Execution time: {minutes} minutes and {seconds} seconds")

if __name__ == "__main__":
    main()
