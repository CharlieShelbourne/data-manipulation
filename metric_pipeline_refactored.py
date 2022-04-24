import pandas as pd

from clean import clean

df = pd.read_csv("./unicorn_companies.csv")
df = clean(df)
df = df.sort_values(by="founded_year")

metric_config = {
    "country": [
        {
            "name": "total_unicorns",
            "grouping": ["country"],
            "column": "company", 
            "operation": "count"
        },
        {
            "name": "average_valuation",
            "grouping": ["country"],
            "column": "valuation", 
            "operation": "mean"
        },
        {
            "name": "max_valuation",
            "grouping": ["country"],
            "column": "valuation", 
            "operation": "max"
        }
    ],
    "country_time_series": [
        {
            "name": "total_unicorns",
            "grouping": ["country", "founded_year"],
            "column": "company", 
            "operation": "count"
        },
        {
            "name": "total_valuation",
            "grouping": ["country", "founded_year"],
            "column": "valuation", 
            "operation": "sum"
        }
    ],
    "investor": [
        {
            "name": "total_companies",
            "grouping": ["select_investors_single"],
            "column": "company", 
            "operation": "count"
        },
        {
            "name": "total_industries",
            "grouping": ["select_investors_single"],
            "column": "industry", 
            "operation": "count"
        },
        {
            "name": "total_company_valuations",
            "grouping": ["select_investors_single"],
            "column": "valuation", 
            "operation": "sum"
        }
    ]

}

def generate_metrics(df: pd.DataFrame, metrics_cofigs: list, expanding: bool=False) -> pd.DataFrame:

    # construct dataframe with category columns from grouping 
    # uses first operation to generate the resulting new index and uses index as a base frame to add metrics to
    grouped_obj = df.groupby(metrics_cofigs[0]["grouping"])
    metrics_df = getattr(grouped_obj, metrics_cofigs[0]["operation"])()[[]].reset_index()

    # loop through each operation in table list and add to metrics dataframe
    for params in metrics_cofigs:

        if expanding:
            grouped_obj = df.groupby(params["grouping"]).expanding()
        else:
            grouped_obj = df.groupby(params["grouping"])

        operation = params["operation"]
        column = params["column"]

        metrics_df[params["name"]] = getattr(grouped_obj, operation)()[column].reset_index(drop=True)

    return metrics_df


# COUNTRY STATS
country_metrics = generate_metrics(df, metric_config["country"])
print(country_metrics)

# TIME SERIES 
time_series_metrics = generate_metrics(df, metric_config["country_time_series"])
time_series_cusum = generate_metrics(df, metric_config["country_time_series"], expanding=True)
print(time_series_metrics)
print(time_series_cusum)

# INVESTOR STATS
# split the investors in to list
df["select_investors"] = df["select_investors"].str.split(',')

# change investor lists to columns
investors = df["select_investors"].explode()

# inner merge to transform dataframe rows of unique investors per company
df = pd.merge(investors, df, left_index=True, right_index=True, suffixes=("_single", "_grouped"))

investor_metrics = generate_metrics(df, metric_config["investor"])
print(investor_metrics)
