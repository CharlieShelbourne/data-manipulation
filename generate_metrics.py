import pandas as pd

from metrics import Metrics

def generate_metrics(df: pd.DataFrame, metrics: Metrics, metrics_cofigs: list) -> pd.DataFrame:

    # construct dataframe with columns for unique groupings
    # uses the grouping in our config to generate a dataframe with index derived from the grouping
    # throws away result and keeps grouping columns only (count is an arbitary method)
    metrics_df = getattr(df.groupby(metrics_cofigs[0]["grouping"]), "count")()[[]].reset_index()

    # loop through each operation in table list and add to metrics dataframe
    for params in metrics_cofigs:
        # outputs an object of method apply() from groupby() 
        grouped_apply = getattr(df.groupby(params["grouping"])[params["column"]], "apply")
        
        # object of Metrics() method used to trandform data
        funct = getattr(metrics, params["operation"])

        # call the grouped apply object, passing it the metrics method object
        # applies metrics method to the grouped data
        metrics_df[params["name"]] = grouped_apply(funct).reset_index(drop=True)

    return metrics_df


def generate_cumsum_metrics(df: pd.DataFrame, metrics: Metrics, metrics_cofigs: list) -> pd.DataFrame:

    for params in metrics_cofigs:
        grouped_apply = getattr(df.groupby(params["grouping"]).expanding()[params["column"]], "apply")
        
        funct = getattr(metrics, params["operation"])

        df[params["name"]] = grouped_apply(funct).reset_index(drop=True)

    return df