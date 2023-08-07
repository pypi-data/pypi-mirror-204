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

#https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%20AND%20(ec:"1.1.1.1")%20&size=500&fields=accession,go_p,go_c,go_f

class EC2AllGO:
    def __init__(self, ec):
        self.ec = ec

    def go(self):
        f=open(r"Enz_FamDom_%s.txt" %jobid,"a")
        allres = []
        tabsep = []
        bp = []
        cc = []
        mf = []
        s = ""
        u1 = "https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%20AND%20(ec:"
        u2 = ")%20&size=500&fields=accession,go_p,go_c,go_f"
        curl = u1 + self.ec + u2
        f.write ("Gene Ontology data" + "\n")
        f.write ("Enzyme (EC number): " + self.ec + "\n\n")
        r = requests.get(curl)
        abs = r.content.decode("utf-8")
        #print (abs)
        allres = abs.split("},{")
        ctln = len(allres)
        if ctln <=2:
            print ("Gene Ontology data is not available")
        for each in allres:
            #print (each)
            if (dtval := re.match(r".+\"GO\",\"id\":\"GO:(\d+)\",\"properties\":\[\{\"key\":\"GoTerm\",\"value\":\"C:(.+)\"", each)):
                goid = dtval.group(1)
                govl = dtval.group(2)
                gocp = goid + "-" + govl
                gocp = gocp.strip()
                #print(gocp)
                cc.append(gocp)
            if (dtval := re.match(r".+\"GO\",\"id\":\"GO:(\d+)\",\"properties\":\[\{\"key\":\"GoTerm\",\"value\":\"F:(.+)\"", each)):
                goid = dtval.group(1)
                govl = dtval.group(2)
                gocp = goid + "-" + govl
                gocp = gocp.strip()
                #print(gocp)
                mf.append(gocp)
            if (dtval := re.match(r".+\"GO\",\"id\":\"GO:(\d+)\",\"properties\":\[\{\"key\":\"GoTerm\",\"value\":\"P:(.+)\"", each)):
                goid = dtval.group(1)
                govl = dtval.group(2)
                gocp = goid + "-" + govl
                gocp = gocp.strip()
                #print(gocp)
                bp.append(gocp)
            #tabsep = each.split("\t")
        uncc = set(cc)
        f.write ("Cellular component:" + "\n" + "GO ID-GO Term:" + "\n")
        print ("\nCellular component:\n")
        for upr in uncc:
            print (upr)
            f.write (upr + "\n")
        unmf = set(mf)
        f.write ("\n" + "Molecular function:" + "\n" + "GO ID-GO Term:" + "\n")
        print ("\nMolecular function:\n")
        for umf in unmf:
            print (umf)
            f.write (umf + "\n")
        unbp = set(bp)
        f.write ("\n" + "Biological process:" + "\n" + "GO ID-GO Term:" + "\n")
        print ("\nBiological process:\n")
        for ubp in unbp:
            print (ubp)
            f.write (ubp + "\n")
        return ""


class EC2SoGO:
    def __init__(self, ec, taxid):
        self.ec = ec
        self.taxid = taxid

    def sogo(self):
        f=open(r"Enz_FamDom_%s.txt" %jobid,"a")
        allres = []
        tabsep = []
        bp = []
        cc = []
        mf = []
        s = ""
        u1 = "https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%20AND%20(ec:"
        u2 = ")%20AND%20(taxonomy_id:"
        u3 = ")&size=500&fields=accession,go_p,go_c,go_f"
        curl = u1 + self.ec + u2 + self.taxid + u3
        f.write ("Gene Ontology data" + "\n")
        f.write ("Enzyme (EC number): " + self.ec + "\t" + "Organism: " + self.taxid + "\n\n")
        r = requests.get(curl)
        abs = r.content.decode("utf-8")
        #print (abs)
        allres = abs.split("},{")
        ctln = len(allres)
        if ctln <=2:
            print ("Gene Ontology data is not available")
        for each in allres:
            #print (each)
            if (dtval := re.match(r".+\"GO\",\"id\":\"GO:(\d+)\",\"properties\":\[\{\"key\":\"GoTerm\",\"value\":\"C:(.+)\"", each)):
                goid = dtval.group(1)
                govl = dtval.group(2)
                gocp = goid + "-" + govl
                gocp = gocp.strip()
                #print(gocp)
                cc.append(gocp)
            if (dtval := re.match(r".+\"GO\",\"id\":\"GO:(\d+)\",\"properties\":\[\{\"key\":\"GoTerm\",\"value\":\"F:(.+)\"", each)):
                goid = dtval.group(1)
                govl = dtval.group(2)
                gocp = goid + "-" + govl
                gocp = gocp.strip()
                #print(gocp)
                mf.append(gocp)
            if (dtval := re.match(r".+\"GO\",\"id\":\"GO:(\d+)\",\"properties\":\[\{\"key\":\"GoTerm\",\"value\":\"P:(.+)\"", each)):
                goid = dtval.group(1)
                govl = dtval.group(2)
                gocp = goid + "-" + govl
                gocp = gocp.strip()
                #print(gocp)
                bp.append(gocp)
            #tabsep = each.split("\t")
        uncc = set(cc)
        f.write ("Cellular component:" + "\n" + "GO ID-GO Term:" + "\n")
        print ("\nCellular component:\n")
        for upr in uncc:
            print (upr)
            f.write (upr + "\n")
        unmf = set(mf)
        f.write ("\n" + "Molecular function:" + "\n" + "GO ID-GO Term:" + "\n")
        print ("\nMolecular function:\n")
        for umf in unmf:
            print (umf)
            f.write (umf + "\n")
        unbp = set(bp)
        f.write ("\n" + "Biological process:" + "\n" + "GO ID-GO Term:" + "\n")
        print ("\nBiological process:\n")
        for ubp in unbp:
            print (ubp)
            f.write (ubp + "\n")
        return ""