import numpy, datetime, time, math
from sklearn import linear_model
from sklearn import svm, tree, ensemble

def featuresConstruct(file_X, file_y, isPredict):
    f_X = open(file_X, 'r')
    if(isPredict == False):
        f_y = open(file_y, 'r')
    
    X = []
    y = []
    user_id = []
    
    for line in f_X:
        li = line.split('\t')
        user_id.append(li[0])
        tmp = []
        for i in range(1, 15):
            tmp.append(math.log(int(li[i]) + 1))
        for i in range(15, 21):
            tmp.append(math.log(float(li[i]) + 1))
        for i in range(21, 26):
            tmp.append(math.log(int(li[i]) + 1))
        tmp.append(math.log(int(li[26]) + 1))
            
        X.append(tmp)
    #for line in f_X:
    #    li = line.split('\t')
    #    user_id.append(li[0])
    #    tmp = []
    #    for i in range(1, 8):
    #        tmp.append(math.log(int(li[i]) + 1))
    #    for i in range(8, 14):
    #        tmp.append(math.log(float(li[i]) + 1))
    #    
    #    X.append(tmp)
        
    if(isPredict == False):
        f_y.readline()
        for line in f_y:
            li = line.split('\t')
            y.append(math.log(int(li[1]) + 1))
            
    return user_id, X, y

start_time = time.clock()
output = featuresConstruct("validation_train_X(all).tsv", "validation_train_y(all).tsv", False)
#output = featuresConstruct("training_train_X(all).tsv", "training_train_y(all).tsv", False)

X = output[1]
y = output[2]

# learn OLS model
#model = linear_model.LinearRegression(normalize = True)
#model.fit(X, y)

# learn SVR model
#model = svm.SVR(C = 1e-6, epsilon = 0.6, kernel = 'poly', degree = 4, gamma = 0.048, coef0 = -1.9)
#model.fit(X, y)

#learn SDG Regression
#model = linear_model.SGDRegressor()
#model.fit(X, y)

#learn Decision Tree Regression
#model = tree.DecisionTreeRegressor(max_leaf_nodes = 5, max_depth = None, min_samples_leaf = 1)
#model.fit(X, y)

#learn GBR
model = ensemble.GradientBoostingRegressor(n_estimators = 20, learning_rate = 0.1, max_depth = 1)
model.fit(X, y)

output1 = featuresConstruct("validation_predict_X(all).tsv", "validation_train_y(all).tsv", True)
#output1 = featuresConstruct("training_predict_X(all).tsv", "training_predict_y(all).tsv", True)

user_id = output1[0]
xx = output1[1]
yy = model.predict(xx)

constant = 2.25

with open("predictRes.tsv", "w") as of:
    of.write("user_id	solution\n")
    for i in range(len(user_id)):
        yy[i] = max(math.exp(yy[i]) - 1 - constant, 0)
        of.write(str(user_id[i]) + "\t" + str(yy[i]) + "\t\n")

end_time = time.clock()
print end_time - start_time