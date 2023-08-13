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

            data = pd.read_csv(self.dataset, header=0, delimiter=",", na_filter=True, index_col=False)
            
            # print(data.columns.values)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            # print(data.describe())

            # Remove columns with only 0
            # https://stackoverflow.com/questions/21164910/how-do-i-delete-a-column-that-contains-only-zeros-in-pandas
            data = data.loc[:, (data != 0).any(axis=0)]
            print(data.describe())

            y = data['id']
            X = data.drop(columns=['id', 't']) 
            print(X.columns.values)
            
            # normalizar 
            X_normalized = preprocessing.normalize(X, norm='l1')
            # X_normalized = X
            transformer = preprocessing.MaxAbsScaler().fit(X) 
            # X_normalized = transformer.transform(X)
            
            transformer = preprocessing.MinMaxScaler().fit(X)
            # X_normalized = transformer.transform(X)

            transformer = RobustScaler().fit(X)
            X_normalized = transformer.transform(X)

            X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.5, random_state=42, shuffle=True)
            return X_train, X_test, y_train, y_test, X_normalized, y
        except Exception as e:
            print("read_data: ", e)

    def main(self):
        X_train, X_test, y_train, y_test, X, y = self.read_data()
        
        rfc = RandomForestClassifier(class_weight='balanced', random_state=42, max_depth=3, min_samples_split=2)
        rfc.fit(X_train, y_train)
        y_pred_rfc = rfc.predict(X_test)
        y_score_rfc = rfc.predict_proba(X_test)[:,1:]
        
        self.get_score_clf("rfc", y_test, y_pred_rfc, y_score_rfc)
        # https://stackoverflow.com/questions/49055410/confusion-matrix-too-many-values-to-unpack
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred_rfc).ravel()
        print("CV: tn", tn, "fp", fp, "fn", fn, "tp", tp)

        # https://stackoverflow.com/questions/38151615/specific-cross-validation-with-random-forest
        # rfc_1 = RandomForestClassifier(class_weight='balanced', random_state=42)
        # print(cross_val_score(rfc_1, X, y, cv=10))

        xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=4)
        xgb.fit(X_train, y_train)
        y_pred_xgb = xgb.predict(X_test)
        y_score_xgb = xgb.predict_proba(X_test)[:,1:]
        self.get_score_clf("xgb", y_test, y_pred_xgb, y_score_xgb)

        # xgb_1 = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
        # print(cross_val_score(xgb_1, X, y, cv=10))

        dtc = DecisionTreeClassifier(class_weight='balanced', random_state=42)
        dtc.fit(X_train, y_train)
        y_pred_dtc = dtc.predict(X_test)
        y_score_dtc = dtc.predict_proba(X_test)[:,1:]
        self.get_score_clf("dtc", y_test, y_pred_dtc, y_score_dtc)

        # dtc_1 = DecisionTreeClassifier(class_weight='balanced', random_state=42)
        # print(cross_val_score(dtc_1, X, y, cv=10))

        nuclf = NuSVC(probability=True, random_state=42)
        nuclf.fit(X_train, y_train)
        y_pred_nuclf = nuclf.predict(X_test)
        y_score_nuclf = nuclf.predict_proba(X_test)[:,1:]
        self.get_score_clf("nusvc", y_test, y_pred_nuclf, y_score_nuclf)

        # lsvc = RadiusNeighborsClassifier(radius=2.0)
        # lsvc.fit(X_train, y_train)
        # y_pred_lsvc = lsvc.predict(X_test)
        # y_score_lsvc = lsvc.predict_proba(X_test)[:,1:]
        # self.get_score_clf("rnc", y_test, y_pred_lsvc, y_score_lsvc)

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
