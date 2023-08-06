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
    
    
def find_best_model_regression(df_X_train, df_X_test, df_y_train, df_y_test):
    
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, BayesianRidge, SGDRegressor
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor, ExtraTreesRegressor, BaggingRegressor
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.neural_network import MLPRegressor
    from xgboost import XGBRegressor
    from lightgbm import LGBMRegressor
    from catboost import CatBoostRegressor
    from sklearn import metrics

    models = [
        ("Linear Regression", LinearRegression()),
        ("Ridge Regression", Ridge()),
        ("Lasso Regression", Lasso()),
        ("ElasticNet Regression", ElasticNet()),
        ("Bayesian Ridge Regression", BayesianRidge()),
        ("Decision Tree Regressor", DecisionTreeRegressor()),
        ("Random Forest Regressor", RandomForestRegressor()),
        ("Gradient Boosting Regressor", GradientBoostingRegressor()),
        ("XGBoost Regressor", XGBRegressor(eval_metric="rmse")),
        ("LightGBM Regressor", LGBMRegressor()),
        ("Support Vector Regressor", SVR()),
        ("K-Nearest Neighbors Regressor", KNeighborsRegressor()),
        ("Multi-layer Perceptron Regressor", MLPRegressor(max_iter=1000)),
        ("AdaBoost Regressor", AdaBoostRegressor()),
        ("Extra Trees Regressor", ExtraTreesRegressor()),
        ("Stochastic Gradient Descent Regressor", SGDRegressor()),
        ("Bagging Regressor", BaggingRegressor()),
        ("CatBoost Regressor", CatBoostRegressor(verbose=0, random_seed=42)),
    ]

    best_model = None
    best_mse = float("inf")
    best_model_instance = None

    for name, model in models:
        model.fit(df_X_train, df_y_train)
        y_pred = model.predict(df_X_test)

        print(name + " Model:")
        mse = metrics.mean_squared_error(df_y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = metrics.r2_score(df_y_test, y_pred)

        print("Mean Squared Error:", mse)
        print("Root Mean Squared Error:", rmse)
        print("R-squared:", r2)
        print()

        if mse < best_mse:
            best_mse = mse
            best_model = name
            best_model_instance = model

    print("The best model is:", best_model, "with a Mean Squared Error of", best_mse)

    # Print the metrics for the best model
    y_pred_best = best_model_instance.predict(df_X_test)
    best_rmse = np.sqrt(best_mse)
    best_r2 = metrics.r2_score(df_y_test, y_pred_best)
    print("Metrics of the best model:")
    print("Mean Squared Error:", best_mse)
    print("Root Mean Squared Error:", best_rmse)
    print("R-squared:", best_r2)


def find_best_clustering_algorithm(data, scaling=True, n_clusters=None, visualize=True, test_feature_combinations=False):
    from sklearn.cluster import estimate_bandwidth
    import itertools
    if scaling:
        scaler = StandardScaler()
        data = scaler.fit_transform(data)
    
    if test_feature_combinations:
        print("\nTesting different feature combinations:")
        for num_features in range(1, data.shape[1] + 1):
            for feature_combination in itertools.combinations(range(data.shape[1]), num_features):
                reduced_data = data[:, feature_combination]
                _, _, score = find_best_clustering_algorithm(reduced_data, scaling=False, n_clusters=n_clusters, visualize=False)
                print(f"Silhouette score for features {feature_combination}: {score}")

    clustering_algorithms = [
        ("KMeans", KMeans(n_clusters=n_clusters) if n_clusters else KMeans()),
        ("MiniBatchKMeans", MiniBatchKMeans(n_clusters=n_clusters) if n_clusters else MiniBatchKMeans()),
        ("AffinityPropagation", AffinityPropagation()),
        ("MeanShift", MeanShift(bandwidth=estimate_bandwidth(data, n_samples=n_clusters)) if n_clusters else MeanShift()),
        ("SpectralClustering", SpectralClustering(n_clusters=n_clusters) if n_clusters else SpectralClustering()),
        ("AgglomerativeClustering", AgglomerativeClustering(n_clusters=n_clusters) if n_clusters else AgglomerativeClustering()),
        ("DBSCAN", DBSCAN()),
        ("OPTICS", OPTICS()),
        ("Birch", Birch(n_clusters=n_clusters) if n_clusters else Birch()),
        ("GaussianMixture", GaussianMixture(n_components=n_clusters) if n_clusters else GaussianMixture())
    ]
    
    best_algorithm = None
    best_algorithm_name = ""
    best_score = -np.inf

    for name, algorithm in clustering_algorithms:
        try:
            if isinstance(algorithm, GaussianMixture):
                algorithm.fit(data)
                labels = algorithm.predict(data)
            else:
                labels = algorithm.fit_predict(data)

            if len(np.unique(labels)) > 1:
                score = silhouette_score(data, labels)
                print(f"{name} Algorithm:")
                print("Silhouette Score:", score)
                if score > best_score:
                    best_score = score
                    best_algorithm = algorithm
                    best_algorithm_name = name
        except Exception as e:
            print(f"An error occurred while processing {name}: {e}")

    print("The best clustering algorithm is:", best_algorithm_name, "with a silhouette score of", best_score)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(data)

    # Get cluster labels using the best clustering model
    if isinstance(best_algorithm, GaussianMixture):
        best_algorithm.fit(data)
        cluster_labels = best_algorithm.predict(data)
    else:
        cluster_labels = best_algorithm.fit_predict(data)

    # Create a scatter plot with different colors for each cluster
    plt.figure(figsize=(10, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_labels, cmap='viridis', edgecolors='k', s=50)

    plt.title('Scatter Plot for the Best Clustering Model: ' + best_algorithm_name)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.show()
    return best_algorithm_name, best_algorithm, best_score
