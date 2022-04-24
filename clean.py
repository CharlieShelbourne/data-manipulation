import numpy as np
import pandas as pd

def clean(df):
    df["valuation"] = df["valuation"].replace('[\$,]', '', regex=True).astype(float)
    df["founded_year"] = df["founded_year"].replace('None', np.nan)
    df["founded_year"] = pd.to_datetime(df["founded_year"].astype(str))