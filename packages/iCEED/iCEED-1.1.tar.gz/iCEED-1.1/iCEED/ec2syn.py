import sys
import io
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
import requests
import re
now = datetime.now()
jobid = str(now)
jobid = re.sub(' ', '', jobid)
jobid = re.sub('\.', '', jobid)
jobid = re.sub('-', '', jobid)
jobid = re.sub(':', '', jobid)


class EC2SYN:
    def __init__(self, ec):
        self.ec = ec

    def syn(self):
        f=open(r"Enz_syn_%s.txt" %jobid,"a")
        allsyns = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=39&W[2]=&l=10&os=1&RN=&W[1]=%s&T[1]=1&W[3]=&T[3]=2&W[4]=&T[4]=2&W[5]=&T[5]=2&Search=Search&l=10" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("Synonyms:" + "\n")
        print("Synonyms:\n")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            count = 0
            print ("Synonyms are not available for the enzyme:" + " " + self.ec)
            f.write ("Synonyms are not available for the enzyme:" + " " + self.ec + "\n")
        if (dtval := re.match(r"(\S+)\t(.+)", abs)):
            count = 1
            syns=dtval[2]
            allres = syns.split(",")
        for esn in allres:
            esn = esn.strip()
            esn = re.sub('in	this	file', '', esn)
            print (count, " - ", esn)
            f.write (str(count) + " - " + esn + "\n")
            count += 1
        return ""
