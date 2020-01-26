#takes in 2 numpy arrays 
#first array is "clean text"
#second array is the classes 

def naive_bayes(text_array, class_vector):
    
    from sklearn.model_selection import KFold
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    import numpy as np 
    
    
    #split data into 5 folds
    kf = KFold(n_splits=5, random_state = 0)
    fold1, fold2, fold3, fold4, fold5 = kf.split(text_array)
    folds = [fold1, fold2, fold3, fold4, fold5]
    
    scores = []
    
    for f in folds:
        #split data into testing a training set 
        train, train_classes = text_array[f[0]], class_vector[f[0]]
        test, test_classes = text_array[f[1]], class_vector[f[1]]
        
        #vectorize the features
        vectorizer = CountVectorizer()
        train_v = vectorizer.fit_transform(train)
        test_v = vectorizer.transform(test)
        
        #return test_v,test_classes
        
        #run NB
        nb_classifier = MultinomialNB()
        nb_classifier.fit(train_v, train_classes)
        #print(nb_classifier.score(test_v, test_classes))
        #print(type(nb_classifier.score(test_v, test_classes)))
        
        scores += [nb_classifier.score(test_v, test_classes)]
    
    return np.mean(scores)



#takes in 3 numpy objects 
#first array is "clean text"
#second array is the classes 
#3rd argument is optional matrix of other numerical features 

def logistic(text_array, class_vector, numerical_matrix = None):
    
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import KFold
    from sklearn.feature_extraction.text import CountVectorizer
    from scipy.sparse import csr_matrix, hstack
    import numpy as np

    
    #split data into 5 folds
    kf = KFold(n_splits=5, random_state = 0)
    fold1, fold2, fold3, fold4, fold5 = kf.split(text_array)
    folds = [fold1, fold2, fold3, fold4, fold5]
    
    scores = []
    
    for f in folds:
        #split data into testing a training set 
        train_text, train_classes = text_array[f[0]], class_vector[f[0]] 
        test_text, test_classes = text_array[f[1]], class_vector[f[1]]
        
        #vectorize the features
        vectorizer = CountVectorizer()
        train = vectorizer.fit_transform(train_text)
        test = vectorizer.transform(test_text)
        
        #combine with rest of numerical data 
        if type(numerical_matrix) != type(None):
            train = hstack([train, csr_matrix(numerical_matrix[f[0]])])
            test = hstack([test, csr_matrix(numerical_matrix[f[1]])])
        
        #run logistic regression
        logistic_classifier = LogisticRegression(random_state=0, max_iter = 2000)
        logistic_classifier.fit(train, train_classes)
        
        scores += [logistic_classifier.score(test, test_classes)]
    
    return np.mean(scores)




def random_forest(text_array, class_vector, numerical_matrix = None):
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import KFold
    from sklearn.feature_extraction.text import CountVectorizer
    from scipy.sparse import csr_matrix, hstack
    import numpy as np 

    
    #split data into 5 folds
    kf = KFold(n_splits=5)
    fold1, fold2, fold3, fold4, fold5 = kf.split(text_array)
    folds = [fold1, fold2, fold3, fold4, fold5]
    
    scores = []
    
    for f in folds:
        #split data into testing a training set 
        train_text, train_classes = text_array[f[0]], class_vector[f[0]] 
        test_text, test_classes = text_array[f[1]], class_vector[f[1]]
        
        #vectorize the features
        vectorizer = CountVectorizer()
        train = vectorizer.fit_transform(train_text)
        test = vectorizer.transform(test_text)
        
        #combine with rest of numerical data 
        if type(numerical_matrix) != type(None):
            train = hstack([train, csr_matrix(numerical_matrix[f[0]])])
            test = hstack([test, csr_matrix(numerical_matrix[f[1]])])
        
        #run logistic regression
        rf_classifier = RandomForestClassifier()
        rf_classifier.fit(train, train_classes)
        
        scores += [rf_classifier.score(test, test_classes)]
    
    return np.mean(scores)
    
    
    