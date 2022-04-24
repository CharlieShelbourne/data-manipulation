import pandas as pd

from clean import clean

df = pd.read_csv("./unicorn_companies.csv")
df = clean(df)
df = df.sort_values(by="founded_year")

# COUNTRY STATS

# number of startups by country
country_stats = df.groupby(["country"])["company"].count().reset_index()

# average valuation by country
country_stats["mean_valuations_billion_usd"] = df.groupby(["country"])["valuation"].mean().reset_index(drop=True)

# max valuation by country
country_stats["max_valuations_billion_usd"] = df.groupby(["country"])["valuation"].max().reset_index(drop=True)

print(country_stats)

# TIME SERIES STATS

# number of unicorns over time
time_series = df.groupby(["country", "founded_year"])["company"].count().reset_index()
# valuations over time by country
time_series["valuation_billion_usd"] = df.groupby(["country", "founded_year"])["valuation"].sum().reset_index(drop=True)

# cumulative count of unicorns over time
time_series["company_cumsum"] = time_series.groupby(["country"])["company"].expanding().sum().reset_index(drop=True)
# cumulative valuation of unicorns over time
time_series["valuation_cumsum"] = time_series.groupby(["country"])["valuation_billion_usd"].expanding().sum().reset_index(drop=True)

# INVESTOR STATS

# split the investors in to list
df["select_investors"] = df["select_investors"].str.split(',')

# change investor lists to columns
investors = df["select_investors"].explode()

# inner merge to transform dataframe rows of unique investors per company 
df = pd.merge(investors, df, left_index=True, right_index=True, suffixes=(" single", " list"))

# count of companiess in investors portfolio
investor_df = df.groupby(["select_investors single"])["company"].count().reset_index()

# count of industries in investors portfolio
investor_df["industry_count"] = df.groupby(["select_investors single"])["Industry"].count().reset_index(drop=True)

# valiation of companies in investors portfolio
investor_df["total_valuation"] = df.groupby(["select_investors single"])["valuation"].sum().reset_index(drop=True)

print(investor_df)









