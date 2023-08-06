"""Function to get resource recommendation"""

from sklearn.neighbors import NearestNeighbors
import json


def recommend_resources(df, df1, user, num_recommended_resources):
    # print('The list of the Resources {} has used \n'.format(user))

   # for m in df[df[user] > 0][user].index.tolist():
    #   print(m)

    # print('\n')

    recommended_resources = []

    for m in df[df[user] == 0].index.tolist():
        index_df = df.index.tolist().index(m)
        predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
        recommended_resources.append((m, predicted_rating))

    sorted_rm = sorted(recommended_resources, key=lambda x: x[1], reverse=True)

    print('The list of the Recommended Resource(s)  \n')
    rank = 1
    for recommended_res in sorted_rm[:num_recommended_resources]:
        if recommended_res[1] == 0.0:
            continue
        else:
            print('{}: {} - predicted rating:{}'.format(rank, recommended_res[0], recommended_res[1]))
        rank = rank + 1
    my_details = {
        'Recommendations': dict(Ref_User_ID=user, Recommendation=sorted_rm[:num_recommended_resources]),
    }
    with open('Data/Recommendation.json', 'w') as json_file:
        json.dump(my_details, json_file)


def resource_recommender(df, user, num_recommendation):
    number_neighbors = 3
    knn = NearestNeighbors(metric='euclidean', algorithm='brute')
    knn.fit(df.values)
    distances, indices = knn.kneighbors(df.values, n_neighbors=number_neighbors)

    df1 = df.copy()

    user_index = df.columns.tolist().index(user)

    for m, t in list(enumerate(df.index)):
        if df.iloc[m, user_index] == 0:
            sim_resources = indices[m].tolist()
            resource_distances = distances[m].tolist()

            if m in sim_resources:
                id_resource = sim_resources.index(m)
                sim_resources.remove(m)
                resource_distances.pop(id_resource)

            else:
                sim_resources = sim_resources[:number_neighbors - 1]
                resource_distances = resource_distances[:number_neighbors - 1]

            resource_similarity = [1 - x for x in resource_distances]
            resource_similarity_copy = resource_similarity.copy()
            nominator = 0

            for s in range(0, len(resource_similarity)):
                if df.iloc[sim_resources[s], user_index] == 0:
                    if len(resource_similarity_copy) == (number_neighbors - 1):
                        resource_similarity_copy.pop(s)
                    else:
                        resource_similarity_copy.pop(s - (len(resource_similarity) - len(resource_similarity_copy)))
                else:
                    nominator = nominator + resource_similarity[s] * df.iloc[sim_resources[s], user_index]

            if len(resource_similarity_copy) > 0:
                if sum(resource_similarity_copy) > 0:
                    predicted_r = nominator / sum(resource_similarity_copy)
                else:
                    predicted_r = 0
            else:
                predicted_r = 0

            df1.iloc[m, user_index] = predicted_r
    recommend_resources(df, df1, user, num_recommendation)
