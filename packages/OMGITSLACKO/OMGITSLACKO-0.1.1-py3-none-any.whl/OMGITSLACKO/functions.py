import pandas as pd
from IPython.core.display import HTML

def correlation(df):
    corr = df.corr()
    corr_stacked = corr.stack().reset_index()
    corr_stacked.columns = ['var1', 'var2', 'corr']
    corr_stacked = corr_stacked[(corr_stacked['corr'] != 1.0) & (corr_stacked['corr'] != -1.0)]
    corr_stacked = corr_stacked[corr_stacked['var1'] < corr_stacked['var2']] # Remove duplicates
    corr_stacked.sort_values(by=['corr'], ascending=False, inplace=True)

    html_table = '<table><thead><tr><th>Variable 1</th><th>Variable 2</th><th>Correlation</th></tr></thead>'
    html_table += '<tbody>'
    for index, row in corr_stacked.iterrows():
        html_table += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(row['var1'], row['var2'], round(row['corr'], 2))
    html_table += '</tbody></table>'

    return HTML('<div style="max-height:300px; overflow-y:auto;">{}</div>'.format(html_table))
    
def find_best_model_classification(df_X_train, df_X_test, df_y_train, df_y_test):
    
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LogisticRegression, RidgeClassifier, PassiveAggressiveClassifier, Perceptron
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, ExtraTreesClassifier, BaggingClassifier, IsolationForest, StackingClassifier
    from sklearn.svm import SVC, OneClassSVM
    from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
    from sklearn.naive_bayes import GaussianNB, BernoulliNB
    from sklearn.neural_network import MLPClassifier
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis
    from sklearn.cluster import KMeans
    from xgboost import XGBClassifier
    from lightgbm import LGBMClassifier
    from catboost import CatBoostClassifier
    from imblearn.ensemble import BalancedRandomForestClassifier
    from sklearn import metrics
    
    models = [
        ("Logistic Regression", LogisticRegression(max_iter=1000)),
        ("Decision Tree", DecisionTreeClassifier()),
        ("Random Forest", RandomForestClassifier()),
        ("Gradient Boosting", GradientBoostingClassifier()),
        ("XGBoost", XGBClassifier(eval_metric="logloss")),
        ("LightGBM", LGBMClassifier()),
        ("Support Vector Machine", SVC()),
        ("K-Nearest Neighbors", KNeighborsClassifier()),
        ("Naive Bayes", GaussianNB()),
        ("Multi-layer Perceptron", MLPClassifier(max_iter=1000)),
        ("AdaBoost", AdaBoostClassifier()),
        ("Extra Trees", ExtraTreesClassifier()),
        ("Ridge Classifier", RidgeClassifier()),
        ("Quadratic Discriminant Analysis", QuadraticDiscriminantAnalysis()),
        ("CatBoost", CatBoostClassifier(verbose=0, random_seed=42)),
        ("Balanced Random Forest", BalancedRandomForestClassifier()),
        ("Linear Discriminant Analysis", LinearDiscriminantAnalysis()),
        ("Nearest Centroid Classifier", NearestCentroid()),
        ("Passive Aggressive Classifier", PassiveAggressiveClassifier()),
        ("Perceptron", Perceptron()),
        ("Bernoulli Naive Bayes", BernoulliNB()),
        ("Bagging Classifier", BaggingClassifier()),
        # Add a base estimator for StackingClassifier
        ("Stacking Classifier", StackingClassifier(estimators=[('lr', LogisticRegression()), ('dt', DecisionTreeClassifier())])),
    ]


    best_model = None
    best_accuracy = -1
    best_model_instance = None

    for name, model in models:
        model.fit(df_X_train, df_y_train)
        y_pred_binary = model.predict(df_X_test)

        if name in ["Isolation Forest", "One-Class SVM", "K-Means"]:
            y_pred_binary = np.where(y_pred_binary == -1, 0, y_pred_binary)

        print(name + " Model:")
        confusion_matrix = metrics.confusion_matrix(df_y_test, y_pred_binary)
        print("Confusion Matrix:")
        print(confusion_matrix)

        accuracy = metrics.accuracy_score(df_y_test, y_pred_binary)
        precision = metrics.precision_score(df_y_test, y_pred_binary)
        recall = metrics.recall_score(df_y_test, y_pred_binary)
        classification_report = metrics.classification_report(df_y_test, y_pred_binary)

        print("Accuracy:", accuracy)
        print("Precision:", precision)
        print("Recall:", recall)
        print(classification_report)

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = name
            best_model_instance = model

    print("The best model is:", best_model, "with an accuracy of", best_accuracy)

    # Print the confusion matrix for the best model
    y_pred_best = best_model_instance.predict(df_X_test)
    if best_model in ["Isolation Forest", "One-Class SVM", "K-Means"]:
        y_pred_best = np.where(y_pred_best == -1, 0, y_pred_best)
    print("Confusion Matrix of the best model:")
    print(metrics.confusion_matrix(df_y_test, y_pred_best))