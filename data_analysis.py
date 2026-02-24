# data_analysis.py
import pandas as pd

def load_and_filter(csv_file):
    df = pd.read_csv(csv_file)
    df = df[df['age'] > 18]  # no check if 'age' column exists
    return df

def calculate_average(df):
    avg = df['salary'].mean()  # fails if 'salary' column missing or NaN-heavy
    return round(avg)

