import pandas as pd
import numpy as np
import pickle

#import classifiers
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB  
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

#import k-fold
from sklearn.model_selection import KFold

#import cross_val_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score

#import grid search
from sklearn.model_selection import GridSearchCV

#import confusion matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

#import cross_val_predict
from sklearn.model_selection import cross_val_predict

#import preprocessing
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

le = preprocessing.LabelEncoder()


Label = "Credit"
Features = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","A13","A14","A15","A16","A17","A18","A19"]


# classifiers to test
classifiers = {"Logistic Regression": LogisticRegression(),
               "Naive Bayes": GaussianNB(),
               "SVM": SVC(),
               "Decision Tree": DecisionTreeClassifier(),
               "Random Forest": RandomForestClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
               "KNN": KNeighborsClassifier()
               }




def saveBestModel(clf):
    pickle.dump(clf, open("bestModel.model", 'wb'))

def readData(file):
    df = pd.read_csv(file)
    return df

def trainOnAllData(df, clf):
    #Use this function for part 4, once you have selected the best model
    X = df[Features].values 
    Y = df[Label].values
    clf.fit(X, Y)
    saveBestModel(clf)
    

df = readData("credit_train.csv")


#scale data
X = df[Features].values 
Y = df[Label].values
X_scaled = StandardScaler().fit_transform(X)

Y_encoded = le.fit_transform(Y) # encode the target variable

kf = KFold(n_splits=10) # 10-fold cross-validation

print("AUROC    STD    Classifier")
# calculates the AUROC and outputs into a table
for name, classifier in classifiers.items():
    scores = cross_val_score(classifier, X_scaled, Y, cv=kf, scoring='roc_auc')
    print("%0.2f     %0.2f   [%s]" % (scores.mean(), scores.std(), name))

# hyperparameter tuning 
# param_grid_f = {'n_estimators': [100, 500, 1000], 'max_depth': [3, 5, 7, 9]}
# grid_search_f = GridSearchCV(RandomForestClassifier(), param_grid_f, cv=kf, scoring='roc_auc')
# grid_search_f.fit(X_scaled, Y)
# print("Best parameters(RF): ", grid_search_f.best_params_)

# param_grid_s = {'C': [6, 10, 40], 'gamma': [0.009, 0.001, 0.0001]}
# grid_search_s = GridSearchCV(SVC(), param_grid_s, cv=kf, scoring='roc_auc')
# grid_search_s.fit(X_scaled, Y)
# print("Best parameters(SVC): ", grid_search_s.best_params_)

print("Parameter tuning test")
print("AUROC    STD    Classifier")
score_RF = cross_val_score(RandomForestClassifier(n_estimators=1000,max_depth=9), X_scaled, Y, cv=kf, scoring='roc_auc')
print("%0.2f     %0.2f   [%s]" % (score_RF.mean(), score_RF.std(), "Random Forest"))

score_SVC = cross_val_score(SVC(C=10,gamma=0.001), X_scaled, Y, cv=kf, scoring='roc_auc')
print("%0.2f     %0.2f   [%s]" % (score_SVC.mean(), score_SVC.std(), "SVM"))

# confusion matrix
y_pred_RF = cross_val_predict(RandomForestClassifier(n_estimators=1000,max_depth=9), X_scaled, Y_encoded, cv=kf)
confusion_matrix_RF = confusion_matrix(Y_encoded, cross_val_predict(RandomForestClassifier(n_estimators=1000,max_depth=9), X_scaled, Y_encoded, cv=kf))
print("\nConfusion Matrix")
print(confusion_matrix_RF)

# accuracy
accuracy_RF = accuracy_score(Y_encoded, y_pred_RF)
print("\nAccuracy: ", accuracy_RF)

# precision
precision_RF = precision_score(Y_encoded, y_pred_RF)
print("\nPrecision: ", precision_RF)

# recall
recall_RF = recall_score(Y_encoded, y_pred_RF)
print("\nRecall: ", recall_RF.mean())

# AUROC
auroc_RF = roc_auc_score(Y_encoded, y_pred_RF)
print("\nAUROC: ", auroc_RF)

best_model = RandomForestClassifier(n_estimators=1000,max_depth=9)

# save
saveBestModel(RandomForestClassifier(n_estimators=1000,max_depth=9))


# save to csv file
output_df = pd.DataFrame(X_scaled, columns=Features)  # Features
output_df['Ground Truth'] = Y_encoded
output_df['Prediction'] = y_pred_RF
output_df.to_csv('bestModel.output', index=False)

