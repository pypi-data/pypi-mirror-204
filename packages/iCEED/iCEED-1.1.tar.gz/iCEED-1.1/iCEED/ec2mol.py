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


class EC2MOL:
    def __init__(self, ec):
        self.ec = ec

    def subpr(self):
        f=open(r"Enz_subpr_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=37&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&W[2]=&W[3]=&T[3]=2&W[4]=&T[4]=2&W[5]=&T[5]=2&V[5]=1&W[6]=&T[6]=2&V[6]=1&W[7]=&T[7]=2&W[10]=&T[10]=2&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("Substrates" + "\t" "Products" + "\t" + "Organism" + "\n")
        print("Substrates\tProducts\tOrganism\n")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("Substrate and Product data is not available for the enzyme:" + " " + self.ec)
            f.write ("Substrate and Product data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('	\d+	$', '', each)
            each = re.sub('Nothing	in	this	file', '', each)
            eachline = each.split("\t")
            if (dtval := re.match(r"(\S+)\t(.+)\t(.+)\t(.+)", each)):
                subs=dtval[2]
                subs = re.sub('additional information', '', subs)			
                org=dtval[3]
                org = re.sub('additional information', '', org)
                prd=dtval[4]
                prd = re.sub('additional information', '', prd)
                print (subs + "\t" + prd + "\t" + org)
                f.write (subs + "\t" + prd + "\t" + org + "\n")
        f.write ("\n")
        return ""


    def cof(self):
        f=open("Enz_cof_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=48&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&W[2]=&W[3]=&T[3]=2&W[4]=&T[4]=2&W[6]=&T[6]=2&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("Cofactor/s" + "\n")
        print("Cofactor/s\n")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("Cofactor data is not available for the enzyme:" + " " + self.ec)
            f.write ("Cofactor data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(\S+)\t(.+)", each)):
                cof=dtval[2]
                cof = re.sub('additional information', '', cof)
                print (cof)
                f.write (cof + "\n")
        f.write ("\n")
        return ""


    def metion(self):
        f=open("Enz_metion_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=15&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&W[2]=&W[3]=&T[3]=2&W[4]=&T[4]=2&W[6]=&T[6]=2&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("Metal and Ion" + "\n")
        print("Metal and Ion\n")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("Metal and Ion data is not available for the enzyme:" + " " + self.ec)
            f.write ("Metal and Ion data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(\S+)\t(.+)", each)):
                metion=dtval[2]
                metion = re.sub('additional information', '', metion)
                #org=dtval[3]
                #prd=dtval[4]
                print (metion)
                f.write (metion + "\n")
        f.write ("\n")
        return ""


    def inhib(self):
        f=open("Enz_inhib_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=11&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&W[2]=&W[3]=&T[3]=2&W[4]=&T[4]=2&W[6]=&T[6]=2&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        #f.write ("Substrates" + "\t" "Products" + "\t" + "Organism" + "\n")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("Inhibitor data is not available for the enzyme:" + " " + self.ec)
            f.write ("Inhibitor data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(\S+)\t(.+)", each)):
                inhib=dtval[2]
                inhib = re.sub('additional information', '', inhib)
                #org=dtval[3]
                #prd=dtval[4]
                print (inhib)
                f.write (inhib + "\n")
        f.write ("\n")
        return ""


    def actcpd(self):
        f=open("Enz_actcpd_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=1&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&W[2]=&W[3]=&T[3]=2&W[4]=&T[4]=2&W[6]=&T[6]=2&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        #f.write ("Substrates" + "\t" "Products" + "\t" + "Organism" + "\n")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("Activating compound data is not available for the enzyme:" + " " + self.ec)
            f.write ("Activating compound data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(\S+)\t(.+)", each)):
                actcpd=dtval[2]
                actcpd = re.sub('additional information', '', actcpd)
                #org=dtval[3]
                #prd=dtval[4]
                print (actcpd)
                f.write (actcpd + "\n")
        f.write ("\n")
        return ""