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


class ProtEC2SEQ:
    def __init__(self, ec,taxid):
        self.ec = ec
        self.taxid = taxid

    def protseq(self):
        f=open(r"Enz_ProtSeq_%s.txt" %jobid,"a")
        u1 = "https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%20AND%20(ec:"
        u2 = ")%20AND%20(taxonomy_id:"
        u3 = ")&format=fasta"
        curl = u1 + self.ec + u2 + self.taxid + u3
        f.write ("Protein sequences" + "\n")
        f.write ("Enzyme (EC number): " + self.ec + "\n\n")
        r = requests.get(curl)
        abs = r.content.decode("utf-8")
        allres = abs.split("\n")
        cnln = len(allres)
        if cnln == 1:
            print ("Protein sequence/s are not available")
        print (abs)
        f.write (abs)
        return ""


class NucEC2SEQ:
    def __init__(self,taxid,ec):
        self.taxid = taxid
        self.ec = ec

    def nucseq(self):
        f=open(r"Enz_NucSeq_%s.txt" %jobid,"a")
        u1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nuccore&term=txid"
        u2 = "[Organism:noexp]%20AND%20("
        u3 = "[EC/RN%20Number])&retmax=1000"
        curl = u1 + self.taxid + u2 + self.ec + u3
        f.write ("Nucleotide sequences" + "\n")
        f.write ("Enzyme (EC number): " + self.ec + "\t" + "Organism: " + self.taxid + "\n\n")
        r = requests.get(curl)
        abs = r.content.decode("utf-8")
        allres = abs.split("\n")
        s = ""
        for each in allres:
            each = each.strip()
            s += each
        if (dtval := re.match(r".+<Count>0<\/Count>", s)):
            print ("Nucleotide sequnece/s are not available")
        if (dtval := re.findall(r"\<Id\>\d+\<\/Id\>", s)):
            for ids in dtval:
                ids = re.sub('<Id>', '', ids)
                ids = re.sub('</Id>', '', ids)
                url2 ="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=%s&rettype=fasta&retmode=text" %ids
                rs = requests.get(url2)
                seq = rs.content.decode("utf-8")
                print (seq)
                f.write(seq)
        return ""
