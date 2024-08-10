import pandas as pd




def preprocess(df_sum,region_df):
    # merge with region_df
    df_sum = df_sum.merge(region_df, on='NOC', how='left')

    # dropping duplicates
    df_sum.drop_duplicates(inplace=True)

    # one hot encoding medals
    df_sum = pd.concat([df_sum, pd.get_dummies(df_sum['Medal'])], axis=1)
    return df_sum

