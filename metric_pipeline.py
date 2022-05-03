import pandas as pd
import numpy as np

df = pd.read_csv("./data/unicorn_companies.csv")
df["valuation"] = df["valuation"].replace('[\$,]', '', regex=True).astype(float)
df["date_joined"] = df["date_joined"].replace('None', np.nan)
df["date_joined"] = pd.to_datetime(df["date_joined"].astype(str))
df = df.sort_values(by="date_joined")

# COUNTRY STATS

# number of startups by country
country_stats = df.groupby(by=["country"])["company"].count().reset_index()

# average valuation by country
country_stats["mean_valuations_billion_usd"] = df.groupby(by=["country"])["valuation"].mean().reset_index(drop=True)

# max valuation by country
country_stats["max_valuations_billion_usd"] = df.groupby(by=["country"])["valuation"].max().reset_index(drop=True)

print(country_stats)

# TIME SERIES STATS

# number of unicorns over time
time_series = df.groupby(by=["country", "date_joined"])["company"].count().reset_index()
# valuations over time by country
time_series["valuation_billion_usd"] = df.groupby(by=["country", "date_joined"])["valuation"].sum().reset_index(drop=True)

# cumulative count of unicorns over time
time_series["company_cumsum"] = time_series.groupby(by=["country"])["company"].expanding().sum().reset_index(drop=True)
# cumulative valuation of unicorns over time
time_series["valuation_cumsum"] = time_series.groupby(by=["country"])["valuation_billion_usd"].expanding().sum().reset_index(drop=True)

# INVESTOR STATS

# split the investors in to list
df["select_investors"] = df["select_investors"].str.split(',')

# change investor lists to columns
investors = df["select_investors"].explode()

# inner merge to transform dataframe rows of unique investors per company 
df = pd.merge(investors, df, left_index=True, right_index=True, suffixes=("_single", "_list"))

# count of companiess in investors portfolio
investor_df = df.groupby(["select_investors single"])["company"].count().reset_index()

# count of industries in investors portfolio
investor_df["industry_count"] = df.groupby(["select_investors_single"])["Industry"].count().reset_index(drop=True)

# valiation of companies in investors portfolio
investor_df["total_valuation"] = df.groupby(["select_investors_single"])["valuation"].sum().reset_index(drop=True)

print(investor_df)









