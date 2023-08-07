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


class EC2REPATH:
    def __init__(self, ec):
        self.ec = ec


    def rcn(self):
        f=open(r"Enz_RC_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=27&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n\n")
        f.write ("Reactions" + "\n")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("Reaction data is not available for the enzyme:" + " " + self.ec)
            f.write ("Reaction data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('	\d+	$', '', each)
            each = re.sub('Nothing	in	this	file', '', each)
            eachline = each.split("\t")
            if (dtval := re.match(r"(\S+)\t(.+)", each)):
                rcn=dtval[2]
                print (rcn)
                f.write (rcn + "\n")
        f.write ("\n")
        return ""


    def pth(self):
        f=open("Enz_Path_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=137&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&V[3]=1&V[4]=1&V[5]=1&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n\n")
        f.write ("Pathway name" + "\t" "Database Identifier" + "\t" "Source database" + "\n")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("Pathway data is not available for the enzyme:" + " " + self.ec)
            f.write ("Pathway data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(\S+)\t(.+)", each)):
                ki=dtval[2]
                if (kg := re.match(r".+\tPWY-\d+", ki) or re.match(r".+\tPWY\S+-\d+", ki)or re.match(r".+\t\S+-PWY.+", ki)):
                    ki = re.sub('\t-', '', ki)
                    print (ki + "\t" + "MetaCyc")
                    f.write (ki + "\t" + "MetaCyc" + "\n")
                if (kg := re.match(r".+\t\d+\t", ki)):
                    ki = re.sub('\t-', '', ki)
                    print (ki + "\t" + "KEGG")
                    f.write (ki + "\t" + "KEGG" + "\n")
                if (kg := re.match(r".+\t\w+ .+\t", ki)):
                    ki = re.sub('\t-', '', ki)
                    print (ki + "\t" + "BRENDA")
                    f.write (ki + "\t" + "BRENDA" + "\n")
        f.write ("\n")
        return ""
