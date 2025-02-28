"""
Iris Dataset Classification Script

This script loads the Iris dataset, preprocesses it using normalization, splits it into training 
and testing sets, trains a K-Nearest Neighbors (KNN) classifier, and evaluates its performance.

Modules Used:
    - pandas: Used for handling datasets.
    - sklearn.datasets: Provides access to the Iris dataset.
    - sklearn.preprocessing: Used for feature normalization (MinMaxScaler).
    - sklearn.model_selection: Splits data into training and testing subsets.
    - sklearn.neighbors: Implements the KNN classifier.
    - sklearn.metrics: Computes model accuracy.
    - numpy: Provides numerical operations.

Usage:
    Run this script to train and test a KNN classifier on the Iris dataset.
"""

import pandas as pd  # pandas used to manage datasets
from sklearn.datasets import load_iris  # Loading the Iris dataset
from sklearn.preprocessing import MinMaxScaler  # For normalizing feature values
from sklearn.model_selection import train_test_split  # Splitting data into training and testing subsets
from sklearn.neighbors import KNeighborsClassifier  # Importing KNN classifier
from sklearn.metrics import accuracy_score  # Used for evaluating model performance
import numpy as np  # Used for numerical operations

# Load the Iris dataset
data = load_iris()
X = data.data  # Features (sepal length, sepal width, petal length, petal width)
y = data.target  # Labels (Iris species)

# Normalize the feature values to range [0,1]
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset into training (80%) and testing (20%) subsets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize KNN classifier with k=3
knn = KNeighborsClassifier(n_neighbors=3)

# Train the model on the training data
knn.fit(X_train, y_train)

# Predict labels on the test set
y_pred = knn.predict(X_test)

# Calculate accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)

# Output results
print(f"KNN Classifier Accuracy: {accuracy:.2f}")
