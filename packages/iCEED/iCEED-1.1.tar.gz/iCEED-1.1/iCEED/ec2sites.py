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


class EC2SITE:
    def __init__(self, ec):
        self.ec = ec

    def act(self):
        f=open(r"Enz_Act_%s.txt" %jobid,"a")
        allres = []
        sites = []
        u1 = "https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%28ec%3A"
        u2 = "%29&size=500&fields=accession,ft_act_site&format=tsv"
        curl = u1 + self.ec + u2
        #print (curl)
        f.write ("Enzyme (EC number): " + self.ec + "\n\n")
        f.write ("Acceesion number" + "\t" + "Amino acid residue number" + "\t" + "Description" + "\n")
        r = requests.get(curl)
        abs = r.content.decode("utf-8")
        allres = abs.split("\n")
        ctln = len(allres)
        if ctln <=2:
            print ("Active site data is not available")
        for each in allres:
            each = re.sub('^Entry.+', '', each)
            if (dtval := re.match(r"(\w+)\tACT_SITE (\d+)\; \/note\=\"(.+)\"\;", each)):
                acno = dtval.group(1)
                aano = dtval.group(2)
                des = dtval.group(3)
                des = re.sub('\"\; \/evidence.+', '', des)
                cmp = acno + "\t" + aano + "\t" + des
                sites.append(cmp)
        unst = set(sites)
        for est in unst:
                print (est)
                f.write (est + "\n")
        return ""

    def site(self):
        f=open(r"Enz_Site_%s.txt" %jobid,"a")
        allres = []
        sites = []
        u1 = "https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%28ec%3A"
        u2 = "%29&size=500&fields=accession,ft_site&format=tsv"
        curl = u1 + self.ec + u2
        f.write ("Enzyme (EC number): " + self.ec + "\n\n")
        f.write ("Acceesion number" + "\t" + "Amino acid residue number" + "\t" + "Description" + "\n")
        r = requests.get(curl)
        abs = r.content.decode("utf-8")
        allres = abs.split("\n")
        ctln = len(allres)
        if ctln <=2:
            print ("Site data is not available")
        for each in allres:
            each = re.sub('^Entry.+', '', each)
            if (dtval := re.match(r"(\w+)\tSITE (\d+)\; \/note\=\"(.+)\"\;", each)):
                acno = dtval.group(1)
                aano = dtval.group(2)
                des = dtval.group(3)
                des = re.sub('\"\; \/evidence.+', '', des)
                cmp = acno + "\t" + aano + "\t" + des
                sites.append(cmp)
        unst = set(sites)
        for est in unst:
                print (est)
                f.write (est + "\n")
        return ""
