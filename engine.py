import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
df_percent = pickle.load(open('model_up.pkl', 'rb'))

# TF-IDF Vectorization
df_percent.set_index('name', inplace=True)
indices = pd.Series(df_percent.index)

# Creating tf-idf matrix
tfidf = TfidfVectorizer(analyzer='word', ngram_range=(
    1, 2), min_df=0, stop_words='english')
tfidf_matrix = tfidf.fit_transform(df_percent['reviews_list'])

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)


def recommend_restaurants(name, cosine_similarities=cosine_similarities):

    # Create a list to put top restaurants
    recommend_restaurant = []

    # Find the index of the restaurant you entered
    idx = indices[indices == name].index[0]

    # Find the restaurants with a similar cosine-sim value and order them from biggest numbers
    score_series = pd.Series(
        cosine_similarities[idx]).sort_values(ascending=False)

    # Extract top 30 restaurant indexes with a similar cosine-sim value
    top30_indexes = list(score_series.iloc[0:31].index)

    # Names of the top 30 restaurants
    for each in top30_indexes:
        recommend_restaurant.append(list(df_percent.index)[each])

    # Creating the new data set to show similar restaurants
    similar_restaurants = pd.DataFrame(
        columns=['cuisines', 'Mean Rating', 'cost'])

    # Create the top 30 similar restaurants
    for each in recommend_restaurant:
        similar_restaurants = similar_restaurants.append(pd.DataFrame(
            df_percent[['cuisines', 'Mean Rating', 'cost']][df_percent.index == each].sample()))

    # Drop the same named restaurants and sort only the top 10 by the highest rating
    similar_restaurants = similar_restaurants.drop_duplicates(
        subset=['cuisines', 'Mean Rating', 'cost'], keep=False)
    similar_restaurants = similar_restaurants.sort_values(
        by='Mean Rating', ascending=False).head(10)

    return similar_restaurants
