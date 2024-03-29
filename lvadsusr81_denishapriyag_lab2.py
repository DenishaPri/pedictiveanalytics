# -*- coding: utf-8 -*-
"""LVADSUSR81_DENISHAPRIYAG_LAB2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-0lRWJ0nadPRnhoXqLT1sd1OjnAPgnTA
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

df = pd.read_csv('/content/drive/MyDrive/booking.csv')
# print(df)
df.columns.tolist()
# df.info()

# -------------Handle missing values------------
if df.isna().sum().sum()>0:
  df.dropna(inplace=True)

#---------outliers----------
X = df.drop(['type of meal','room type', 'market segment type','booking status','Booking_ID','date of reservation'], axis=1)
x = df.drop('booking status', axis=1)
y = df['booking status']
print('Before removing outliers')
print()
print()
#creating a box plot
for i in X:
  plt.figure(figsize = (5,5))
  sns.boxplot(data=X[i])
  plt.title(i)
  plt.ylabel('Values')
  plt.xticks(rotation = 45)
  plt.show()
#replace outlier with median
def detect_and_treat_outliers(df,columns):

  for col in columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    #define bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    #replace outliers with the median of column
    median = df[col].median()
    df[col] = np.where((df[col] < lower_bound) | (df[col] > upper_bound), median, df[col])

  return df

df = detect_and_treat_outliers(df,X)
# print(df)
X = df.drop(['type of meal','room type', 'market segment type','booking status','Booking_ID','date of reservation'], axis=1)
x = df.drop('booking status', axis=1)
y = df['booking status']
print('After removing outliers')
print()
print()
#creating a box plot after removing outliers
for i in X:
  plt.figure(figsize = (5,5))
  sns.boxplot(data=X[i])
  plt.title(i)
  plt.ylabel('Values')
  plt.xticks(rotation = 45)
  plt.show()

# ---------------Encoding categorical data---------

label_encoder = LabelEncoder()
df['type of meal'] = label_encoder.fit_transform(df['type of meal'])
df['room type'] = label_encoder.fit_transform(df['room type'])
df['market segment type'] = label_encoder.fit_transform(df['market segment type'])
df['booking status'] = label_encoder.fit_transform(df['market segment type'])
df['Booking_ID'] = label_encoder.fit_transform(df['market segment type'])
df['date of reservation'] = label_encoder.fit_transform(df['market segment type'])

#------------------ Feature selection-------------
x = df.drop('booking status', axis=1)
y = df['booking status']
#---------------- data cleaning---------------
if df.duplicated().sum()>0:
  df.drop_duplicates(inplace = True)

# ------------Data Splitting----------------

x_train , x_test, y_train, y_test = train_test_split(x,y,test_size = .5, random_state = 42)

# --------------Model Development and Training---------
clf = LogisticRegression()
clf = clf.fit(x_train,y_train)
model = clf.predict(x_test)
print('predicted',model)
print()
print('test',y_test)

# -----------model evaluation----------
accuracy = accuracy_score(y_test,model)
precision = precision_score(y_test,model, average = 'weighted')
recall = recall_score(y_test,model, average = 'weighted')
f1 = f1_score(y_test,model, average = 'weighted')

conf_matrix = confusion_matrix(y_test,model)
print('accuracy: ',accuracy)
print('precision: ',precision)
print('recall: ',recall)
print('f1: ',f1)
print('conf_matrix: ',conf_matrix)