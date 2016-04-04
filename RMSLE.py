import math, csv, time
from collections import namedtuple

def RSMLE(myout, accurate):
    test = {}
    acc = {}
    
    f = open(myout,'r')
    f.readline()
    for line in f:
        s = line.split('\t')
	test.update({s[0]:s[1]})
	
    # for validation   
    ff = open(accurate, 'r')
    ff.readline()
    for line in ff:
        s = line.split(',')
	acc.update({s[0]:s[1]})
     # for training
 #   ff = open(accurate, 'r')
 #   ff.readline()
 #   for line in ff:
 #       s = line.split('\t')
	#acc.update({s[0]:s[1]})

 #   with open(accurate) as ff:
	#f_csv = csv.reader(ff)
	#headings = next(f_csv)
	#Row = namedtuple('Row', headings)
	#for r in f_csv:
	#   row = Row(*r)
	#   acc.update({row.user_id:row.solution})

    n = len(acc.keys());
    sum = 0
    sum_mse = 0
    for x in acc.keys():
        if(x in test.keys()):
	   pi = float(test[x])
	else:
	   #pi = int(acc[x])
	   n -= 1
	   #print "meiyou"
	ai = int(acc[x])
	if(x in test.keys()):
	    sum += (math.log(pi+1)-math.log(ai+1))**2
	    sum_mse += (pi - ai)**2

    sum /= n
    sum_mse /= n
    res = math.sqrt(sum)
    res_mse = math.sqrt(sum_mse)

    return res, res_mse
####################################
start_time = time.clock()

res =  RSMLE("predictRes.tsv", "validation_solutions.tsv")
#res = RSMLE("predictRes.tsv", "training_predict_y(all).tsv")
print "rmsle: " + str(res[0])
print "mse: " + str(res[1])
#print RSMLE("predictRes.tsv", "training_predict_y.tsv")

end_time = time.clock()
print end_time - start_time