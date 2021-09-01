import pandas as pd

def preprocess_data(df:pd.DataFrame): 
    df = df.copy()   
    for col in df.columns:
        for line in df.index:
            if df[col].dtype == str:
                df[col].loc[line] = df[col].loc[line].replace('\n', '')
    return df

