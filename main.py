#!/usr/bin/env python
# coding: utf-8

# In[132]:


#The project folder should contain a sample email folder, in which contains folder named "Spams" and "Hams".
#IF the files are organized differently, all parameter passed into construct_paths should change accordingly.


# In[133]:


import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#create a list of paths    
def construct_paths(pre):
    mains = os.listdir(pre)
    mains.sort() #to get rid of the parent directory entry
    mains.pop(0)
    print(mains)
    fulls = [pre + main for main in mains]
    print(fulls)
    return fulls


# In[134]:


# create a exhaustive list of words
# input: path to the email folder
def create_dict(pre):
    paths = construct_paths(pre + "Spams/")
    paths += construct_paths(pre + "Hams/")
    words = []
    for path in paths:
        f = open(path)
        content = f.read()
        words += content.split(" ")

    for word in words: 
        if not word.isalnum():
            word = "//"

    out_dict = Counter(words)
    del out_dict["//"] #delete non_valid_words 
    return out_dict


# In[135]:


#label words and classify ALL result-known emails in email folder. 
#input: the dictionary, and the path to the email folder
def label_words(in_dict, pre): 
    spam_paths = construct_paths(pre + "Spams/") #list of paths for spam email files
    num_spam = len(spam_paths);
    
    ham_paths = construct_paths(pre + "Hams/") #list of paths for ham email files
    num_ham = len(ham_paths);
    
    y = [True] * len(spam_paths) #spam is true, ham is false
    y += [False] * len(ham_paths)
    
    paths = spam_paths + ham_paths
    
    x = [] #counts for each word in dictionary in all emails; each entry is a list of counts
    # a sparse matrix of the size (num_emails) * (num_words_in_exhaustie list)  
    # works together with y, the result vector
    
    for path in paths:
        f = open(path)
        content = f.read().split(" ") #a message splitted into a list of words
         
        counts = []; #counts for each word in dictionary in ONE email; each entry is a number
        for given_word in in_dict:
            count = content.count(given_word)
            counts.append(count) # append to a row
        x.append(counts) #append one row
    return x, y


# In[136]:


#split the data into a training set and a set for testing
def train_classifier(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.5) 
    
    #train the model
    classifier = MultinomialNB();
    classifier.fit(x_train, y_train);

    #test the model
    predicted_y = classifier.predict(x_test);
    accuracy = accuracy_score(predicted_y, y_test) #compare predicted_y to the real result y_test
    print(accuracy)
    
    return classifier


# In[137]:


#msg: the message as a string
def self_test_msg(msg):
    x = [] #aka count; the count for all words in dictionary; a list of counts
    for given_word in g_dict:
        count = msg.split().count(given_word)
        x.append(count)
    prediction = g_classifier.predict([x]) #it takes a 2D array.put [] to indicate it is a 1 by n matrix.
    if (prediction[0]):
        print("we predict it is a spam")
    else:
        print("we predict it is ham")


# In[138]:


g_dict = create_dict("sample emails/")
x,y = label_words(g_dict, "sample emails/")
g_classifier = train_classifier(x,y)
self_test_msg("hello i am homie. i am 22 years old")

