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


class EC2SORG:
    def __init__(self, ec):
        self.ec = ec

    def org(self):
        f=open("Enz_org_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=20&RN=&RNV=&os=&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=&W[2]=%s&T[2]=1&W[4]=&T[4]=2&W[5]=&T[5]=2&V[5]=1&W[6]=&T[6]=1&V[6]=&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("Organism" + "\t" "PubMed ID" "\n")
        print ("\nOrganism\tPubMed ID")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("Organism data is not available for the enzyme:" + " " + self.ec)
            f.write ("Organism data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(.+)\t(.+)", each)):
                org=dtval[1]
                pubmedid=dtval[2]
                print (org + "\t" + pubmedid)
                f.write (org + "\t" + pubmedid + "\n")
        f.write ("\n")
        return ""