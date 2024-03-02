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
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier, export_graphviz
    from sklearn import tree
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC

    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer, HashingVectorizer
    from sklearn import metrics
    from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
    from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, f1_score, plot_confusion_matrix, balanced_accuracy_score

    from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, OneHotEncoder, OrdinalEncoder

    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression

    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

except Exception as e:
    print('Unmet dependency:', e)
    sys.exit(1)

class Titanic(object):
    """
        Titanic code: https://www.kaggle.com/c/spaceship-titanic/overview

        Run code using:
        python3 main.py --dataset-train ../data/train.csv --dataset-test ../data/test.csv > out.csv

    """
    def __init__(self, dataset_train, dataset_test):
        self.datasetTrain = dataset_train
        self.datasetTest = dataset_test

       ## Config ##
        self.testSize = 0.5
        self.randomState = 42

    def read_data(self, file1, file2):
        try:
            df1 = pd.read_csv(file1, header=0, delimiter=",", na_filter=True)
            df2 = pd.read_csv(file2, header=0, delimiter=",", na_filter=True)

            return df1, df2
        except Exception as e:
            print("read_data: ", e)

    def get_score_clf(self, y_test, y_pred, y_score):
        try:
                return round(roc_auc_score(y_test, y_score), 4), \
                   round(precision_score(y_test, y_pred), 4), \
                   round(recall_score(y_test, y_pred), 4), \
                   round(f1_score(y_test, y_pred), 4), \
                   round(accuracy_score(y_test, y_pred), 4), \
                   round(balanced_accuracy_score(y_test, y_pred), 4)
        except Exception as e:
            print("get_score_clf", e)

    def convert_name(self, df):
        try:
            names = []

            for each_name in df['Name']:
                new_string = str(each_name).split(" ")
                names.append(new_string[-1])

            df = df.drop(['Name'], 1)
            dfnames = pd.DataFrame(names, columns=['Names'])

            result = pd.concat([df, dfnames], axis=1)
            return result
        except Exception as e:
            print("convert_name",e)

    def convert_ticket(self, df):
        try:
            ticket_name = []
            ticket_location = []
            for each_ticket in df['Ticket']:
                # use only characteres
                word1 = " ".join(re.findall("[a-zA-Z]+", each_ticket))
                # print(each_ticket, "||", word1.replace(" ","").lower())
                ticket_location.append(word1.replace(" ","").lower())

                # use only numbers
                word2 = " ".join(re.findall("[0-9]+", each_ticket))
                # print(each_ticket, "||", word2.split(" ")[-1])
                ticket_name.append(word2.split(" ")[-1])

            df = df.drop(['Ticket'], 1)
            dfticket = pd.DataFrame(ticket_name, columns=['Ticket'])
            dflocation = pd.DataFrame(ticket_location, columns=['Location'])
            result = pd.concat([df, dfticket, dflocation], axis=1)

            return result
        except Exception as e:
            print("convert_ticket",e)

    def convert_cabin(self, df):
        try:
            deck = []
            num =[]
            side = []
            df['Cabin'].fillna(" / / ",inplace=True)
            for each_cabin in df['Cabin']:
                new = each_cabin.split("/")

                deck.append(str(new[0]))
                num.append(str(new[1]))
                side.append(str(new[2]))

            df = df.drop(['Cabin'], 1)
            dfDeck = pd.DataFrame(deck, columns=['NewDeck'])
            dfNum = pd.DataFrame(num, columns=['NewNum'])
            dfSide = pd.DataFrame(side, columns=['NewSide'])

            result = pd.concat([df, dfDeck, dfNum, dfSide], axis=1)
            return result
        except Exception as e:
            print("convert_cabin", e)

    def group_pass(self, df):
        try:
            NumberGroups = []
            Groups = []
            for each_passID in df['PassengerId']:
                split_string = each_passID.split("_")
                NumberGroups.append(split_string[-1])
                Groups.append(split_string[0])

            dfNumberGroups = pd.DataFrame(NumberGroups, columns=['NumberGroups'])
            dfGroups = pd.DataFrame(Groups, columns=['Groups'])
            result = pd.concat([df, dfGroups, dfNumberGroups], axis=1)
            return result
        except Exception as e:
            print("group_pass", e)

    def billed(self, df):
        try:
            dfBilled = pd.DataFrame(df['RoomService'] + df ['FoodCourt'] + df['ShoppingMall'] + df['Spa'] + df['VRDeck'], columns=['Billed'])
            result = pd.concat([df, dfBilled], axis=1)
            return result
        except Exception as e:
            print("billed", e)

    def convert_data(self, train, test):
        try:
            # get label y: Transported
            y_train = train['Transported']
            y_test = []

            # get group from PassengerId
            train = self.group_pass(train)
            test = self.group_pass(test)

            # Add sum billed
            train = self.billed(train)
            test = self.billed(test)

            # Convert ticket
            #train = self.convert_ticket(train)
            #test = self.convert_ticket(test)

            # Convert cabin
            train = self.convert_cabin(train)
            test = self.convert_cabin(test)

            # Convert names (Just using last name)
            train = self.convert_name(train)
            test = self.convert_name(test)

            # print(train)
            # drop: PassengerId
            X_train = train.drop(['PassengerId', 'Transported'], 1)
            X_test = test.drop(['PassengerId'], 1)

            return X_train, y_train, X_test, y_test

        except Exception as e:
            print("convert_data: ", e)

    def multilayerPerceptron(self, X_train, X_test, y_train):
        try:
            clf = MLPClassifier(random_state=42)
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            return y_pred
        except Exception as a:
            print('multilayerPerceptron', a)

    def get_without_na(self, df):
        newDf = df[df.isnull().any(axis=1)]
        return newDf

    def object_to_category(self, df, column):
        try:
            for each_column in column:
                # Change to categorical
                df[str(each_column)] = df[str(each_column)].astype('category')
                # convert category two int representation
                df["categorical_"+str(each_column)] = df[str(each_column)].cat.codes
            df = df.drop(column, 1)
            return df
        except Exception as e:
            print("object to category", e)

    def for_each_column(self, df):
        try:
            # get '' to NaN
            # df = df.replace(np.nan, '', regex=True)

            header = df.head()
            for each in header:
                # df = df[each].fillna(df[each].mode(), inplace=True)
                df = df[each].fillna("")
            return df
        except Exception as e:
            print("for_each_column", e)

    def main(self):
        print("Build data")
        df_train, df_test = self.read_data(self.datasetTrain, self.datasetTest)

        ## Fix NaN, na, and empty values
        # drop lines with nan
        #df_train = self.get_without_na(df_train)
        #df_test = self.get_without_na(df_test)
        # or replace (https://pbpython.com/categorical-encoding.html)
        #df_train = self.for_each_column(df_train)
        #df_test = self.for_each_column(df_test)

        # Convert and create new columns (In this case y_test will be empty because we are not using the validation set in this problem)
        X_train, y_train, X_test, y_test = self.convert_data(df_train, df_test)

        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None)
        # print(X_train.iloc[1])
        # print(X_train)

        # change enconding (esta errado, pq devo trocar ao mesmo tempo. Grupos podem estar faltando em um conjunto de dados)
        # print(X_train.info())
        #X_train = self.object_to_category(X_train, ['HomePlanet','CryoSleep','Destination','VIP','NewDeck','NewNum','NewSide','Names'])
        #X_test = self.object_to_category(X_test, ['HomePlanet','CryoSleep','Destination','VIP','NewDeck','NewNum','NewSide','Names'])
        # print(X_train.dtypes) #(use csv_evaluation for more information about the dataset)

        # self.test_many(X_train, y_train)
        self.train_case(df_test, X_train, X_test, y_train, y_test)
        #self.grid_train_case(df_test, X_train, X_test, y_train, y_test)

    def grid_train_case(self, df_test, X_train_org, X_test_org, y_train_org, y_test_org):
        # https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html
        # print(X_train.info())

        # Transform Numerical Columns
        numeric_features = ["Age", "RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck", "Billed"]
        numeric_transformer_0 = Pipeline(
                steps=[
                    ("si", SimpleImputer(strategy="mean")), #Fix NaN, Inf
                    ("sc", StandardScaler()),
                    ]
                )
        numeric_transformer_1 = Pipeline(
                steps=[
                    ("si", SimpleImputer(strategy="mean")),
                    ("mm", MinMaxScaler()),
                    ]
                )
        numeric_transformer_2 = Pipeline(
                steps=[
                    ("si", SimpleImputer(strategy="mean")),
                    ("mas", MaxAbsScaler()),
                    ]
                )

        # Transform Categorical Columns
        categorical_features = ["HomePlanet", "CryoSleep", "Destination", "VIP", "Groups", "NewDeck", "NewNum", "NewSide", "Names"]
        categorical_transformer_0 = Pipeline(
                steps=[
                    ("ohe", OneHotEncoder(handle_unknown="ignore")),
                    ]
                )
        categorical_transformer_1 = Pipeline(
                steps=[
                    ("oe", OrdinalEncoder()), # OrdinalEncoder doesn't allow NaN
                    ]
                )

        # define the preprocessor
        preprocessor_0 = ColumnTransformer(
                transformers=[
                    ("num", numeric_transformer_0, numeric_features),
                    ("cat", categorical_transformer_0, categorical_features),
                    ]
                )
        preprocessor_1 = ColumnTransformer(
                transformers=[
                    ("num", numeric_transformer_1, numeric_features),
                    ("cat", categorical_transformer_0, categorical_features),
                    ]
                )
        preprocessor_2 = ColumnTransformer(
                transformers=[
                    ("num", numeric_transformer_2, numeric_features),
                    ("cat", categorical_transformer_0, categorical_features),
                    ]
                )

        # Pipeline for each alg.
        lr_pipe_0 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_0),
                    ("classifier", LogisticRegression())
                    ]
                )
        lr_pipe_1 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_1),
                    ("classifier", LogisticRegression())
                ]
                )
        lr_pipe_2 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_2),
                    ("classifier", LogisticRegression())
                ]
                )
        lr_param_grid = {
                "preprocessor__num__si__strategy": ["mean", "median"],
                "classifier__max_iter": [200, 500, 1000],
                "classifier__C": [0.1, 1.0, 10, 100],
                }

        svm_pipe_0 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_0),
                    ("classifier", SVC())
                    ]
                )
        svm_pipe_1 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_1),
                    ("classifier", SVC())
                    ]
                )
        svm_pipe_2 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_2),
                    ("classifier", SVC())
                    ]
                )
        svm_param_grid = {
                "preprocessor__num__si__strategy": ["mean", "median"],
                "classifier__max_iter": [200, 500],
                "classifier__class_weight": ['balanced', None],
                "classifier__probability": [True, False],
                "classifier__gamma": ['scale', 'auto'],
        }

        knn_pipe_0 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_0),
                    ("classifier", KNeighborsClassifier())
                    ]
                )
        knn_pipe_1 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_1),
                    ("classifier", KNeighborsClassifier())
                    ]
                )
        knn_pipe_2 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_2),
                    ("classifier", KNeighborsClassifier())
                    ]
                )
        knn_param_grid = {
                "preprocessor__num__si__strategy": ["mean", "median"],
                "classifier__n_neighbors": [3, 5],
                "classifier__weights": ['uniform', 'distance'],
        }

        dtc_pipe_0 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_0),
                    ("classifier", DecisionTreeClassifier())
                    ]
                )
        dtc_pipe_1 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_1),
                    ("classifier", DecisionTreeClassifier())
                    ]
                )
        dtc_pipe_2 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_2),
                    ("classifier", DecisionTreeClassifier())
                    ]
                )
        dtc_param_grid = {
                "preprocessor__num__si__strategy": ["mean", "median"],
                "classifier__criterion": ['gini', 'entropy'],
                "classifier__max_depth": [4, 6, 8],
                "classifier__min_samples_split": [2, 8, 14, 20, 26, 32, 38],
                "classifier__min_samples_leaf": [3, 7, 11, 17, 25, 27],
                "classifier__class_weight": ['balanced', None],
        }

        rfc_pipe_0 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_0),
                    ("classifier", RandomForestClassifier())
                    ]
                )
        rfc_pipe_1 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_1),
                    ("classifier", RandomForestClassifier())
                    ]
                )
        rfc_pipe_2 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_2),
                    ("classifier", RandomForestClassifier())
                    ]
                )
        rfc_param_grid = {
                "preprocessor__num__si__strategy": ["mean", "median"],
                "classifier__criterion": ['gini', 'entropy'],
                "classifier__max_depth": [4, 6, 8],
                #"classifier__min_samples_split": [2, 8, 14, 20, 26, 32, 38],
                "classifier__min_samples_split": [2, 20],
                #"classifier__min_samples_leaf": [3, 7, 11, 17, 25, 27],
                "classifier__min_samples_leaf": [7],
                "classifier__class_weight": ['balanced', None],
        }

        xgbc_pipe_0 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_0),
                    ("classifier", XGBClassifier())
                    ]
                )
        xgbc_pipe_1 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_1),
                    ("classifier", XGBClassifier())
                    ]
                )
        xgbc_pipe_2 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_2),
                    ("classifier", XGBClassifier())
                    ]
                )
        xgbc_param_grid = {
                "preprocessor__num__si__strategy": ["mean", "median"],
                "classifier__max_depth": [4, 6, 8],
        }

        mlp_pipe_0 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_0),
                    ("classifier", MLPClassifier())
                    ]
                )
        mlp_pipe_1 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_1),
                    ("classifier", MLPClassifier())
                    ]
                )
        mlp_pipe_2 = Pipeline(
                steps=[
                    ("preprocessor", preprocessor_2),
                    ("classifier", MLPClassifier())
                    ]
                )
        mlp_param_grid = {
                "preprocessor__num__si__strategy": ["mean", "median"],
                "classifier__hidden_layer_sizes": [100, 200],
                "classifier__activation": ['relu', 'tanh', 'logistic'],
                "classifier__max_iter": [200, 500],
                "classifier__learning_rate": ['constant', 'invscaling', 'adaptive'],
                "classifier__solver": ['lbfgs', 'sgd', 'adam'],
        }
        warnings.warn('binary:logistic', UserWarning)

        # use train data
        X_train, X_test, y_train, y_test = train_test_split(X_train_org, y_train_org, test_size=0.25, random_state=45)

        index = ['roc_auc', 'precision', 'recall', 'f1_score', 'accuracy', 'balanced_accuracy_score']
        metrics = pd.DataFrame(index=index)

        # metrics = self.grid_code('LR_0', lr_pipe_0, lr_param_grid, X_train, X_test, y_train, y_test, metrics)
        # metrics = self.grid_code('LR_1', lr_pipe_1, lr_param_grid, X_train, X_test, y_train, y_test, metrics)
        # metrics = self.grid_code('LR_2', lr_pipe_2, lr_param_grid, X_train, X_test, y_train, y_test, metrics)

        # metrics = self.grid_code('SVM_0', svm_pipe_0, svm_param_grid, X_train, X_test, y_train, y_test, metrics)
        # metrics = self.grid_code('SVM_1', svm_pipe_1, svm_param_grid, X_train, X_test, y_train, y_test, metrics)
        # metrics = self.grid_code('SVM_2', svm_pipe_2, svm_param_grid, X_train, X_test, y_train, y_test, metrics)

        # metrics = self.grid_code('KNN_0', knn_pipe_0, knn_param_grid, X_train, X_test, y_train, y_test, metrics)
        # metrics = self.grid_code('KNN_1', knn_pipe_1, knn_param_grid, X_train, X_test, y_train, y_test, metrics)
        # metrics = self.grid_code('KNN_2', knn_pipe_2, knn_param_grid, X_train, X_test, y_train, y_test, metrics)

        # metrics = self.grid_code('DTC_0', dtc_pipe_0, dtc_param_grid, X_train, X_test, y_train, y_test, metrics)
        # metrics = self.grid_code('DTC_1', dtc_pipe_1, dtc_param_grid, X_train, X_test, y_train, y_test, metrics)
        # metrics = self.grid_code('DTC_2', dtc_pipe_2, dtc_param_grid, X_train, X_test, y_train, y_test, metrics)

        #metrics = self.grid_code('RFC_0', rfc_pipe_0, rfc_param_grid, X_train, X_test, y_train, y_test, metrics)
        #metrics = self.grid_code('RFC_1', rfc_pipe_1, rfc_param_grid, X_train, X_test, y_train, y_test, metrics)
        #metrics = self.grid_code('RFC_2', rfc_pipe_2, rfc_param_grid, X_train, X_test, y_train, y_test, metrics)

        metrics = self.grid_code('XGBC_0', xgbc_pipe_0, xgbc_param_grid, X_train, X_test, y_train, y_test, metrics)
        metrics = self.grid_code('XGBC_1', xgbc_pipe_1, xgbc_param_grid, X_train, X_test, y_train, y_test, metrics)
        metrics = self.grid_code('XGBC_2', xgbc_pipe_2, xgbc_param_grid, X_train, X_test, y_train, y_test, metrics)

        # metrics = self.grid_code('MLP_0', mlp_pipe_0, mlp_param_grid, X_train, X_test, y_train, y_test, metrics)
        # metrics = self.grid_code('MLP_1', mlp_pipe_1, mlp_param_grid, X_train, X_test, y_train, y_test, metrics)
        # metrics = self.grid_code('MLP_2', mlp_pipe_2, mlp_param_grid, X_train, X_test, y_train, y_test, metrics)

        print(metrics)

    def grid_code(self, name, x_pipe, param, X_train, X_test, y_train, y_test, metrics):
        try:
            grid_search = GridSearchCV(x_pipe, param,
                    scoring='f1',
                    cv=10,
                    verbose=1,
                    n_jobs=2,
                    )

            grid_search.fit(X_train, y_train)
            print("Best params:", grid_search.best_params_)

            gs = grid_search.best_estimator_
            gs.fit(X_train, y_train)
            y_pred_gs = gs.predict(X_test)
            y_score_gs = gs.predict_proba(X_test)[:,1:]
            metrics[str(name)] = self.get_score_clf(y_test, y_pred_gs, y_score_gs)

            return metrics
        except Exception as e:
            print("grid_code",e)

    def train_case(self, df_test, X_train, X_test, y_train, y_test):
        """
            Always check functions param.
        """
        numeric_features = ["Age", "RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck", "Billed"]
        numeric_transformer = Pipeline(
                steps=[
                    ("si", SimpleImputer(strategy="median")),
                    ("sc", StandardScaler()),
                    ]
                )
        categorical_features = ["HomePlanet", "CryoSleep", "Destination", "VIP", "Groups", "NewDeck", "NewNum", "NewSide", "Names"]
        categorical_transformer = Pipeline(
                steps=[
                    ("ohe", OneHotEncoder(handle_unknown="ignore")),
                    ]
                )
        preprocessor = ColumnTransformer(
                transformers=[
                    ("num", numeric_transformer, numeric_features),
                    ("cat", categorical_transformer, categorical_features),
                    ]
                )

        my_model = Pipeline(
                steps=[
                    ("preprocessor", preprocessor),
                    ("classifier", XGBClassifier(max_depth=4))
                    ]
                )

        my_model.fit(X_train, y_train)
        y_pred = my_model.predict(X_test)

        rr = pd.DataFrame({'Transported': y_pred})
        print('PassengerId,Transported')
        for idd, each in zip(df_test['PassengerId'], rr['Transported']):
            print(idd,',',bool(each), sep = '')

    def fix_nan_inf(self, df):
        try:
            # bad_indices = np.where(np.isnan(X_train_st))
            # bad_indices = np.where(np.isinf(X_train_st))
            df.fillna(df.mean(),inplace=True)
            return df
        except Exception as e:
            print("fix_nan_inf", e)

    def test_many(self, X_train, y_train):
        try:
            print("Running test function")
            # The Frame for metrics
            index = ['roc_auc', 'precision', 'recall', 'f1_score', 'accuracy', 'balanced_accuracy_score']
            metrics = pd.DataFrame(index=index)

            X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.25, random_state=45)

            # Fix data
            X_train = self.fix_nan_inf(X_train)
            X_test = self.fix_nan_inf(X_test)

            # SVM
            st = StandardScaler()
            X_train_st = st.fit_transform(X_train)
            X_test_st = st.transform(X_test)
            svm = SVC(class_weight='balanced', probability=True)
            svm.fit(X_train_st, y_train)
            y_pred_svm = svm.predict(X_test_st)
            y_score_svm = svm.predict_proba(X_test_st)[:,1:]
            metrics['SVM'] = self.get_score_clf(y_test, y_pred_svm, y_score_svm)

            # KNN
            sc = MinMaxScaler()
            X_train_std = sc.fit_transform(X_train)
            X_test_std = sc.transform(X_test)
            knc = KNeighborsClassifier()
            knc.fit(X_train_std, y_train)
            y_pred_knc = knc.predict(X_test_std)
            y_score_knc = knc.predict_proba(X_test_std)[:,1:]
            metrics['KNN'] = self.get_score_clf(y_test, y_pred_knc, y_score_knc)

            # Decision tree
            dtc = DecisionTreeClassifier(class_weight='balanced')
            dtc.fit(X_train, y_train)
            y_pred_dtc = dtc.predict(X_test)
            y_score_dtc = dtc.predict_proba(X_test)[:,1:]
            metrics['DTC'] = self.get_score_clf(y_test, y_pred_dtc, y_score_dtc)

            # GridSearch
            params = {
                     'criterion': ['gini', 'entropy'],
                     'max_depth': [4, 6, 8],
                     'min_samples_split': [2, 8, 14, 20, 26, 32, 38],
                     'min_samples_leaf': [3, 7, 11, 17, 25, 27]
                     }
            dtc = DecisionTreeClassifier(class_weight='balanced')
            cv = StratifiedKFold(n_splits=3, shuffle=True)
            grid_cv = GridSearchCV(dtc, params, scoring='f1', cv=cv, verbose=1)
            grid_cv.fit(X_train, y_train)
            grid_cv.best_params_
            gs_dtc = grid_cv.best_estimator_
            print(grid_cv.best_params_, grid_cv.best_estimator_)
            gs_dtc.fit(X_train, y_train)
            y_pred_gs_dtc = gs_dtc.predict(X_test)
            y_score_gs_dtc = gs_dtc.predict_proba(X_test)[:,1:]
            metrics['DTC_GS'] = self.get_score_clf(y_test, y_pred_gs_dtc, y_score_gs_dtc)

            # Random Forest
            rfc = RandomForestClassifier(class_weight='balanced')
            rfc.fit(X_train, y_train)
            y_pred_rfc = rfc.predict(X_test)
            y_score_rfc = rfc.predict_proba(X_test)[:,1:]
            metrics['RFC'] = self.get_score_clf(y_test, y_pred_rfc, y_score_rfc)

            # Gridsearch
            params = {
                     'n_estimators': [100, 200, 300],
                     'criterion': ['gini', 'entropy'],
                     'min_samples_leaf': [1, 2, 3],
                     'min_samples_split': [2, 4]
                     }
            rfc = RandomForestClassifier(class_weight='balanced')
            cv = StratifiedKFold(n_splits=3, shuffle=True)
            grid_cv = GridSearchCV(rfc, params, scoring='accuracy', cv=cv, verbose=1, n_jobs=-1)
            grid_cv.fit(X_train, y_train)
            grid_cv.best_params_
            gs_rfc = grid_cv.best_estimator_
            print(grid_cv.best_params_, grid_cv.best_estimator_)
            gs_rfc.fit(X_train, y_train)
            y_pred_gs_rfc = gs_rfc.predict(X_test)
            y_score_gs_rfc = gs_rfc.predict_proba(X_test)[:,1:]
            metrics['RFC_GS'] = self.get_score_clf(y_test, y_pred_gs_rfc, y_score_gs_rfc)

            # XGBoost
            xgb = XGBClassifier()
            xgb.fit(X_train, y_train)
            y_pred_xgb = xgb.predict(X_test)
            y_score_xgb = xgb.predict_proba(X_test)[:,1:]
            metrics['XGB'] = self.get_score_clf(y_test, y_pred_xgb, y_score_xgb)

            # LGBM
            '''
            lgbm = LGBMClassifier(class_weight='balanced')
            lgbm.fit(X_train, y_train)
            y_pred_lgbm = lgbm.predict(X_test)
            y_score_lgbm = lgbm.predict_proba(X_test)[:,1:]
            metrics['LGBM'] = self.get_score_clf(y_test, y_pred_lgbm, y_score_lgbm)

            # Gridsearch
            params = {
                     'boosting_type': ['gbdt', 'goss'],
                     'learning_rate': [0.005, 0.01, 0.05, 0.1, 0.3],
                     'n_estimators': [100, 200, 300, 400],
                     'reg_alpha': np.linspace(0.0, 20.0, 5),
                     'reg_lambda': np.linspace(0.0, 25.0, 5),
                     'max_depth': [-1, 4, 10]
                     }
            lgbm = LGBMClassifier(class_weight='balanced')
            cv = StratifiedKFold(n_splits=3, shuffle=True)
            grid_cv = GridSearchCV(lgbm, params, scoring='accuracy', cv=cv, verbose=1, n_jobs=-1)
            grid_cv.fit(X_train, y_train)
            grid_cv.best_params_
            gs_lgb = grid_cv.best_estimator_
            gs_lgb.fit(X_train, y_train)
            y_pred_lg_gs = gs_lgb.predict(X_test)
            y_score_lg_gs = gs_lgb.predict_proba(X_test)[:,1:]
            metrics['LGBM_GS'] = self.get_score_clf(y_test, y_pred_lg_gs, y_score_lg_gs)
            '''
            print(metrics)
        except Exception as e:
            print("Test_many", e)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='.')

    parser.add_argument('--version', '-v', '-vvv', '-version', action='version', version=str('Base 2.1'))

    parser.add_argument('--dataset-train', type=str, required=True, help='This option define the dataset Train.')

    parser.add_argument('--dataset-test', type=str, required=True,  help='This option define the dataset Test.')

    # get args
    args = parser.parse_args()
    kwargs = {
        'dataset_train': args.dataset_train,
        'dataset_test': args.dataset_test
    }

    args = parser.parse_args()

    try:
        worker = Titanic(**kwargs)
        worker.main()
    except KeyboardInterrupt as e:
        print('Exit using ctrl^C')
