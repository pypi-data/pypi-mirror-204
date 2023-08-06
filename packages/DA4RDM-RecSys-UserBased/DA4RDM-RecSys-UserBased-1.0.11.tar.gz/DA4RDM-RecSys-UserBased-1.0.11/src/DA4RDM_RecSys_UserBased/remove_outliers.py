def remove_outliers(df, method):

    if method.lower() == "zscore":
        upper_limit = df['StandardRating'].mean() + 3 * df['StandardRating'].std()
        lower_limit = df['StandardRating'].mean() - 3 * df['StandardRating'].std()
        u_limit = upper_limit["StandardRating"]
        l_limit = lower_limit["StandardRating"]
        # print("Z-Score upper limit", upper_limit["StandardRating"])
        # print("Z-Score lower limit", lower_limit["StandardRating"])
        new_df = df.iloc[(df['StandardRating'].values < u_limit) & (df['StandardRating'].values > l_limit)]
        return new_df
    elif method.lower() == "iqr":
        percentile25 = df['StandardRating'].quantile(0.25)
        percentile75 = df['StandardRating'].quantile(0.75)
        iqr = percentile75 - percentile25
        upper_limit = percentile75 + 1.5 * iqr
        lower_limit = percentile25 - 1.5 * iqr
        u_limit = upper_limit["StandardRating"]
        l_limit = lower_limit["StandardRating"]
        # print("IQR Upper Limit", u_limit)
        # print("IQR Lower Limit", l_limit)
        new_df = df.iloc[(df['StandardRating'].values < u_limit) & (df['StandardRating'].values > l_limit)]
        return new_df
    elif method.lower() == "percentile":
        percentile99 = df['StandardRating'].quantile(0.99)
        percentile01 = df['StandardRating'].quantile(0.01)
        u_limit = percentile99["StandardRating"]
        l_limit = percentile01["StandardRating"]
        # print("Percentile upper_limit", u_limit)
        # print("Percentile lower_limit", l_limit)
        new_df = df.iloc[(df['StandardRating'].values < u_limit) & (df['StandardRating'].values > l_limit)]
        return new_df
