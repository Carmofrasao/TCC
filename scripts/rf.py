#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import numpy as np
    import pandas as pd
    import sys
    import argparse
    import re

    from xgboost import XGBRegressor, XGBClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
    from sklearn.tree import DecisionTreeClassifier, export_graphviz
    from sklearn import tree
    from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
    from sklearn.svm import SVC, NuSVC, LinearSVC
    from sklearn.linear_model import SGDClassifier

    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer, HashingVectorizer
    from sklearn import metrics
    from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
    from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, f1_score, balanced_accuracy_score, confusion_matrix, brier_score_loss

    from sklearn.model_selection import cross_val_score
    from sklearn import preprocessing
    from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, OneHotEncoder, OrdinalEncoder, RobustScaler

    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression

    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

except Exception as e:
    print('Unmet dependency:', e)
    sys.exit(1)

class Main():
    """
    python3 rf.py --dataset map_calls_dataset.csv
    """

    def __init__(self, dataset):
        self.dataset = dataset

    def get_score_clf(self, name, y_test, y_pred, y_score):
        try:
            print(name, \
                  "ROC", round(roc_auc_score(y_test, y_score), 4), \
                  "precision", round(precision_score(y_test, y_pred), 4), \
                  "recall", round(recall_score(y_test, y_pred), 4), \
                  "f1", round(f1_score(y_test, y_pred), 4), \
                  "accuracy", round(accuracy_score(y_test, y_pred), 4), \
                  "bac", round(balanced_accuracy_score(y_test, y_pred), 4) , \
                  "brier", round(brier_score_loss(y_test, y_pred), 4)
                  )

            tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
            print("tn", tn, "fp", fp, "fn", fn, "tp", tp)

        except Exception as e:
            print("get_score_clf", e)

    def read_data(self):
        try:
            # find . -type f -print0 | xargs -0 wc -l | sort -n
            # get files with more calls

            data = pd.read_csv(self.dataset, header=0, delimiter=",", na_filter=True, index_col=0)
            # print(data.columns.values)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            # print(data.describe())

            # Remove columns with only 0
            # https://stackoverflow.com/questions/21164910/how-do-i-delete-a-column-that-contains-only-zeros-in-pandas
            data = data.loc[:, (data != 0).any(axis=0)]
            # print(data.describe())

            y = data['t']
            X = data.drop(columns=['t'])
            # print(X.columns.values)

            # normalizar
            X_normalized = preprocessing.normalize(X, norm='l1')
            # X_normalized = X
            transformer = preprocessing.MaxAbsScaler().fit(X)
            # X_normalized = transformer.transform(X)

            transformer = preprocessing.MinMaxScaler().fit(X)
            # X_normalized = transformer.transform(X)

            # transformer = RobustScaler().fit(X)
            X_normalized = transformer.transform(X)

            X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.5, random_state=42, shuffle=True)
            return X_train, X_test, y_train, y_test, X_normalized, y
        except Exception as e:
            print("read_data: ", e)

    def grid_search_classifier(self, classifier_name, classifier, param_grid, X_train, y_train, X_test, y_test):
        # print('Fazendo pesquisa exaustiva sobre valores de parâmetros especificados para um estimador.')
        grid_search = GridSearchCV(classifier, param_grid, cv=5, scoring='f1')
        # print('Ajustando todos os conjuntos de parâmetros.')
        grid_search.fit(X_train, y_train)

        # print("Melhores parâmetros para", classifier_name, ":", grid_search.best_params_)
        # print("Melhor pontuação para", classifier_name, ":", grid_search.best_score_)

        best_classifier = grid_search.best_estimator_
        best_classifier.fit(X_train, y_train)
        y_pred = best_classifier.predict(X_test)
        y_score = best_classifier.predict_proba(X_test)[:,1:]
        self.get_score_clf(classifier_name, y_test, y_pred, y_score)

    def main(self):
        X_train, X_test, y_train, y_test, X, y = self.read_data()

        # Essa parte:
        print('Otimizado')

        # RandomForestClassifier
        # rfc ROC 0.9634 precision 0.9167 recall 0.898 f1 0.9072 accuracy 0.91 bac 0.9098 brier 0.09
        rfc_param_grid = {
            'n_estimators': [65],
            'criterion': ['entropy'],
            'max_depth': [10],
            'min_samples_split': [3],
            'min_samples_leaf': [2],
            'min_weight_fraction_leaf': [0.0],
            'max_features': ['sqrt'],
            'max_leaf_nodes': [25],
            'min_impurity_decrease': [0.0],
            'bootstrap': [False],
            'n_jobs': [-1],
            'random_state': [None],
            'class_weight': ['balanced_subsample'],
            'max_samples': [None],
        }
        self.grid_search_classifier("rfc", RandomForestClassifier(), rfc_param_grid, X_train, y_train, X_test, y_test)

        # XGBClassifier
        # xgb ROC 0.9748 precision 0.8654 recall 0.9184 f1 0.8911 accuracy 0.89 bac 0.8906 brier 0.11
        xgb_param_grid = {
            'learning_rate': [0.5],
            'max_depth': [8],
            'min_child_weight': [1],
            'subsample': [0.7],
            'colsample_bytree': [0.5],
            'n_estimators': [65],
            'base_score': [0.1],
            'colsample_bylevel': [1],
            'gamma': [0],
            'max_delta_step': [0],
            'missing': [5],
            'nthread': [-1],
            'objective': ['binary:logistic'],
            'reg_alpha': [0],
            'reg_lambda': [5],
            'scale_pos_weight': [5],
            'seed': [2],
        }
        self.grid_search_classifier("xgb", XGBClassifier(), xgb_param_grid, X_train, y_train, X_test, y_test)

        # DecisionTreeClassifier
        # dtc ROC 0.8603 precision 0.8571 recall 0.8571 f1 0.8571 accuracy 0.86 bac 0.8599 brier 0.14
        dtc_param_grid = {
            'criterion': ['log_loss'],
            'splitter': ['random'],
            'max_depth': [8],
            'min_samples_split': [2],
            'min_samples_leaf': [1],
            'min_weight_fraction_leaf': [0.0],
            'max_features': ['log2'],
            'random_state': [None],
            'max_leaf_nodes': [25],
            'min_impurity_decrease': [0.0],
            'class_weight': ['balanced'],
            'ccp_alpha': [0.0],
        }
        self.grid_search_classifier("dtc", DecisionTreeClassifier(), dtc_param_grid, X_train, y_train, X_test, y_test)

        # NuSVC
        # nusvc ROC 0.8647 precision 0.8478 recall 0.7959 f1 0.8211 accuracy 0.83 bac 0.8293 brier 0.17
        nuclf_param_grid = {
            'nu': [0.5],
            'kernel': ['poly'],
            'degree': [1],
            'gamma': ['scale'],
            'coef0': [0.0],
            'shrinking': [True],
            'probability': [True],
            'tol': [0.0001],
            'cache_size': [0, 1],
            'class_weight': ['balanced'],
            'break_ties': [True],
            'random_state': [None]
        }
        self.grid_search_classifier("nusvc", NuSVC(), nuclf_param_grid, X_train, y_train, X_test, y_test)

        # MLPClassifier
        # mlpc ROC 0.948 precision 0.9762 recall 0.8367 f1 0.9011 accuracy 0.91 bac 0.9086 brier 0.09
        mlpc_param_grid = {
            'hidden_layer_sizes': [(50,)],
            'activation': ['logistic'],
            'solver': ['lbfgs'],
            'batch_size': ['auto'],
            'learning_rate': ['invscaling'],
            'max_iter': [100000],
            'shuffle': [True],
            'random_state': [None],
            'nesterovs_momentum': [True],
            'early_stopping': [True],
            'validation_fraction': [0.3],
            'beta_1': [0.7],
            'beta_2': [0.999],
        }
        self.grid_search_classifier("mlpc", MLPClassifier(), mlpc_param_grid, X_train, y_train, X_test, y_test)

        # AdaBoostClassifier
        # ab ROC 0.9768 precision 0.9348 recall 0.8776 f1 0.9053 accuracy 0.91 bac 0.9094 brier 0.09
        ab_param_grid = {
            'estimator': [None],
            'n_estimators': [150],
            'learning_rate': [1.5],
            'algorithm': ['SAMME'],
            'random_state': [42]
        }
        self.grid_search_classifier("ab", AdaBoostClassifier(), ab_param_grid, X_train, y_train, X_test, y_test)

        # SGDClassifier
        # sgdc ROC 0.8856 precision 0.8302 recall 0.898 f1 0.8627 accuracy 0.86 bac 0.8607 brier 0.14
        sgdc_param_grid = {
            'loss': ['modified_huber'],
            'penalty': [None],
            'alpha': [0.001],
            'l1_ratio': [0.1],
            'fit_intercept': [False],
            'max_iter': [1000],
            'tol': [0.0000001],
            'shuffle': [True],
            'epsilon': [0.01],
            'n_jobs': [-1],
            'random_state': [None],
            'learning_rate': ['optimal'],
            'power_t': [0.0],
            'early_stopping': [True],
            'validation_fraction': [0.3],
            'n_iter_no_change': [5],
        }
        self.grid_search_classifier("sgdc", SGDClassifier(), sgdc_param_grid, X_train, y_train, X_test, y_test)

        # Substitue essa:
        print("Original")

        rfc = RandomForestClassifier(class_weight='balanced', random_state=42, max_depth=3, min_samples_split=2)
        rfc.fit(X_train, y_train)
        y_pred_rfc = rfc.predict(X_test)
        y_score_rfc = rfc.predict_proba(X_test)[:,1:]
        self.get_score_clf("rfc", y_test, y_pred_rfc, y_score_rfc)

        xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=4)
        xgb.fit(X_train, y_train)
        y_pred_xgb = xgb.predict(X_test)
        y_score_xgb = xgb.predict_proba(X_test)[:,1:]
        self.get_score_clf("xgb", y_test, y_pred_xgb, y_score_xgb)

        dtc = DecisionTreeClassifier(class_weight='balanced', random_state=42)
        dtc.fit(X_train, y_train)
        y_pred_dtc = dtc.predict(X_test)
        y_score_dtc = dtc.predict_proba(X_test)[:,1:]
        self.get_score_clf("dtc", y_test, y_pred_dtc, y_score_dtc)

        nuclf = NuSVC(probability=True, random_state=42)
        nuclf.fit(X_train, y_train)
        y_pred_nuclf = nuclf.predict(X_test)
        y_score_nuclf = nuclf.predict_proba(X_test)[:,1:]
        self.get_score_clf("nusvc", y_test, y_pred_nuclf, y_score_nuclf)

        mlpc = MLPClassifier(random_state=42, max_iter=100)
        mlpc.fit(X_train, y_train)
        y_pred_mlpc = mlpc.predict(X_test)
        y_score_mlpc = mlpc.predict_proba(X_test)[:,1:]
        self.get_score_clf("mlpc", y_test, y_pred_mlpc, y_score_mlpc)

        ab = AdaBoostClassifier(random_state=42)
        ab.fit(X_train, y_train)
        y_pred_ab = ab.predict(X_test)
        y_score_ab = ab.predict_proba(X_test)[:,1:]
        self.get_score_clf("ab", y_test, y_pred_ab, y_score_ab)

        sgdc = SGDClassifier(max_iter=1000, loss='modified_huber', random_state=42)
        sgdc.fit(X_train, y_train)
        y_pred_sgdc = sgdc.predict(X_test)
        y_score_sgdc = sgdc.predict_proba(X_test)[:,1:]
        self.get_score_clf("sgdc", y_test, y_pred_sgdc, y_score_sgdc)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='.')
    parser.add_argument('--version', '-v', '-vvv', '-version', action='version', version=str('Base 2.1'))
    parser.add_argument('--dataset', type=str, required=True, help='This option define the dataset.')

    # get args
    args = parser.parse_args()
    kwargs = {
        'dataset': args.dataset
    }

    args = parser.parse_args()

    try:
        worker = Main(**kwargs)
        worker.main()
    except KeyboardInterrupt as e:
        print('Exit using ctrl^C')
