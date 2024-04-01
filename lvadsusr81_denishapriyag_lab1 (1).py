# -*- coding: utf-8 -*-
"""LVADSUSR81_DENISHAPRIYAG_LAB1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C3AscFI6EgPH3v0pki1RTQBcCFBh-db-
"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, precision_score, f1_score, recall_score, confusion_matrix
from sklearn.preprocessing import MinMaxScaler
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# Load the dataset
df = pd.read_csv("/content/drive/MyDrive/winequality-red.csv")
df.columns.tolist()

df.info()
df.head(5)
df.isna().sum()
df.shape

data = df.fillna(df.mean())
data.shape

# -------------Handle missing values------------
data.isna().sum()

Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1

outliers = ((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)
print(outliers)
df1 = data[~outliers]

#-----------Data Transformation-------------
def map_quality(quality):
    if quality >= 3 and quality <= 6:
        return 0
    elif quality >= 7 and quality <= 8:
        return 1
    else:
        return None
df1['quality'] = df1['quality'].apply(map_quality)

quality_distribution = df1['quality'].value_counts()
print("Wine quality distribution:")
print(quality_distribution)

plt.figure(figsize=(8, 6))
quality_distribution.plot(kind='bar', color='blue')
plt.title('Wine Quality Distribution')
plt.xlabel('Quality')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

from imblearn.over_sampling import SMOTE
X = df1.drop(columns=['quality'])
y = df1['quality']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

selected_features = X.columns

from sklearn.metrics import classification_report
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train_resampled, y_train_resampled)
y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", round(accuracy*100,2),"%")
prec = precision_score(y_test, y_pred)
print("Precision:", round(prec*100,2),"%")
recall = recall_score(y_test, y_pred)
print("Recall:", round(recall*100,2),"%")