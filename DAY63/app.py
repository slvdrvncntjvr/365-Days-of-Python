

import argparse
import concurrent.futures
import csv
import functools
import io
import json
import logging
import multiprocessing
import os
import random
import re
import statistics
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from functools import lru_cache, partial, wraps
from pathlib import Path
from typing import (Any, Callable, Dict, Generator, Iterable, List, 
                   Optional, Set, Tuple, TypeVar, Union, cast)

# Third-party imports - these would normally be installed with pip
try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import requests
    import seaborn as sns
    from scipy import stats
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from tqdm import tqdm
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Please install required packages using: pip install pandas numpy matplotlib seaborn scikit-learn requests tqdm")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("DataPipeline")

# Type variables for generic functions
T = TypeVar('T')
U = TypeVar('U')


# -------------------------------------------------------------------------
# Configuration and Constants
# -------------------------------------------------------------------------

class DataSource(Enum):
    """Enumeration of possible data sources."""
    CSV = auto()
    JSON = auto()
    API = auto()
    DATABASE = auto()
    SYNTHETIC = auto()


@dataclass
class PipelineConfig:
    """Configuration for the data pipeline."""
    input_path: str = ""
    output_path: str = "output"
    data_source: DataSource = DataSource.SYNTHETIC
    num_processes: int = max(1, multiprocessing.cpu_count() - 1)
    sample_size: int = 10000
    random_seed: int = 42
    log_level: int = logging.INFO
    visualize: bool = True
    batch_size: int = 1000
    cache_results: bool = True
    api_url: str = ""
    api_key: str = ""
    db_connection_string: str = ""
    features: List[str] = field(default_factory=list)
    target: str = ""
    test_size: float = 0.2
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.num_processes <= 0:
            logger.warning("Invalid num_processes, setting to 1")
            self.num_processes = 1
        
        if self.sample_size <= 0:
            logger.warning("Invalid sample_size, setting to 1000")
            self.sample_size = 1000
        
        # Create output directory if it doesn't exist
        if self.output_path:
            os.makedirs(self.output_path, exist_ok=True)


# -------------------------------------------------------------------------
# Utility Functions and Decorators
# -------------------------------------------------------------------------

