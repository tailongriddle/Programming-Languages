import sys
import subprocess
import ssl
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn"]) 
subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"]) 
subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"]) 

'''
Feel free to delete the lines above here once you have installed the necessary packages
'''

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
import requests

#  Introduction to Machine Learning with sckit-learn (Lab 7)
#
#  In this lab, you will explore the basics of machine learning using the scikit-learn library.
#  You will work with several datasets and models to understand the impact of different features.
#  You will also explore the impact of different parameters on the performance of the models.
#
#  The lab is divided into four sections:
#  1. Linear Regression with Boston Housing Dataset
#  2. Logistic Regression with Iris Dataset
#  3. Decision Tree with Titanic Survival Dataset
#  4. Clustering with Mall Customer Segmentation Data
#
#  Each sections includes two parts:
#      Part 1: Read/understand/modify the code
#      Part 2: Answer the questions
#
#  Most of the focus is on the first section (Linear Regression with Boston Housing Dataset).
#  The other sections are included to give a quick exposure to other ML algorithms.

def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):
    '''
    This function helps to visualize the decision boundaries of the logisitc regression model.
    You can ignore the details of this function, but you'll use it to visualize the decision boundaries!
    '''
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                    alpha=0.8, c=colors[idx],
                    marker=markers[idx], label=iris.target_names[cl],
                    edgecolor='black')

# For reproducibility
np.random.seed(42)

########################################################################

# -------------------------------
# Linear Regression with Boston Housing Dataset
# -------------------------------

'''
The Boston Housing Dataset was compiled in the 1970s. It contains data on various aspects of housing in
the Boston area, including 506 instances with 14 attributes, such as average number of rooms per dwelling,
property tax rate, and pupil-teacher ratio by town.

The "B" feature within this dataset stands for the proportion of Black residents in the
neighborhood, calculated using the formula B=1000*(Bk-0.63)^2, where Bk is the proportion
of Black residents in the town. 

This feature has become controversial for its implicit racial bias and ethical implications, raising
significant concerns about perpetuating stereotypes and discrimination through data and machine learning
models. Its use has sparked discussions on the importance of ethical considerations and the potential
for harm when using datasets that include sensitive demographic information.

Task: Investigating the Impact of the "B" Feature

Part 1: Technical Analysis
    1. Reintroduce the "B" Feature: At the bottom of the code for this section, create another copy of
       the dataset with the "B" feature included. (There is a TODO comment showing where to put this)
    2. Train the linear regression model with "B" feature included, and make the same plot as before.
       Can you notice a difference in the resulting plot?
    3. To more explicitly show the difference between the two models, plot the residuals (difference
       between predicted and actual home values) for predictions made with and without the "B" feature.
       Here is code that will calculate the residuals for both models, and the plot the difference
       between the two sets of residuals:

        residual_diff = (y_pred_with_b - y_test_boston) - (y_pred_boston - y_test_boston)
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test_boston, residual_diff, color='green', s=10)
        plt.axhline(y=0, color='black', linestyle='--')
        plt.xlabel('Actual Median Value ($1000s)')
        plt.ylabel('Residual Difference (With B - Without B)')
        plt.title('Difference in Residuals With and Without "B" Feature')
        plt.show()

       In this final plot, points above the y=0 line indicate cases where including "B" worsened the prediction
       (increased the residual), while points below indicate improvements (decreased the residual).

Part 2 - Reflection:
        1. How does the inclusion of the "B" feature impact the accuracy of your model? Is the change
           significant?
        2. Considering the nature of the "B" feature, what might be the social implications of using
           this feature in a model that predicts housing prices?
        3. How does the inclusion of such features contribute to biases in machine learning models? 
           Discuss the concept of fairness in this context.
        4. In your opinion, should demographic information related to race or ethnicity be used in 
           predictive modeling for housing prices? Why or why not?
'''

