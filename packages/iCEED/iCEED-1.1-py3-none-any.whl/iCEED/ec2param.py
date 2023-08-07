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


class EC2PARAM:
    def __init__(self, ec):
        self.ec = ec


    def kmv(self):
        f=open(r"Enz_KM_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=12&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&W[2]=&W[3]=&T[3]=1&W[4]=&T[4]=2&V[4]=1&W[5]=&T[5]=2&W[6]=&T[6]=2&W[8]=&T[8]=2&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("KM value" + "\t" "Substrate" + "\n")
        print ("\nKM value\tSubstrate")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("KM value data is not available for the enzyme:" + " " + self.ec)
            f.write ("KM value data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('	\d+	$', '', each)
            each = re.sub('Nothing	in	this	file', '', each)
            eachline = each.split("\t")
            if (dtval := re.match(r"(\S+)\t(.+)\t(.+)", each)):
                km=dtval[2]
                km = re.sub('additional information', '', km)
                subs=dtval[3]
                subs = re.sub('additional information', '', subs)
                print (km + "\t" + subs)
                f.write (km + "\t" + subs + "\n")
        f.write ("\n")
        return ""


    def kiv(self):
        f=open("Enz_Ki_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=49&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&W[2]=&W[3]=&T[3]=1&W[4]=&T[4]=2&V[4]=1&W[5]=&T[5]=2&W[6]=&T[6]=2&W[8]=&T[8]=2&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("KI value" + "\t" "Inhibitors" + "\n")
        print ("\nKI value\tInhibitors")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("Ki value data is not available for the enzyme:" + " " + self.ec)
            f.write ("Ki value data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(\S+)\t(.+)\t(.+)", each)):
                ki=dtval[2]
                ki = re.sub('additional information', '', ki)
                inhibs=dtval[3]
                inhibs = re.sub('additional information', '', inhibs)
                print (ki + "\t" + inhibs)
                f.write (ki + "\t" + inhibs + "\n")
        f.write ("\n")
        return ""


    def ic50(self):
        f=open("Enz_Ic50_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=54&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&W[2]=&W[3]=&T[3]=1&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("IC50 value" + "\n")
        print ("\nIC50 value")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        #print (abs)
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("IC50 value data is not available for the enzyme:" + " " + self.ec)
            f.write ("IC50 value data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(\S+)\t(\S+)", each)):
                ic=dtval[2]
                #inhibs=dtval[3]
                print (ic)
                f.write (ic + "\n")
        f.write ("\n")
        return ""


    def pH(self):
        f=open("Enz_pH_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=45&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&W[2]=&W[3]=&T[3]=1&W[4]=&T[4]=2&W[5]=&T[5]=2&W[6]=&T[6]=2&V[6]=1&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("pH" + "\t" "PubMed ID" "\n")
        print ("\npH value\tPubMed ID")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("pH value data is not available for the enzyme:" + " " + self.ec)
            f.write ("pH value data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(\S+)\t(\S+)\t(.+)", each)):
                pH=dtval[2]
                pubmedid=dtval[3]
                print (pH + "\t" + pubmedid)
                f.write (pH + "\t" + pubmedid + "\n")
        f.write ("\n")
        return ""


    def temp(self):
        f=open("Enz_temp_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=41&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&W[2]=&W[3]=&T[3]=1&W[4]=&T[4]=2&W[5]=&T[5]=2&W[6]=&T[6]=2&V[6]=1&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("Temperature" + "\t" "PubMed ID" "\n")
        print ("\nTemperature value\tPubMed ID")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("Temperature value data is not available for the enzyme:" + " " + self.ec)
            f.write ("Temperature  value data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(\S+)\t(\S+)\t(.+)", each)):
                temp=dtval[2]
                pubmedid=dtval[3]
                print (temp + "\t" + pubmedid)
                f.write (temp + "\t" + pubmedid + "\n")
        f.write ("\n")
        return ""


    def pI(self):
        f=open("Enz_pI_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=53&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=%s&T[1]=1&W[2]=&W[3]=&T[3]=1&W[4]=&T[4]=2&W[5]=&T[5]=2&V[5]=1&W[6]=&T[6]=2&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("pI value" + "\t" "PubMed ID" "\n")
        print ("\npI value\tPubMed ID")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("pI value  data is not available for the enzyme:" + " " + self.ec)
            f.write ("pI value  data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(\S+)\t(\S+)\t(.+)", each)):
                pI=dtval[2]
                pubmedid=dtval[3]
                print (pI + "\t" + pubmedid)
                f.write (pI + "\t" + pubmedid + "\n")
        f.write ("\n")
        return ""


    def org(self):
        f=open("Enz_org_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=20&RN=&RNV=&os=&pt=&FNV=&tt=&SYN=&Textmining=&W[1]=&W[2]=%s&T[2]=1&W[4]=&T[4]=2&W[5]=&T[5]=2&V[5]=1&W[6]=&T[6]=1&V[6]=&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("Organism" + "\t" "PubMed ID" "\n")
        print ("\nOrganism\tPubMed ID")
        r = requests.get(u1)
        abs = r.content.decode("utf-8")
        #print (abs)
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