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


class EC2DOMFAM:
    def __init__(self, ec):
        self.ec = ec

    def domfam(self):
        f=open(r"Enz_FamDom_%s.txt" %jobid,"a")
        allres = []
        tabsep = []
        intpr = []
        pfm = []
        prdm = []
        prst = []
        s = ""
        u1 = "https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%28ec%3A"
        u2 = "%29&size=500&fields=accession,xref_interpro,xref_pfam,xref_prosite"
        curl = u1 + self.ec + u2
        #print (curl)
        f.write ("Domain and Family data" + "\n")
        f.write ("Enzyme (EC number): " + self.ec + "\n\n")
        r = requests.get(curl)
        abs = r.content.decode("utf-8")
        allres = abs.split("\n")
        ctln = len(allres)
        if ctln <=2:
            print ("Domain and family data is not available")
        for each in allres:
            if (dtval := re.match(r".+\"database\":\"InterPro\",\"id\":\"(\w+)\",\"properties\":\[\{\"key\":\"EntryName\",\"value\":\"(\w+)\"", each)):
                inpid = dtval.group(1)
                inpvl = dtval.group(2)
                inpcp = inpid + "-" + inpvl
                inpcp = inpcp.strip()
                intpr.append(inpcp)
            if (dtval := re.match(r".+\"database\":\"Pfam\",\"id\":\"(\w+)\",\"properties\":\[\{\"key\":\"EntryName\",\"value\":\"(\w+)\"", each)):
                pfmid = dtval.group(1)
                pfmvl = dtval.group(2)
                pfmcp = pfmid + "-" + pfmvl
                pfmcp = pfmcp.strip()
                pfm.append(pfmcp)
            if (dtval := re.match(r".+\"database\":\"PROSITE\",\"id\":\"(\w+)\",\"properties\":\[\{\"key\":\"EntryName\",\"value\":\"(\w+)\"", each)):
                prsid = dtval.group(1)
                prsvl = dtval.group(2)
                prscp = prsid + "-" + prsvl
                prscp = prscp.strip()
                prst.append(prscp)
            tabsep = each.split("\t")
        unintpr = set(intpr)
        f.write ("INTERPRO:" + "\t")
        print(', '.join([str(upr) for upr in unintpr]))
        f.write (', '.join([str(upr) for upr in unintpr]))
        unpfm = set(pfm)
        f.write ("\n" + "PFAM:" + "\t")
        print(', '.join([str(pfm) for pfm in unpfm]))
        f.write (', '.join([str(pfm) for pfm in unpfm]))
        unprst = set(prst)
        f.write ("\n" + "PROSITE:" + "\t")
        print(', '.join([str(prst) for prst in unprst]))
        f.write (', '.join([str(prst) for prst in unprst]))
        return ""
