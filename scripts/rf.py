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
        print('Fazendo pesquisa exaustiva sobre valores de parâmetros especificados para um estimador.')
        grid_search = GridSearchCV(classifier, param_grid, cv=5, scoring='f1')
        print('Ajuste com todos os conjuntos de parâmetros.')
        grid_search.fit(X_train, y_train)

        print("Melhores parâmetros para", classifier_name, ":", grid_search.best_params_)
        print("Melhor pontuação para", classifier_name, ":", grid_search.best_score_)

        best_classifier = grid_search.best_estimator_
        best_classifier.fit(X_train, y_train)
        y_pred = best_classifier.predict(X_test)
        y_score = best_classifier.predict_proba(X_test)[:,1:]
        self.get_score_clf(classifier_name, y_test, y_pred, y_score)

    def main(self):
        X_train, X_test, y_train, y_test, X, y = self.read_data()

        # Essa parte:
        print('Otimizado')

        # Variaveis de RandomForestClassifier:
        # n_estimators -------------> O número de árvores na floresta.
        # criterion ----------------> A função para medir a qualidade de uma divisão.
        # max_depth ----------------> A profundidade máxima da árvore.
        # min_samples_split --------> O número mínimo de amostras necessárias para dividir um nó interno.
        # min_samples_leaf ---------> O número mínimo de amostras necessárias para estar em um nó folha.
        # min_weight_fraction_leaf -> A fração ponderada mínima da soma total dos pesos (de todas as amostras de entrada) necessária para estar em um nó folha.
        # max_features -------------> O número de características a considerar quando se procura o melhor split.
        # max_leaf_nodes -----------> Cultivar árvores com max_leaf_nodes da melhor forma possível.
        # min_impurity_decrease ----> Um nó será dividido se esta divisão induzir uma diminuição da impureza maior ou igual a este valor.
        # bootstrap ----------------> Se as amostras bootstrap são utilizadas na construção de árvores.
        # n_jobs -------------------> O número de trabalhos a executar em paralelo.
        # random_state -------------> Controla a aleatoriedade do bootstrapping das amostras utilizadas na construção de árvores (se bootstrap=True) e a amostragem das características a considerar ao procurar a melhor divisão em cada nó (se max_features < n_features).
        # class_weight -------------> Pesos associados às classes na forma {class_label: weight}.
        # max_samples --------------> Se bootstrap for Verdadeiro, o número de amostras a retirar de X para treinar cada estimador de base.

        # RandomForestClassifier
        rfc_param_grid = {
            'n_estimators': [50, 75],
            'criterion': ['gini', 'entropy', 'log_loss'],
            'max_depth': [None, 1, 50],
            'min_samples_split': [2, 25],
            'min_samples_leaf': [1, 25],
            'min_weight_fraction_leaf': [0.1, 0.25],
            'max_features': ['sqrt', 'log2', None],
            'max_leaf_nodes': [1, 25],
            'min_impurity_decrease': [0.1, 0.25],
            'bootstrap': [True, False],
            'n_jobs': [-1],
            'random_state': [None, 1, 25],
            'class_weight': ['balanced', 'balanced_subsample'],
            'max_samples': [1, 25],
        }
        # Esses valores são bons, mas tem poucos parametros
        #rfc_param_grid = {
        #    'max_depth': [None],
        #    'min_samples_leaf': [1],
        #    'min_samples_split': [2],
        #    'n_estimators': [50]
        #}
        self.grid_search_classifier("rfc", RandomForestClassifier(), rfc_param_grid, X_train, y_train, X_test, y_test)
        exit(1)
        # XGBClassifier
        xgb_param_grid = {
            'learning_rate': [0.3],
            'max_depth': [1],
            'min_child_weight': [1],
            'subsample': [0.7],
            'colsample_bytree': [0.1],
            'n_estimators': [100]
        }
        self.grid_search_classifier("rfc", RandomForestClassifier(class_weight='balanced', random_state=42, max_depth=3, min_samples_split=2), rfc_param_grid, X_train, y_train, X_test, y_test)

        # XGBClassifier
        xgb_param_grid = {
            'learning_rate': [0.3],
            'max_depth': [1],
            'min_child_weight': [1],
            'subsample': [0.7],
            'colsample_bytree': [0.1],
            'n_estimators': [100]
        }
        self.grid_search_classifier("xgb", XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=4), xgb_param_grid, X_train, y_train, X_test, y_test)

        # DecisionTreeClassifier
        dtc_param_grid = {
            'max_depth': [None],
            'min_samples_split': [2],
            'min_samples_leaf': [2]
        }
        self.grid_search_classifier("dtc", DecisionTreeClassifier(class_weight='balanced', random_state=42), dtc_param_grid, X_train, y_train, X_test, y_test)

        # NuSVC
        nuclf_param_grid = {
            'kernel': ['linear'],
            'gamma': ['auto'],
        }
        self.grid_search_classifier("nusvc", NuSVC(probability=True, random_state=42), nuclf_param_grid, X_train, y_train, X_test, y_test)

        # MLPClassifier
        mlpc_param_grid = {
            'activation': ['relu'],
            'alpha': [0.00001],
            'hidden_layer_sizes': [(50, 50, 50)],
            'learning_rate': ['constant'],
            'solver': ['sgd']
        }
        self.grid_search_classifier("mlpc", MLPClassifier(random_state=42, max_iter=10000), mlpc_param_grid, X_train, y_train, X_test, y_test)

        # AdaBoostClassifier
        ab_param_grid = {
            'algorithm': ['SAMME'],
            'learning_rate': [1.5],
            'n_estimators': [150]
        }
        self.grid_search_classifier("ab", AdaBoostClassifier(random_state=42), ab_param_grid, X_train, y_train, X_test, y_test)

        # SGDClassifier
        sgdc_param_grid = {
            'alpha': [0.00004],
            'eta0': [0.04],
            'learning_rate': ['constant'],
            'loss': ['modified_huber']
        }
        self.grid_search_classifier("sgdc", SGDClassifier(max_iter=1000, loss='modified_huber', random_state=42), sgdc_param_grid, X_train, y_train, X_test, y_test)

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