# Fetch the Boston Housing dataset
data_url = "http://lib.stat.cmu.edu/datasets/boston"
response = requests.get(data_url)
data_str = response.text
lines = data_str.split('\n')[22:]
combined_lines = [lines[i] + lines[i + 1] for i in range(0, len(lines)-1, 2)]
data_list = [line.split() for line in combined_lines if line.strip() != '']
columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']

# Create the dataset from the raw values
boston_df = pd.DataFrame(data_list, columns=columns).astype(float)

# Excluding the 'B' feature for ethical considerations
boston_df = boston_df.drop(['B'], axis=1)

# MEDV is what we're trying to predict
X_boston = boston_df.drop('MEDV', axis=1)
y_boston = boston_df['MEDV']

X_train_boston, X_test_boston, y_train_boston, y_test_boston = train_test_split(X_boston, y_boston, test_size=0.2, random_state=42)

# Train a linear regression model
lr = LinearRegression()
lr.fit(X_train_boston, y_train_boston)

# Evaluate the model on the test set
y_pred_boston = lr.predict(X_test_boston)

# Plot the actual vs predicted values
print("Boston Housing Dataset - Linear Regression")
print("RMSE:", np.sqrt(mean_squared_error(y_test_boston, y_pred_boston)))
plt.figure(figsize=(10, 6))
plt.scatter(y_test_boston, y_pred_boston)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted Home Values')
plt.show()

# TODO: Create another copy of the dataset, with the "B" feature included
boston_df_wB = pd.DataFrame(data_list, columns=columns).astype(float)

X_boston_wB = boston_df_wB.drop('MEDV', axis=1)
y_boston_wB = boston_df_wB['MEDV']

X_train_boston_wB, X_test_boston_wB, y_train_boston_wB, y_test_boston_wB = train_test_split(X_boston_wB, y_boston_wB, test_size=0.2, random_state=42)


# TODO: Train, evaluate, and plot a linear regression model on the copy with "B" included
# Train
lr_wB = LinearRegression()
lr_wB.fit(X_train_boston_wB, y_train_boston_wB)

# Evaulate
y_pred_boston_wB = lr_wB.predict(X_test_boston_wB)

# Plot
print("Boston Housing Dataset With B - Linear Regression")
print("RMSE:", np.sqrt(mean_squared_error(y_test_boston_wB, y_pred_boston_wB)))
plt.figure(figsize=(10, 6))
plt.scatter(y_test_boston_wB, y_pred_boston_wB)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted Home Values With B')
plt.show()

# TODO: Calculate the residuals for both models and plot the difference

residual_diff = (y_pred_boston_wB - y_test_boston) - (y_pred_boston - y_test_boston)
plt.figure(figsize=(10, 6))
plt.scatter(y_test_boston, residual_diff, color='green', s=10)
plt.axhline(y=0, color='black', linestyle='--')
plt.xlabel('Actual Median Value ($1000s)')
plt.ylabel('Residual Difference (With B - Without B)')
plt.title('Difference in Residuals With and Without "B" Feature')
plt.show()

########################################################################

# -------------------------------
# Logistic Regression with Iris Dataset
# -------------------------------

'''
The Iris dataset is a foundational dataset in the field of machine learning and statistics, introduced by the British biologist
Ronald Fisher in 1936. It consists of 150 observations of iris flowers, evenly distributed across three different species:
   Iris setosa, Iris versicolor, and Iris virginica.
For each observation, the dataset records four features:
   The length and the width of the sepals and petals in centimeters.

Task: Compare the effectiveness of using different pairs of features.
    Part 1. Modify the X = iris.data[:, [2, 3]] line to use different columns and then replot the decision boundaries.
    Part 2. How does the decision boundary change when you use sepal length and sepal width instead of petal length and petal width?
'''

# Load the Iris dataset
iris = load_iris()

# Columns are [sepal length, sepal width, petal length, petal width]
# We'll use petal length and petal width for this example

X = iris.data[:, [0, 1]]  # Use only petal length and petal width (index 2 and 3)
y = iris.target

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Train a logistic regression model
logreg = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')
logreg.fit(X_train, y_train)

