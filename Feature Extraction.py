import numpy, datetime, time

#constant declaration
Base_T = datetime.datetime.strptime("2001-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
Base_Target = time.mktime(Base_T.timetuple())
T = datetime.datetime.strptime("2008-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
Target = int(time.mktime(T.timetuple()) - Base_Target) # Sep.1 2010 in secs
Train_T = datetime.datetime.strptime("2007-08-01 00:00:00", "%Y-%m-%d %H:%M:%S")
Train_Target = int(time.mktime(Train_T.timetuple()) - Base_Target) # Apr.1 2010 in secs

# periods of X days, X = 1, 2, 4, 8, 16, 64, 365 days
P = [1, 2, 4, 8, 16, 64, 365] 
Period = [elem * 24 * 60 * 60 for elem in P] # periods of secs
#SolutionPeriod = (31 * 3 + 30 * 2) * 24 * 60 * 60 # next 5 months in unit of in secs
D = [1, 16, 64, 256, 512] # the Dth most recent edit
#Namespace: 0 1 2 3 4 5
N = [0, 1, 2, 3, 4, 5]

#funtions implementation
def extractData(filename):
    #read a file
    f = open(filename,'r')

    # data: user_id, namespace, timestamp, article_id
    data = []
    user_id = []
    article_id = []
    namespace = []
    #nreverted = []
	
    titleString = f.readline()

    for line in f:
	s = line.split('\t')

	user_id.append(s[0])
	article_id.append(s[1])
	namespace.append(s[2])
	date = s[3]

        data.append((s[0], s[2], date, s[1], s[4]))
		
    return data, user_id
    
def getFeatures(inputfile, outputFeatures, outputValue, isPredict):
    if(isPredict == True):
        datePoint = Target
    else:
        datePoint = Train_Target
        
    data = extractData(inputfile)
    #print data[0][1][2]
    user_id = [elem for elem in set(data[1])]
    
    # editsX : userid -> 1:0, 2:0, 4:0, ... 365:0 (0: num of edits)
    editsX = {}
    # editsArtX : userid -> 1:0, 2:0, 4:0, ... 365:0 (0: num of edited articles)
    editsArtX = {}
    # editsArtX_dict : userid -> 1:[], 2:[], 4:[], ... 365:[] ([]: article id)
    editsArtX_dict = {}
    # durationX_dict : userid -> 1:[], 2:[], 4:[], ... 365:[] ([]: timestamp)
    durationX_dict = {}
    # durationX : userid -> 1:0, 2:0, 4:0, ... 365:0 (0: duration in unit of sec)
    durationX = {}
    # solution : userid -> 0 (0: num of edits in the next 5 months)
    trainRes = {}
    # namespace : 0, 1, 2, 3, 4, 5, sum
    namespace = {}
    # number of reverted edits
    nreverted = {}
    
    # initialize editsX, editsArtX, editsArtX_dict, trainRes
    for x in user_id:
	edits_tmp = { x : [0, 0, 0, 0, 0, 0, 0] }
	editsX.update( edits_tmp )

	editsArt_tmp = { x : [0, 0, 0, 0, 0, 0, 0] }
	editsArtX.update( editsArt_tmp )

	editsArt_dict_tmp = { x : {} }
	editsArtX_dict.update( editsArt_dict_tmp )

	trainRes_tmp = { x : 0 }
	trainRes.update( trainRes_tmp )

	durationX_dict.update( { x : [] } )
	
	durationX.update( { x : [Target, Target, Target, Target, Target] } )

	namespace.update( { x : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0]} )
	
	nreverted.update( {x : 0} )
    
    # fill in editsX, editsArtX_dict, trainRes 
    for i in range(len(data[0])):
        x = data[0][i][0]
	for j in range(len(Period)):
	    # editsX, editsArtX, editsArtX_dict, 
	    if(int(data[0][i][2]) < datePoint and datePoint - int(data[0][i][2]) <= Period[j]):
                editsX[x][j] += 1
		aid = data[0][i][3]

		if(P[j] in editsArtX_dict[x].keys()):
		    editsArtX_dict[x][P[j]].append(aid)
		else:
		    editsArtX_dict[x][P[j]] = [aid]

	# trainRes
	if(isPredict == False):       
	    if(int(data[0][i][2]) >= datePoint):     
		trainRes[x] += 1

	# durationX_dict
	if(int(data[0][i][2]) < datePoint):
	    durationX_dict[x].append(int(data[0][i][2]))

	#namespace
	if(int(data[0][i][2]) < datePoint):
	    nid = int(data[0][i][1])
	    namespace[x][nid] += 1
	    namespace[x][6] += 1 # sum++
	
	# nreverted
	if(int(data[0][i][2]) < datePoint and int(data[0][i][4]) > 0):
	    nreverted[x] += int(data[0][i][4])
    
    # compute editsArtX from editsArtX_dict
    for x in user_id:
        for j in range(len(Period)):
            if(P[j] in editsArtX_dict[x].keys()):
                s = set( editsArtX_dict[x][P[j]] )
                editsArtX[x][j] = len(s)
                #editsArtX_dict[x][P[j]] = [s]
                
    # compute durationX from durationX_dict
    for x in user_id:
        arr = durationX_dict[x]
        arr.sort(reverse = True)
        for i in range(len(D)):
            if(len(arr) >= D[i]):
                durationX[x][i] = datePoint - arr[ D[i]-1 ]
	    elif(len(arr) > 0):
	        durationX[x][i] = datePoint - arr[-1]
	        
    # compute the percentage of each namespace
    for x in user_id:
        if(namespace[x][6] > 0):
            for i in range(len(N)):
                namespace[x][i] /= namespace[x][6]

    # output whole features without user_id
    with open(outputFeatures, "w") as of:
        for x in user_id:
            of.write(str(x) + "\t")
            of.write("\t".join(map(str, editsX[x][:7])) + "\t")
            of.write("\t".join(map(str, editsArtX[x][:7])) + "\t")
            of.write("\t".join(map(str, namespace[x][:6])) + "\t")
            of.write("\t".join(map(str, durationX[x][:5])) + "\t")
            of.write(str(nreverted[x]) + "\t\n")

    # in learn phase, output Train_Solu
    if(isPredict == False):
        with open(outputValue, "w") as of:
            of.write("user_id	solution\n")
            for x in user_id:
                of.write(str(x) + "\t" + str(trainRes[x]) + "\t\n")

    
    
starttime = time.clock()
getFeatures("validation_prepare.tsv", "validation_train_X(all).tsv", "validation_train_y(all).tsv", False)
getFeatures("validation_prepare.tsv", "validation_predict_X(all).tsv", "validation_predict_y.tsv", True)
print time.clock() - starttime