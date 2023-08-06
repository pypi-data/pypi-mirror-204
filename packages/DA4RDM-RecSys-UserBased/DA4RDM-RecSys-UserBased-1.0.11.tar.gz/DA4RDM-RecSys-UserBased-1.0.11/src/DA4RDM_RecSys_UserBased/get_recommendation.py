from DA4RDM_RecSys_UserBased.create_matrix import create_operations_matrix
from DA4RDM_RecSys_UserBased.evaluate_weight import calculate_weight_decay
from DA4RDM_RecSys_UserBased.recommendation import resource_recommender
from DA4RDM_RecSys_UserBased.extract_data import extract_data
import pandas as pd
import numpy as np


def get_recommendations(datapath, dataset_resources, ref_user, num_recommendation=3, outlier_detection_method="percentile"):
    data_extracted = extract_data(datapath)
    data_all_users = data_extracted[~data_extracted["UserId"].isnull()]
    data_all_resources = data_all_users[~data_all_users["ResourceId"].isnull()]
    data_file_selected = data_all_resources[~data_all_resources["FileId"].isnull()]
    unique_operations = data_file_selected["Operation"].unique()
    user_operation_dictionary = calculate_weight_decay(data_all_resources, data_all_users, dataset_resources)

    matrix_columns = ["UserId", "ResourceId", "ProjectId", "Roles"]
    for operation in unique_operations:
        matrix_columns.append(operation)
    matrix_columns.append("Duration")
    matrix_columns.append("Rating")
    data_matrix = pd.DataFrame(columns=[matrix_columns])
    matrix_data = create_operations_matrix(user_operation_dictionary, data_matrix, outlier_detection_method)
    resource_recommender(matrix_data, ref_user, num_recommendation)

    matrix_data.replace(0.0, np.nan, inplace=True)
    count_row = matrix_data.count(axis='columns')
    matrix_data = matrix_data.assign(Resource_Interaction_Count=count_row)
    matrix_data.replace(np.nan, 0, inplace=True)
    matrix_data = matrix_data.sort_values(by=['Resource_Interaction_Count'], ascending=False)