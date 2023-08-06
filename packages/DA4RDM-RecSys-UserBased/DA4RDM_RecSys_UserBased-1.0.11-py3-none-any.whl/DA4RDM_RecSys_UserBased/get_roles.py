import pandas as pd


def get_role(r_id, operations_list):
    roles = []
    key_activity = "Add resource"
    operations_list_lower = []
    for op in operations_list:
        operations_list_lower.append(op.lower())
    for x in r_id:
        if pd.isnull(x):
            continue
        elif x.upper() == "BE294C5E-4E42-49B3-BEC4-4B15F49DF9A5":
            roles.append("Owner")
        elif x.upper() == "508B6D4E-C6AC-4AA5-8A8D-CAA31DD39527":
            roles.append("Member")
    if key_activity.lower() in operations_list_lower:
        roles.append("Data Manager")
    roles = '/'.join(roles)
    return roles
