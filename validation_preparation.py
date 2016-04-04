import numpy, datetime, time

#constant declaration
T = datetime.datetime.strptime("2008-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
Target = time.mktime(T.timetuple()) # Sep.1 2010 in secs
Train_T = datetime.datetime.strptime("2007-08-01 00:00:00", "%Y-%m-%d %H:%M:%S")
Train_Target = time.mktime(Train_T.timetuple()) # Apr.1 2010 in secs
Base_T = datetime.datetime.strptime("2001-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
Base_Target = time.mktime(Base_T.timetuple())

#funtions implementation
def data_prepare(filename, output):
    #read a file
    f = open(filename,'r')
    out =  open(output,'w')
    out.write("user_id" + "\t")
    out.write("article_id" + "\t")
    out.write("namespace" + "\t")
    out.write("time" + "\t")
    out.write("reverted" + "\t\n")

    #user_id = []
    user_id_tmp = []
    #article_id = []
    article_id_tmp = []
    #namespace = []
    namespace_tmp = []
    #timestamp = []
    timestamp_tmp = []
    # reverted
    reverted_tmp = []
    
    nOfedits = 0
    nOfeditors = 0
	
    titleString = f.readline()
    line = f.readline()
    s = line.split('\t')
    prev_id = s[0]
    while 1:
        if not line:
            break
            
        flag = 0
        while 1:
            user_id_tmp.append(s[0])
	    article_id_tmp.append(s[1])
	    namespace_tmp.append(s[3])
	    reverted_tmp.append(s[6])

	   # transfer string to datetime
	    d = datetime.datetime.strptime(s[4], "%Y-%m-%d %H:%M:%S")
	   # how many secs have it been after epoch(1970-01-01)
	    date = time.mktime(d.timetuple())
	    timestamp_tmp.append(date - Base_Target)
	    
            if(date >= Train_Target):
                flag = 1
            
            prev_id = s[0]
            
            line = f.readline()
            if not line:
                break
            s = line.split('\t')
            if s[0] != prev_id:
                break
                
        if flag:
            nOfedits += len(user_id_tmp)
            nOfeditors += 1
            for i in range(len(user_id_tmp)):
                out.write(str(user_id_tmp[i]) + "\t")
                out.write(str(article_id_tmp[i]) + "\t")
                out.write(str(namespace_tmp[i]) + "\t")
                out.write(str(int(timestamp_tmp[i])) + "\t")
                out.write(str(reverted_tmp[i]) + "\t\n")
                
        user_id_tmp = []
        article_id_tmp = []
        namespace_tmp = []
        timestamp_tmp = []
        reverted_tmp = []
    print "number of edits: " + str(nOfedits)
    print "number of editors: " + str(nOfeditors)

###############################
start_time = time.clock()
data_prepare("validation.tsv", "validation_prepare.tsv")
end_time = time.clock()
print end_time - start_time

