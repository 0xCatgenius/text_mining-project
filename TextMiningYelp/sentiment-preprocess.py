
# coding: utf-8

# In[1]:

import csv
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize
from sklearn.utils import shuffle

# %%
# export file names
training_file_path = "review_by_sentences_training.csv"
testing_file_path = "review_by_sentences_testing.csv"
evaluation_file_path = "review_by_sentences_evaluation.csv"


# %%
# Import the data file
data_raw = pd.read_csv("Review.csv")

#shuffle the review order
data = shuffle(data_raw)

# Select only those important columns for our project
df1 = data[['_id', 'UserId', 'BusinessId', 'Rating', 'Text']]
print("len: ", len(df1.index))
# print(df1)

# total num of reviews
num_reviews = len(df1.index)

# num of reviews for evaluation
num_evaluation =int(0.1*50)


# num of reviews for training
num_training = int(0.7*50)

# num of reviews for testing
num_testing = int(0.2*50)

#split df into training, testing, evaluation
df_training = data.iloc[:num_training]
df_testing = data.iloc[num_training:num_training+num_testing]
df_evaluation = data.iloc[num_training+num_testing: num_training+num_testing+num_evaluation]

# end_testing = num_evaluation+num_testing
# df_testing = data.iloc[num_training:end_testing]
# df_training = data.iloc[end_testing:num_training]


print("df_training: ", df_training)

# Preview the data
data.head()

# %%
def write_records(data, output_file_path):
    num_rewiews = 0
    num_sentences = 0
    # # Import the data file
    # data = pd.read_csv(input_file_path)
    # Select only those important columns for our project
    df1 = data[['_id', 'UserId', 'BusinessId', 'Rating', 'Text']]
    print("data_type: ", type(df1))


    with open(output_file_path, 'w', encoding='utf-8') as writeFile:
        reviewPartDictionary = dict()
        for index, r in df1.iterrows():

            num_rewiews += 1
            reviewId = r['_id']
            businessId = r['BusinessId']
            userId = r['UserId']
            rating = r['Rating']
            body = r['Text']

            # break the body of review into sentences
            sentenceList = sent_tokenize(body)
            numberOfSentences = len(sentenceList)
            reviewPartDictionary[str(reviewId)] = numberOfSentences
            num_sentences += numberOfSentences

            # store review id, sentence id, sentence into csv file
            for i in range(0, numberOfSentences):
                row = [reviewId, str(i), sentenceList[i]]
                fname = str(reviewId) + '#' + str(i) + '.txt'
                writer = csv.writer(writeFile)
                writer.writerow(row)
    writeFile.close()

    print("num_reviews: ", num_rewiews)
    print("num_sentences: ", num_sentences)

# %%
write_records(df_training, training_file_path)
write_records(df_testing, testing_file_path)
write_records(df_evaluation, evaluation_file_path)


#%%
annotated_training = pd.read_excel("annotated_training.xlsx")
annotated_testing = pd.read_excel("annotated_testing.xlsx")
annotated_evaluation = pd.read_excel("annotated_evaluation.xlsx")
data_raw = pd.read_csv("Review.csv")
data_raw.head()
# annotated_training.head()

#%%
def add_info (df_lookup, df_input, col_name, output_file):
    df_output = df_input.copy()
    df_output[col_name] = np.nan
    for index, r in df_output.iterrows():
        # print('r_lookup_id: ', df_lookup.loc[df_lookup['_id'] == r['review_id']])
        # print("r_id: ", r['review_id'])
        r_lookup = df_lookup.loc[df_lookup['_id'] == r['review_id']]
        info = r_lookup[col_name]
        # print("info: ", info, " ", type(info))
        
        df_output.loc[index, col_name] = int(info)
        r[col_name] = info
    
    df_output.to_csv(output_file)
    print("finished adding ", col_name, " to ", output_file)

#%%
add_info(data_raw, annotated_training, "Rating", 'annotated_training_w_rating.csv')
add_info(data_raw, annotated_testing, "Rating", 'annotated_testing_w_rating.csv')
add_info(data_raw, annotated_evaluation, "Rating", 'annotated_evaluation_w_rating.csv')