# Plot decision regions
plt.figure(figsize=(10, 7))
plot_decision_regions(X_test, y_test, classifier=logreg)
plt.xlabel('Petal length [cm]')
plt.ylabel('Petal width [cm]')
plt.legend(loc='upper left')
plt.title('Logistic Regression on Iris Dataset')
plt.show()

########################################################################

# -------------------------------
# Decision Tree with Titanic Survival Dataset
# -------------------------------

'''
The Titanic survival dataset contains traits and survival outcomes of passengers aboard the RMS Titanic, which sank in 1912.
Each entry in this dataset represents a passenger, with key features including:
   Passenger class (a proxy for socio-economic status), sex, age, number of siblings/spouses aboard, 
   number of parents/children aboard, ticket fare, cabin, and embarked port.

https://campus.lakeforest.edu/frank/FILES/MLFfiles/Bio150/Titanic/TitanicMETA.pdf
Task: Investigate the impact of the tree's depth on its performance.
    Part 1. Adjust the max_depth parameter in the DecisionTreeClassifier instantiation and plot the accuracy for different depths.
    Part 2. What happens to the model's overall accuracy on the training and test sets as you change the max_depth parameter of the Decision Tree?
'''

# Download Titanic dataset
titanic_url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
titanic_df = pd.read_csv(titanic_url)
titanic_df['Sex'] = titanic_df['Sex'].map({'male': 0, 'female': 1})
titanic_df = titanic_df[['Survived', 'Pclass', 'Sex', 'Age', 'Siblings/Spouses Aboard', 'Parents/Children Aboard', 'Fare']].dropna()

# Split the dataset into features and target
X_titanic = titanic_df.drop('Survived', axis=1)
y_titanic = titanic_df['Survived']  # We are trying to predict the survival

# Split the dataset into training and test sets
X_train_titanic, X_test_titanic, y_train_titanic, y_test_titanic = train_test_split(X_titanic, y_titanic, test_size=0.2, random_state=42)

# Train a decision tree model
dt = DecisionTreeClassifier(max_depth=5)
dt.fit(X_train_titanic, y_train_titanic)
y_pred_titanic = dt.predict(X_test_titanic)

print("\nTitanic Survival Dataset - Decision Tree")
print("Accuracy:", accuracy_score(y_test_titanic, y_pred_titanic))

plt.figure(figsize=(20,10))
plot_tree(dt, filled=True, feature_names=X_titanic.columns, class_names=['Not Survived', 'Survived'],
          impurity=False, proportion=True)
plt.title('Decision Tree - Titanic Survival Prediction')
plt.show()

########################################################################

# -------------------------------
# Clustering with Mall Customer Segmentation Data
# -------------------------------

'''
The Mall Customer Segementation dataset consists of data collected from customers visiting a mall, capturing attributes such as:
   customer ID, gender, age, annual income, and spending score.
The spending score is a subjective number assigned by the mall based on customer behavior and spending nature, typically ranging from 1 to 100.

Task: Explore the effect of the number of clusters.
    Part 1. Change the n_clusters parameter in the KMeans instantiation and observe the new cluster boundaries by re-running the plotting code.
    Part 2. How does changing the number of clusters (n_clusters) affect the visualization and the interpretation of customer segments?
'''

# Download Mall Customer dataset
mall_customers_url = "https://raw.githubusercontent.com/PatrickJWalsh/Mall-Customer-Segmentation/master/Mall%20Customers.csv"
mall_customers_df = pd.read_csv(mall_customers_url)

X_mall_customers = mall_customers_df[['Annual Income (k$)', 'Spending Score (1-100)']].values

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_mall_customers)

# Train a KMeans clustering model
kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(X_scaled)
y_kmeans = kmeans.predict(X_scaled)

print("\nMall Customer Segmentation - Clustering")
plt.figure(figsize=(10, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y_kmeans, s=50, cmap='viridis')
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.5)
plt.title('Customer Segments')
plt.xlabel('Annual Income (Standardized)')
plt.ylabel('Spending Score (Standardized)')
plt.show()
