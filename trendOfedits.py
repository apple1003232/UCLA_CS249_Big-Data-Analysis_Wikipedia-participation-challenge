import time, datetime
import matplotlib.pyplot as fg

Base_T = datetime.datetime.strptime("2001-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
Base_Target = time.mktime(Base_T.timetuple())

FIVEMONTH = 150 * 24 * 3600

First_T = datetime.datetime.strptime("2003-11-01 00:00:00", "%Y-%m-%d %H:%M:%S")
First_Target = time.mktime(First_T.timetuple()) - Base_Target

def trendOfedits(inputfile):
    file = open(inputfile, 'r')
    avg_edits = []
    for i in range(10):
        avg_edits.append(0)
    
    file.readline()
    numOfusers = 0;
    uid = 0;
    for line in file:
        s = line.split('\t')
        time = int(s[3])
        if (numOfusers == 0 or uid != int(s[0])):
            numOfusers += 1
            uid = int(s[0])
        for i in range(10):
            if(time >= First_Target + FIVEMONTH * i and time < First_Target + FIVEMONTH * (i + 1)):
                avg_edits[i] += 1
                break
                
    for i in range(10):
        avg_edits[i] = avg_edits[i] * 1.0 / (numOfusers * 1.0)
    
    print avg_edits
               
    fg.figure()
    #fg.plot(avg_edits)
    fg.bar(range(10), avg_edits, width = 0.9, align = 'center')
    fg.xlabel("Sequence of five months")
    fg.ylabel("Avg edtis number in five months")
    fg.show()

trendOfedits("validation_prepare.tsv")