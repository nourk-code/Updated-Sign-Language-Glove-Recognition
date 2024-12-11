from pandas import DataFrame, read_csv
import pandas as pd 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import serial
import pyttsx3
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn import tree
from sklearn.externals import joblib
from collections import Counter

#loads dataset
df = pd.read_csv('dataset.csv')
X = df[['THUMB', 'INDEX', 'MIDDLE', 'RING', 'LITTLE', 'G1', 'G2', 'G3']]
Y = df['LABEL']

ser = serial.Serial('COM5', baudrate=9600, timeout=1)
for i in range(3):
    arduinodata = ser.readline().strip()
values = arduinodata.decode('ascii').split(',')
a, b, c, d, e, f, g, h = [int(s) for s in values]

example = np.array([a, b, c, d, e, f, g, h])
example = example.reshape(1, -1)

# Train-Test Split
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=60)

# K Nearest Neighbor
model = KNeighborsClassifier()
model.fit(x_train, y_train)
joblib.dump(model, 'KNN')
knn_model = joblib.load('KNN')
pred_knn = knn_model.predict(example)[0]
predicted = model.predict(x_test)
accuracy = accuracy_score(y_test, predicted)
print("Accuracy for KNN is", accuracy)

# Random Forest
rf = RandomForestRegressor(n_estimators=1000)
rf.fit(x_train, y_train)
predictions = rf.predict(x_test)
accuracy = r2_score(y_test, predictions)
print('\nAccuracy for random forest:\n', round(accuracy, 2) * 100, '%.')
joblib.dump(rf, 'randomforest')
rf_model = joblib.load('randomforest')
pred_rf = rf_model.predict(example)[0]

# Naive Bayes
GNB = GaussianNB()
GNB.fit(x_train, y_train)
joblib.dump(GNB, 'NaiveBayes')
nb_model = joblib.load('NaiveBayes')
pred_nb = nb_model.predict(example)[0]
predicted2 = GNB.predict(x_test)
accuracy2 = accuracy_score(y_test, predicted2)
print("Accuracy for Naive Bayes is", accuracy2)

# SVM
svc = svm.SVC(kernel='linear').fit(x_train, y_train)
joblib.dump(svc, 'SVM')
svc_model = joblib.load('SVM')
pred_svm = svc_model.predict(example)[0]
predicted3 = svc.predict(x_test)
accuracy3 = accuracy_score(y_test, predicted3)
print("Accuracy for SVM is", accuracy3)

# Logistic Regression
clf = LogisticRegression().fit(x_train, y_train)
joblib.dump(clf, 'logistic')
logistic_model = joblib.load('logistic')
pred_log = logistic_model.predict(example)[0]
predicted4 = clf.predict(x_test)
accuracy4 = accuracy_score(y_test, predicted4)
print("Accuracy for Logistic Regression is", accuracy4)

# Decision Tree
Dtree = tree.DecisionTreeClassifier().fit(x_train, y_train)
joblib.dump(Dtree, 'DecisionTree')
dtree_model = joblib.load('DecisionTree')
pred_tree = dtree_model.predict(example)[0]
predicted5 = Dtree.predict(x_test)
accuracy5 = accuracy_score(y_test, predicted5)
print("Accuracy for Decision Tree is", accuracy5)

#combines predictions
predictions = [pred_knn, pred_rf, pred_nb, pred_svm, pred_log, pred_tree]
final_prediction = Counter(predictions).most_common(1)[0][0]

#maps final prediction to words
if final_prediction == 0:
    abc = "victory"
elif final_prediction == 1:
    abc = "Comehere"
elif final_prediction == 2:
    abc = "Okay"
elif final_prediction == 3:
    abc = "Stop"
elif final_prediction == 4:
    abc = "You"
elif final_prediction == 5:
    abc = "Hope"
elif final_prediction == 6:
    abc = "Failure"
elif final_prediction == 7:
    abc = "Really"
elif final_prediction == 8:
    abc = "Quote"
elif final_prediction == 9:
    abc = "No"
elif final_prediction == 10:
    abc = "I Love you"
elif final_prediction == 11:
    abc = "Livelong"
elif final_prediction == 12:
    abc = "Thats it"
elif final_prediction == 13:
    abc = "Solidarity"
elif final_prediction == 14:
    abc = "Rock On"
elif final_prediction == 15:
    abc = "Good Bye"
elif final_prediction == 16:
    abc = "What is wrong"
elif final_prediction == 17:
    abc = "Why"
elif final_prediction == 18:
    abc = "Rest room"
elif final_prediction == 19:
    abc = "Joy"
elif final_prediction == 20:
    abc = "Friendship"
elif final_prediction == 21:
    abc = "Adventure"
elif final_prediction == 22:
    abc = "Achievement"
elif final_prediction == 23:
    abc = "Harmony"
elif final_prediction == 24:
    abc = "Courage"
elif final_prediction == 25:
    abc = "Freedom"
else:
    abc = "Unknown"

#speaks 
engine = pyttsx3.init()
engine.say('Predicted Output')
engine.say(abc)
engine.runAndWait()
