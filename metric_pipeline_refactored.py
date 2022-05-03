import pandas as pd
import json
import numpy as np

from metrics import Metrics
from generate_metrics import *

# load metrics config file
with open("config.json") as file:
    metrics_config = json.load(file)

# metrics class instance
metrics = Metrics()

#  load and clean data
df = pd.read_csv("./data/unicorn_companies.csv")
df["valuation"] = df["valuation"].replace('[\$,]', '', regex=True).astype(float)
df["date_joined"] = df["date_joined"].replace('None', np.nan)
df["date_joined"] = pd.to_datetime(df["date_joined"].astype(str))
df = df.sort_values(by="date_joined")

# COUNTRY STATS
country_metrics = generate_metrics(df, metrics, metrics_config["country"])
country_metrics.to_csv("./data/country_metrics.csv")

# # TIME SERIES 
time_series_metrics = generate_metrics(df, metrics, metrics_config["country_time_series"])
print(time_series_metrics)
time_series_metrics = generate_cumsum_metrics(time_series_metrics, metrics, metrics_config["time_series_cumsum"])
print(time_series_metrics)
time_series_metrics.to_csv("./data/time_series_metrics.csv")

# INVESTOR STATS
# split the investors in to list
df["select_investors"] = df["select_investors"].str.split(',')

# change investor lists to columns
investors = df["select_investors"].explode()

# inner merge to transform dataframe rows of unique investors per company
df = pd.merge(investors, df, left_index=True, right_index=True, suffixes=("_single", "_grouped"))

investor_metrics = generate_metrics(df, metrics, metrics_config["investor"])
investor_metrics.to_csv("./data/investor_metrics.csv")
