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


class EC2PUBSO:
    def __init__(self, ec,taxid):
        self.ec = ec
        self.taxid = taxid

    def pubso(self):
        f=open(r"Enz_PUBSO_%s.txt" %jobid,"a")
        allres = []
        pubsid = []
        u1 = "https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%28ec%3A"
        u2 = "%29%20AND%20%28organism_id%3A"
        u3 = "%29&fields=accession,lit_pubmed_id&format=tsv"
        curl = u1 + self.ec + u2 + self.taxid + u3
        f.write ("Enzyme (EC number): " + self.ec + "\t" + "Taxonomy ID: " + self.taxid + "\n")
        f.write ("PubMed ID" + "\t" "Title" + "\n")
        print("PubMed ID\tTitle\n")
        r = requests.get(curl)
        abs = r.content.decode("utf-8")
        allres = abs.split("\n")
        cnln = len(allres)
        if cnln < 3:
            print ("Articles not found in PubMed Database")
        for each in allres:
            each = re.sub('^Entry.+', '', each)
            if (dtval := re.match(r"(.+)\t(.+)", each)):
                pbid = dtval[2]
                pubsid = pbid.split(";")
                for lid in pubsid:
                    lid = re.sub(' ', '', lid)
                    lid = re.sub('PubMedID', '', lid)
                    pubmedurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=%s&retmode=xml"%lid
                    rs = requests.get(pubmedurl)
                    pubct = rs.content.decode("utf-8")
                    if (pbval := re.findall(r"<ArticleTitle>(.+)</ArticleTitle>", pubct)):
                        pbval = pbval[0]
                        print (lid + "\t" + pbval)
                        f.write (lid + "\t" + pbval + "\n")
        return ""


class EC2PUB:
    def __init__(self, ec):
        self.ec = ec

    def pub(self):
        f=open("Enz_Pub_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://www.brenda-enzymes.org/result_download.php?a=30&RN=&RNV=&os=1&pt=&FNV=&tt=&SYN=&Textmining=&T[0]=2&W[1]=%s&T[1]=2&W[2]=&T[2]=2&W[3]=&T[3]=2&W[4]=&T[4]=2&W[5]=&T[5]=2&W[6]=&T[6]=2&V[6]=1&W[7]=&T[7]=2&W[8]=&T[8]=1&W[9]=&T[9]=2&W[11]=&T[11]=1&V[11]=1&W[12]=&T[12]=1&V[12]=&nolimit=1" %self.ec
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        f.write ("PubMed ID" + "\t" "Title" + "\n")
        print("PubMed ID\tTitle\n")
        r = requests.get(u1)
        abs = r.content.decode(errors='replace')
        if (pnm := re.findall(r"Nothing	in	this	file", abs)):
            print ("Articles are not available in the PubMed database for the enzyme:" + " " + self.ec)
            f.write ("Ki data is not available for the enzyme:" + " " + self.ec + "\n")
        allres = abs.split("\n")
        for each in allres:
            each = re.sub('Nothing	in	this	file', '', each)
            if (dtval := re.match(r"(\S+)\t(.+)\t(.+)\t\S+(uid=\d+)\S+", each) or re.match(r"(\S+)\t(.+)\t(.+)\t(\-)", each)):
                ttl=dtval[2]
                pbid=dtval[4]
                pbid = re.sub('uid\=', '', pbid)
                print (pbid + "\t" + ttl)
                f.write (pbid + "\t" + ttl + "\n")
        f.write ("\n")
        return ""