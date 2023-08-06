"""Function to create operation matrix for each unique user resource pair and then create the recommendation matrix
to get resource recommendation for the reference user"""
import numpy as np
import pandas as pd
from DA4RDM_RecSys_UserBased.remove_outliers import remove_outliers


def standardize(df):
    from sklearn.preprocessing import StandardScaler
    df[['StandardRating']] = StandardScaler().fit_transform(df[["Rating"]])
    return df


def create_recommendation_matrix(matrix_dat):
    user_list = matrix_dat["UserId"].squeeze().unique()
    res_list = matrix_dat["ResourceId"].squeeze().unique()
    column_list = []
    for val in user_list:
        column_list.append(val)
    rlist = []
    for valu in res_list:
        rlist.append(valu)
    index = rlist
    recommendation_matrix = pd.DataFrame(index=index, columns=column_list)
    for index, row in matrix_dat.iterrows():
        user = row['UserId']
        res = row['ResourceId']
        rating = row['StandardRating']
        recommendation_matrix.at[res, user] = rating
    recommendation_matrix.replace(np.nan, 0, inplace=True)
    # ax = sns.heatmap(recommendation_matrix, cmap='gray', linewidths=0.5, annot=True)
    # plt.show()
    return recommendation_matrix


def create_operations_matrix(feature_operation_dict, matrix, outlier_method):
    for feature_name, operation_name in feature_operation_dict.items():
        labels = feature_name.split("#")
        matrix.loc[-1, ["UserId"]] = labels[0]
        matrix.loc[-1, ["ResourceId"]] = labels[1]
        matrix.loc[-1, ["Duration"]] = labels[2]
        matrix.loc[-1, ["ProjectId"]] = labels[3]
        matrix.loc[-1, ["Roles"]] = labels[4]
        matrix = matrix.sort_index()
        for ind, value in operation_name.items():
            if ind == "Upload File":
                matrix.loc[-1, [ind]] = value * 0.5
            if ind == "Upload MD":
                matrix.loc[-1, [ind]] = value * 0.5
            if ind == "Update File":
                matrix.loc[-1, [ind]] = value * 0.8
            if ind == "Update MD":
                matrix.loc[-1, [ind]] = value * 0.8
            if ind == "View MD":
                matrix.loc[-1, [ind]] = value * 0.3
            if ind == "Download File":
                matrix.loc[-1, [ind]] = value * 1
            if ind == "Delete File":
                matrix.loc[-1, [ind]] = value * 0.1
        matrix.index = matrix.index + 1
    matrix.replace(np.nan, 0, inplace=True)
    # matrix.to_csv("Data/Matrix_Operations_Ratings.csv")
    matrix['Rating'] = (matrix.iloc[:, 4:10].sum(axis=1)) / 7
    matrix = standardize(matrix)
    matrix = matrix[["UserId", "ResourceId", "ProjectId", "Rating", "StandardRating", "Roles"]]
    # matrix.to_csv("Data/Matrix_Ratings.csv")
    matrix = remove_outliers(matrix, outlier_method)
    matrix_filtered = matrix[["UserId", "ResourceId", "Rating", "StandardRating"]]
    # matrix_filtered.to_csv("Data/Matrix_Ratings_Columns_Filtered.csv")
    recommendation_matrix = create_recommendation_matrix(matrix_filtered)
    # recommendation_matrix.to_csv("Data/Matrix_Interaction_Recommendation.csv")
    return recommendation_matrix
