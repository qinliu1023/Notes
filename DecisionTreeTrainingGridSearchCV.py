def DecisionTreeTrainingGridSearchCV(df_input, col_drop, col_cat, indicator, param_dict, parameters, tree_filename):
    """
    This function is aimed to run DicisionTreeClassifier based on a customized dataset.

    Inputs: 
    - Dataframe
    - Columns not to be included
    - Columns need to be encoded into dummies
    - test_size
    - parameter_dictionary, e.g. {"test_size": 0.20, "min_samples_leaf": 0.05, "max_depth": 4}
    - parameters: for GridSearchCV, e.g. parameters = 
             {"criterion": ["gini", "entropy"],
              "max_depth": range(3,10),
              "min_samples_leaf": [0.05, 0.06, 0.07, 0.08, 0.09, 0.10]} # min sample leaf greater than 5%


    Outpits:
    - Model
    - Tree
    """

    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score
    from sklearn import tree
    import re

    X_inner = df_input.drop(col_drop, axis = 1)
    X_inner = pd.concat([X_inner.drop(col_cat, axis = 1).T,
                   pd.get_dummies(df_input[col_cat], prefix = col_cat, drop_first = True).T 
                  ]).T
    
    y_inner = df_input[[indicator]]
    
    X_inner_train, X_inner_test, y_inner_train, y_inner_test = train_test_split(X_inner, y_inner, stratify = y_inner, 
                                                                                test_size = param_dict["test_size"], 
                                                                                random_state = 42)    
    
    c, r = y_inner_train.shape
    
    model_inner = DecisionTreeClassifier(random_state = 42, 
                                         min_samples_leaf = param_dict["min_samples_leaf"], 
                                         max_depth = param_dict["max_depth"])
    
    grid_model_inner = GridSearchCV(estimator = model_inner, param_grid = parameters, cv = 10).fit(X_inner_train.values, y_inner_train.values.reshape(c,))
    
    best_model_inner = grid_model_inner.best_estimator_
    
    model_predictions = model_inner.fit(X_inner_train, y_inner_train).predict(X_inner_test)
    
    best_predictions = best_model_inner.predict(X_inner_test)
    
    # Report the before-and-afterscores
    print ("Unoptimized model\n------")
    print ("Accuracy score on testing data: {:.4f}".format(accuracy_score(y_inner_test, model_predictions)))
    
    print ("\nOptimized Model\n------")
    print ("Final accuracy score on the testing data: {:.4f}".format(accuracy_score(y_inner_test, best_predictions)))
    
    print ("\n")
    print (grid_model_inner.get_params())
    
    print ("best_model\n------")
    print (best_model_inner)


    if accuracy_score(y_inner_test, model_predictions) <= accuracy_score(y_inner_test, best_predictions):
        model_selected = best_model_inner
    else:
        model_selected = model_inner
    
    dotfile = open("{}_{}.dot".format(tree_filename, pd.datetime.today().strftime('%Y-%m-%d').replace('-','')), 'w')
    tree.export_graphviz(model_selected, out_file = dotfile, feature_names = X_inner_train.columns, proportion = True, impurity = False)
    dotfile.close()
    
    with open("{}_{}.dot".format(tree_filename, pd.datetime.today().strftime('%Y-%m-%d').replace('-',''))) as f:
        read_data=f.read()
    f.closed
    read_data = re.sub(r"\[[0-9]+\.[0-9]+\,","\[",read_data)
    read_data=re.sub(r"value","good_proportion",read_data)
    with open("{}_{}.dot".format(tree_filename, pd.datetime.today().strftime('%Y-%m-%d').replace('-','')),'w') as f:
        f.write(read_data)
    f.closed

    return model_selected



#start_time = time.time()
#
#model = \
#DecisionTreeTrainingGridSearchCV(df_input = df, 
#                                 col_drop = ["is_good", "id", "structure"], 
#                                 col_cat= ['reason'],
#                                 indicator = "is_good",
#                                 param_dict = {"test_size": 0.20, "min_samples_leaf": 0.05, "max_depth": 3}, 
#                                 parameters = {"criterion": ["gini", "entropy"],
#                                               "max_depth": range(3,10),
#                                               "min_samples_leaf": [0.05, 0.06, 0.07, 0.08, 0.09, 0.10]},
#                                 tree_filename = "dt_plot")
#
#end_time = time.time()
#
#print (end_time - start_time)/60.0    