def timer(func: Callable) -> Callable:
    """Decorator to measure the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """Decorator to retry a function on failure."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"Function {func.__name__} failed after {max_attempts} attempts: {e}")
                        raise
                    logger.warning(f"Attempt {attempts} failed, retrying in {delay} seconds: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator


@contextmanager
def performance_monitor(operation_name: str) -> Generator[None, None, None]:
    """Context manager to monitor performance of a code block."""
    start_memory = 0
    try:
        import psutil
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
    except ImportError:
        logger.warning("psutil not installed, memory monitoring disabled")
    
    start_time = time.time()
    yield
    end_time = time.time()
    
    logger.info(f"Operation '{operation_name}' completed in {end_time - start_time:.4f} seconds")
    
    try:
        if start_memory > 0:
            end_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_used = end_memory - start_memory
            logger.info(f"Memory usage for '{operation_name}': {memory_used:.2f} MB")
    except NameError:
        pass


def validate_data(df: pd.DataFrame, rules: Dict[str, Callable[[pd.Series], bool]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate dataframe against a set of rules and return valid and invalid data.
    
    Args:
        df: Input dataframe to validate
        rules: Dictionary mapping column names to validation functions
        
    Returns:
        Tuple of (valid_data, invalid_data)
    """
    valid_mask = pd.Series(True, index=df.index)
    
    for column, validation_func in rules.items():
        if column in df.columns:
            column_valid = validation_func(df[column])
            valid_mask &= column_valid
        else:
            logger.warning(f"Column {column} not found in dataframe")
    
    valid_data = df[valid_mask]
    invalid_data = df[~valid_mask]
    
    logger.info(f"Data validation: {len(valid_data)} valid rows, {len(invalid_data)} invalid rows")
    return valid_data, invalid_data


def parallelize_dataframe(df: pd.DataFrame, func: Callable[[pd.DataFrame], pd.DataFrame], 
                         n_cores: int = 4, batch_size: Optional[int] = None) -> pd.DataFrame:
    """
    Apply a function to a dataframe in parallel using multiple cores.
    
    Args:
        df: Input dataframe
        func: Function to apply to each partition
        n_cores: Number of cores to use
        batch_size: Size of each batch (if None, will be calculated based on df size and n_cores)
        
    Returns:
        Processed dataframe
    """
    if len(df) < n_cores * 10:  # If data is too small, don't parallelize
        return func(df)
    
    if batch_size is None:
        batch_size = max(1, len(df) // n_cores)
    
    df_split = [df[i:i + batch_size] for i in range(0, len(df), batch_size)]
    
    with ProcessPoolExecutor(max_workers=n_cores) as executor:
        df_list = list(executor.map(func, df_split))
    
    return pd.concat(df_list)


@lru_cache(maxsize=128)
def expensive_calculation(x: float, y: float) -> float:
    """
    Example of an expensive calculation that benefits from caching.
    
    Args:
        x: First parameter
        y: Second parameter
        
    Returns:
        Result of calculation
    """
    time.sleep(0.01)  # Simulate expensive operation
    return np.sqrt(x**2 + y**2)


# -------------------------------------------------------------------------
# Data Generation and Loading Functions
# -------------------------------------------------------------------------

def generate_synthetic_data(config: PipelineConfig) -> pd.DataFrame:
    """
    Generate synthetic data for testing and development.
    
    Args:
        config: Pipeline configuration
        
    Returns:
        DataFrame with synthetic data
    """
    logger.info(f"Generating synthetic dataset with {config.sample_size} samples")
    np.random.seed(config.random_seed)
    
    # Generate synthetic customer data
    data = {
        'customer_id': range(1, config.sample_size + 1),
        'age': np.random.normal(40, 15, config.sample_size).astype(int),
        'income': np.random.lognormal(10, 1, config.sample_size).astype(int),
        'spending_score': np.random.uniform(1, 100, config.sample_size).astype(int),
        'loyalty_years': np.random.exponential(5, config.sample_size).astype(int),
        'products_purchased': np.random.poisson(5, config.sample_size),
        'satisfaction': np.random.choice([1, 2, 3, 4, 5], config.sample_size, p=[0.1, 0.2, 0.4, 0.2, 0.1]),
        'last_purchase_days': np.random.exponential(30, config.sample_size).astype(int),
        'website_visits': np.random.poisson(8, config.sample_size),
        'returns': np.random.binomial(1, 0.2, config.sample_size),
    }
    
    # Add some categorical features
    data['gender'] = np.random.choice(['M', 'F', 'Other'], config.sample_size, p=[0.48, 0.48, 0.04])
    data['location'] = np.random.choice(['Urban', 'Suburban', 'Rural'], config.sample_size, p=[0.6, 0.3, 0.1])
    data['membership'] = np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], config.sample_size, p=[0.4, 0.3, 0.2, 0.1])
    
    # Add some missing values
    for col in ['age', 'income', 'loyalty_years', 'satisfaction']:
        mask = np.random.random(config.sample_size) < 0.05
        data[col] = np.where(mask, np.nan, data[col])
    
    # Add some outliers
    for col in ['age', 'income', 'spending_score']:
        outlier_mask = np.random.random(config.sample_size) < 0.01
        if col == 'income':
            data[col] = np.where(outlier_mask, np.random.uniform(500000, 1000000, config.sample_size), data[col])
        elif col == 'age':
            data[col] = np.where(outlier_mask, np.random.uniform(90, 120, config.sample_size), data[col])
        else:
            data[col] = np.where(outlier_mask, np.random.uniform(150, 200, config.sample_size), data[col])
    
    # Add a timestamp column
    start_date = datetime.now() - timedelta(days=365)
    data['registration_date'] = [
        start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(config.sample_size)
    ]
    
    # Create a target variable (high_value_customer) based on income and spending
    income_z = stats.zscore(np.nan_to_num(data['income']))
    spending_z = stats.zscore(data['spending_score'])
    loyalty_z = stats.zscore(np.nan_to_num(data['loyalty_years']))
    
    data['high_value_customer'] = (
        (income_z + spending_z + loyalty_z > 1) | 
        (data['membership'] == 'Platinum')
    ).astype(int)
    
    df = pd.DataFrame(data)
    
    # Add some derived features
    df['age_group'] = pd.cut(
        df['age'], 
        bins=[0, 18, 25, 35, 50, 65, 120], 
        labels=['Under 18', '18-24', '25-34', '35-49', '50-64', '65+']
    )
    
    df['income_bracket'] = pd.qcut(
        df['income'].fillna(df['income'].median()), 
        q=5, 
        labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
    )
    
    # Create a recency-frequency-monetary (RFM) score
    df['recency_score'] = pd.qcut(
        df['last_purchase_days'], 
        q=5, 
        labels=[5, 4, 3, 2, 1]  # Lower days = higher score
    ).astype(int)
    
    df['frequency_score'] = pd.qcut(
        df['products_purchased'].clip(upper=df['products_purchased'].quantile(0.99)), 
        q=5, 
        labels=[1, 2, 3, 4, 5]
    ).astype(int)
    
    df['monetary_score'] = pd.qcut(
        df['spending_score'].clip(upper=df['spending_score'].quantile(0.99)), 
        q=5, 
        labels=[1, 2, 3, 4, 5]
    ).astype(int)
    
    df['rfm_score'] = df['recency_score'] + df['frequency_score'] + df['monetary_score']
    
    return df


@retry(max_attempts=3)
def load_data_from_source(config: PipelineConfig) -> pd.DataFrame:
    """
    Load data from the configured source.
    
    Args:
        config: Pipeline configuration
        
    Returns:
        DataFrame with loaded data
    """
    with performance_monitor("data_loading"):
        if config.data_source == DataSource.SYNTHETIC:
            return generate_synthetic_data(config)
        
        elif config.data_source == DataSource.CSV:
            logger.info(f"Loading data from CSV: {config.input_path}")
            return pd.read_csv(config.input_path)
        
        elif config.data_source == DataSource.JSON:
            logger.info(f"Loading data from JSON: {config.input_path}")
            return pd.read_json(config.input_path)
        
        elif config.data_source == DataSource.API:
            logger.info(f"Fetching data from API: {config.api_url}")
            headers = {'Authorization': f'Bearer {config.api_key}'} if config.api_key else {}
            response = requests.get(config.api_url, headers=headers)
            response.raise_for_status()
            return pd.DataFrame(response.json())
        
        elif config.data_source == DataSource.DATABASE:
            logger.info(f"Loading data from database")
            # This would normally use SQLAlchemy or another DB library
            # For this example, we'll just return synthetic data
            return generate_synthetic_data(config)
        
        else:
            raise ValueError(f"Unsupported data source: {config.data_source}")


# -------------------------------------------------------------------------
# Data Preprocessing Functions
# -------------------------------------------------------------------------

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names: lowercase, replace spaces with underscores.
    
    Args:
        df: Input dataframe
        
    Returns:
        DataFrame with cleaned column names
    """
    df.columns = [re.sub(r'[^\w\s]', '', col).lower().replace(' ', '_') for col in df.columns]
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from dataframe.
    
    Args:
        df: Input dataframe
        
    Returns:
        DataFrame with duplicates removed
    """
    initial_rows = len(df)
    df = df.drop_duplicates()
    removed = initial_rows - len(df)
    if removed > 0:
        logger.info(f"Removed {removed} duplicate rows")
    return df


def handle_missing_values(df: pd.DataFrame, strategy: str = 'median') -> pd.DataFrame:
    """
    Handle missing values in the dataframe.
    
    Args:
        df: Input dataframe
        strategy: Strategy for handling missing values ('median', 'mean', 'mode', 'drop', 'zero')
        
    Returns:
        DataFrame with missing values handled
    """
    # Count missing values before handling
    missing_before = df.isna().sum().sum()
    
    if strategy == 'drop':
        df = df.dropna()
    else:
        # Handle numerical and categorical columns differently
        numerical_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        for col in numerical_cols:
            if strategy == 'median':
                df[col] = df[col].fillna(df[col].median())
            elif strategy == 'mean':
                df[col] = df[col].fillna(df[col].mean())
            elif strategy == 'zero':
                df[col] = df[col].fillna(0)
        
        for col in categorical_cols:
            if strategy == 'mode':
                df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
            else:
                df[col] = df[col].fillna("Unknown")
    
    # Count missing values after handling
    missing_after = df.isna().sum().sum()
    logger.info(f"Handled {missing_before - missing_after} missing values using '{strategy}' strategy")
    
    return df


def detect_and_handle_outliers(df: pd.DataFrame, method: str = 'iqr', 
                              columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Detect and handle outliers in numerical columns.
    
    Args:
        df: Input dataframe
        method: Method for outlier detection ('iqr', 'zscore', 'none')
        columns: List of columns to check for outliers (if None, all numerical columns)
        
    Returns:
        DataFrame with outliers handled
    """
    if method == 'none':
        return df
    
    result_df = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=['number']).columns.tolist()
    
    outlier_counts = {}
    
    for col in columns:
        if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
            continue
        
        # Skip columns with too many missing values
        if df[col].isna().mean() > 0.5:
            continue
        
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index
        elif method == 'zscore':
            z_scores = stats.zscore(df[col].fillna(df[col].median()))
            outliers = df[abs(z_scores) > 3].index
        else:
            logger.warning(f"Unknown outlier detection method: {method}")
            return df
        
        outlier_counts[col] = len(outliers)
        
        # Cap outliers at the boundaries instead of removing them
        result_df.loc[result_df[col] < lower_bound, col] = lower_bound
        result_df.loc[result_df[col] > upper_bound, col] = upper_bound
    
    total_outliers = sum(outlier_counts.values())
    if total_outliers > 0:
        logger.info(f"Detected and handled {total_outliers} outliers using {method} method")
        for col, count in outlier_counts.items():
            if count > 0:
                logger.debug(f"- {col}: {count} outliers")
    
    return result_df


def encode_categorical_variables(df: pd.DataFrame, encoding_method: str = 'onehot', 
                               max_categories: int = 10) -> pd.DataFrame:
    """
    Encode categorical variables using the specified method.
    
    Args:
        df: Input dataframe
        encoding_method: Method for encoding ('onehot', 'label', 'binary', 'none')
        max_categories: Maximum number of categories to one-hot encode
        
    Returns:
        DataFrame with encoded categorical variables
    """
    if encoding_method == 'none':
        return df
    
    result_df = df.copy()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    for col in categorical_cols:
        unique_values = df[col].nunique()
        
        if encoding_method == 'onehot' and unique_values <= max_categories:
            # One-hot encoding
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=False)
            result_df = pd.concat([result_df, dummies], axis=1)
            result_df = result_df.drop(col, axis=1)
            
        elif encoding_method == 'label' or (encoding_method == 'onehot' and unique_values > max_categories):
            # Label encoding
            from sklearn.preprocessing import LabelEncoder
            le = LabelEncoder()
            result_df[f"{col}_encoded"] = le.fit_transform(df[col].fillna('Unknown'))
            
        elif encoding_method == 'binary' and unique_values == 2:
            # Binary encoding
            unique_cats = df[col].dropna().unique()
            if len(unique_cats) == 2:
                result_df[f"{col}_binary"] = df[col].map({unique_cats[0]: 0, unique_cats[1]: 1})
    
    logger.info(f"Encoded {len(categorical_cols)} categorical variables using {encoding_method} encoding")
    return result_df


def normalize_features(df: pd.DataFrame, method: str = 'standard', 
                     columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Normalize numerical features using the specified method.
    
    Args:
        df: Input dataframe
        method: Method for normalization ('standard', 'minmax', 'robust', 'none')
        columns: List of columns to normalize (if None, all numerical columns)
        
    Returns:
        DataFrame with normalized features
    """
    if method == 'none':
        return df
    
    if columns is None:
        columns = df.select_dtypes(include=['number']).columns.tolist()
    
    # Make a copy to avoid modifying the original
    result_df = df.copy()
    
    if method == 'standard':
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
    elif method == 'minmax':
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
    elif method == 'robust':
        from sklearn.preprocessing import RobustScaler
        scaler = RobustScaler()
    else:
        logger.warning(f"Unknown normalization method: {method}")
        return df
    
    # Fit and transform the selected columns
    if columns:
        result_df[columns] = scaler.fit_transform(df[columns].fillna(0))
        logger.info(f"Normalized {len(columns)} features using {method} normalization")
    
    return result_df


def create_date_features(df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
    """
    Extract useful features from date columns.
    
    Args:
        df: Input dataframe
        date_columns: List of date columns to process
        
    Returns:
        DataFrame with additional date-based features
    """
    result_df = df.copy()
    
    for col in date_columns:
        if col in df.columns:
            # Convert to datetime if not already
            if not pd.api.types.is_datetime64_dtype(df[col]):
                try:
                    result_df[col] = pd.to_datetime(df[col])
                except Exception as e:
                    logger.warning(f"Could not convert {col} to datetime: {e}")
                    continue
            
            # Extract date components
            result_df[f"{col}_year"] = result_df[col].dt.year
            result_df[f"{col}_month"] = result_df[col].dt.month
            result_df[f"{col}_day"] = result_df[col].dt.day
            result_df[f"{col}_dayofweek"] = result_df[col].dt.dayofweek
            result_df[f"{col}_quarter"] = result_df[col].dt.quarter
            
            # Calculate days since a reference date
            reference_date = datetime.now()
            result_df[f"days_since_{col}"] = (reference_date - result_df[col]).dt.days
            
            logger.info(f"Created date features from column: {col}")
    
    return result_df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create new features from existing ones.
    
    Args:
        df: Input dataframe
        
    Returns:
        DataFrame with engineered features
    """
    result_df = df.copy()
    
    # Example feature engineering for customer data
    if all(col in df.columns for col in ['income', 'age']):
        result_df['income_per_age'] = df['income'] / df['age'].clip(lower=1)
    
    if all(col in df.columns for col in ['products_purchased', 'website_visits']):
        result_df['conversion_rate'] = df['products_purchased'] / df['website_visits'].clip(lower=1)
    
    if all(col in df.columns for col in ['spending_score', 'income']):
        result_df['spending_to_income_ratio'] = df['spending_score'] / df['income'].clip(lower=1) * 1000
    
    if 'age' in df.columns:
        # Binning age into groups
        result_df['age_group_numeric'] = pd.cut(
            df['age'], 
            bins=[0, 18, 30, 45, 60, 120], 
            labels=[1, 2, 3, 4, 5]
        ).astype(float)
    
    if all(col in df.columns for col in ['satisfaction', 'returns']):
        # Customer satisfaction adjusted by returns
        result_df['adjusted_satisfaction'] = df['satisfaction'] * (1 - 0.5 * df['returns'])
    
    # Count the number of non-null values per row as a measure of data completeness
    result_df['data_completeness'] = df.notnull().sum(axis=1) / len(df.columns)
    
    logger.info(f"Added {len(result_df.columns) - len(df.columns)} engineered features")
    return result_df


@timer
def preprocess_data(df: pd.DataFrame, config: PipelineConfig) -> pd.DataFrame:
    """
    Apply the full preprocessing pipeline to the data.
    
    Args:
        df: Input dataframe
        config: Pipeline configuration
        
    Returns:
        Preprocessed dataframe
    """
    with performance_monitor("data_preprocessing"):
        logger.info(f"Starting data preprocessing on {len(df)} rows and {len(df.columns)} columns")
        
        # Define preprocessing steps
        preprocessing_steps = [
            ("Cleaning column names", clean_column_names),
            ("Removing duplicates", remove_duplicates),
            ("Handling missing values", lambda x: handle_missing_values(x, strategy='median')),
            ("Handling outliers", lambda x: detect_and_handle_outliers(x, method='iqr')),
            ("Creating date features", lambda x: create_date_features(x, ['registration_date'] if 'registration_date' in df.columns else [])),
            ("Feature engineering", feature_engineering),
            ("Encoding categorical variables", lambda x: encode_categorical_variables(x, encoding_method='onehot')),
            ("Normalizing features", lambda x: normalize_features(x, method='standard'))
        ]
        
        # Apply each preprocessing step
        for step_name, step_func in preprocessing_steps:
            logger.info(f"Applying preprocessing step: {step_name}")
            df = step_func(df)
        
        logger.info(f"Completed preprocessing: {len(df)} rows and {len(df.columns)} columns")
        return df


# -------------------------------------------------------------------------
# Analysis and Modeling Functions
# -------------------------------------------------------------------------

def compute_summary_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute summary statistics for the dataset.
    
    Args:
        df: Input dataframe
        
    Returns:
        Dictionary of summary statistics
    """
    summary = {}
    
    # Basic counts
    summary['row_count'] = len(df)
    summary['column_count'] = len(df.columns)
    
    # Data types
    type_counts = df.dtypes.value_counts().to_dict()
    summary['data_types'] = {str(k): v for k, v in type_counts.items()}
    
    # Missing values
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    summary['missing_values'] = {
        'total_missing': missing.sum(),
        'percent_missing': missing_percent.sum() / len(df.columns),
        'columns_with_missing': missing[missing > 0].to_dict()
    }
    
    # Numerical statistics
    numerical_cols = df.select_dtypes(include=['number']).columns
    if not numerical_cols.empty:
        stats_df = df[numerical_cols].describe().transpose()
        summary['numerical_stats'] = stats_df.to_dict()
        
        # Compute additional statistics for numerical columns
        skew = df[numerical_cols].skew().to_dict()
        kurtosis = df[numerical_cols].kurtosis().to_dict()
        summary['skew'] = skew
        summary['kurtosis'] = kurtosis
    
    # Categorical statistics
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if not categorical_cols.empty:
        cat_stats = {}
        for col in categorical_cols:
            cat_stats[col] = df[col].value_counts().to_dict()