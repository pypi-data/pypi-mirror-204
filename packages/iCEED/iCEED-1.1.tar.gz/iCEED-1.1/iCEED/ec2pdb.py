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


class EC2PDB:
    def __init__(self, ec):
        self.ec = ec

    def str(self):
        f=open(r"Enz_Str_%s.txt" %jobid,"a")
        allres = []
        u1 = "https://search.rcsb.org/rcsbsearch/v2/query?json=%7B%22query%22%3A%7B%22type%22%3A%22terminal%22%2C%22label%22%3A%22text%22%2C%22service%22%3A%22text%22%2C%22parameters%22%3A%7B%22attribute%22%3A%22rcsb_polymer_entity.rcsb_ec_lineage.id%22%2C%22operator%22%3A%22in%22%2C%22negation%22%3Afalse%2C%22value%22%3A%5B%22"
        u2 = "%22%5D%7D%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22paginate%22%3A%7B%22start%22%3A0%2C%22rows%22%3A1000%7D%2C%22results_content_type%22%3A%5B%22experimental%22%5D%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22rcsb_entry_info.resolution_combined%22%2C%22direction%22%3A%22asc%22%7D%5D%2C%22scoring_strategy%22%3A%22combined%22%7D%7D"
        curl = u1 + self.ec + u2
        f.write ("Enzyme (EC number): " + self.ec + "\n")
        r = requests.get(curl)
        abs = r.content
        contlen = len(abs)
        if contlen == 0:
            print ("There is no structure/s in the PDB database for enzyme %s: " %self.ec, "\n")
            f.write ("There is no structure/s in the PDB database for enzyme %s: " %self.ec + "\n")
        if (pnm := re.findall(r"\"total_count\" \: (\d+)\,", abs.decode())):
            print ("Total structure found in PDB database for enzyme %s: " %self.ec, pnm[0], "\n")
            f.write ("Total structure found in PDB database for enzyme %s: " %self.ec + pnm[0] + "\n")
        if (pnm := re.findall(r"\"identifier\" \: \"(\S+)\"", abs.decode())):
            for pdbid in pnm:
                csu1 = "https://data.rcsb.org/graphql?query=%7B%0A%20%20entries(entry_ids%3A%20%5B%22"
                csu2 = "%22%5D)%0A%20%20%7B%0A%20%20%20%20rcsb_id%0A%20%20%20%20rcsb_entry_container_identifiers%20%7B%0A%20%20%20%20%20%20entry_id%0A%20%20%20%20%7D%0A%20%20%20%20rcsb_entry_info%20%7B%0A%20%20%20%20%20%20resolution_combined%0A%20%20%20%20%7D%0A%20%20%20%20struct%20%7B%0A%20%20%20%20%20%20title%0A%20%20%20%20%7D%0A%20%20%20%20polymer_entities%20%7B%0A%20%20%20%20%20%20rcsb_entity_source_organism%20%7B%0A%20%20%20%20%20%20%20%20ncbi_scientific_name%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D"
                csrpurl = csu1 + pdbid + csu2
                rp = requests.get(csrpurl)
                rpres = rp.content.decode("utf-8")
                if (dtval := re.match(r"\{\"data\"\:\{\"entries\"\:\[\{\"rcsb_id\"\:\"(\S+)\",\"rcsb_entry_container_identifiers\"\:\{\"entry_id\"\:\"\S+\"\},\"rcsb_entry_info\"\:\{\"resolution_combined\"\:\[(\S+)\]\},\"struct\"\:\{\"title\"\:\"(.+)\"\},\"polymer_entities\"\:\[\{\"rcsb_entity_source_organism\"\:\[\{\"ncbi_scientific_name\"\:\"(.+)\"\}\]\}\]\}\]\}\}", rpres)):
                    id = dtval.group(1)
                    resolution = dtval.group(2)
                    strttl = dtval.group(3)
                    scorg = dtval.group(4)
                    scorg = re.sub(r"\"\}\]\}\,\{\"rcsb_entity_source_organism\".+", "", scorg)
                    scorg = re.sub(r"\:\[\{\"ncbi_scientific_name.+", "", scorg)
                    scorg = re.sub(r"\"\},\{\"ncbi_scientific_name.+", "", scorg)
                    cmbres = id + "\t" + resolution + "\t" + strttl + "\t" + scorg
                    print (cmbres)
                    f.write (cmbres + "\n")
            f.write ("\n")
        return ""


class ORGEC2PDB:
    def __init__(self, ec,taxid):
        self.ec = ec
        self.taxid = taxid

    def orgstr(self):
        f=open(r"Enz_OrgStr_%s.txt" %jobid,"w")
        allres = []
        u1 = "https://search.rcsb.org/rcsbsearch/v2/query?json=%7B%22query%22%3A%7B%22type%22%3A%22group%22%2C%22logical_operator%22%3A%22and%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22parameters%22%3A%7B%22attribute%22%3A%22rcsb_polymer_entity.rcsb_ec_lineage.id%22%2C%22operator%22%3A%22in%22%2C%22negation%22%3Afalse%2C%22value%22%3A%5B%22"
        u2 = "%22%5D%7D%7D%2C%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22parameters%22%3A%7B%22attribute%22%3A%22rcsb_entity_source_organism.taxonomy_lineage.id%22%2C%22operator%22%3A%22exact_match%22%2C%22negation%22%3Afalse%2C%22value%22%3A%22"
        u3 = "%22%7D%7D%5D%2C%22label%22%3A%22text%22%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22paginate%22%3A%7B%22start%22%3A0%2C%22rows%22%3A1000%7D%2C%22results_content_type%22%3A%5B%22experimental%22%5D%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22rcsb_entry_info.resolution_combined%22%2C%22direction%22%3A%22asc%22%7D%5D%2C%22scoring_strategy%22%3A%22combined%22%7D%7D"
        curl = u1 + self.ec + u2 + self.taxid + u3
        f.write ("Enzyme (EC number): " + self.ec + "\n" + "Taxonomy ID: " + self.taxid + "\n")
        print ("Taxonomy ID: " + self.taxid + "\n")
        r = requests.get(curl)
        abs = r.content
        contlen = len(abs)
        if contlen == 0:
            print ("There is no structure/s in the PDB database", "\n")
            f.write ("There is no structure/s in the PDB database" + "\n")
        if (pnm := re.findall(r"\"total_count\" \: (\d+)\,", abs.decode())):
            print ("Total structure found in PDB database: ", pnm[0], "\n")
            f.write ("Total structure found in PDB database: " + pnm[0] + "\n")
        if (pnm := re.findall(r"\"identifier\" \: \"(\S+)\"", abs.decode())):
            for pdbid in pnm:
                csu1 = "https://data.rcsb.org/graphql?query=%7B%0A%20%20entries(entry_ids%3A%20%5B%22"
                csu2 = "%22%5D)%0A%20%20%7B%0A%20%20%20%20rcsb_id%0A%20%20%20%20exptl%20%7B%0A%20%20%20%20%20%20method%0A%20%20%20%20%7D%0A%20%20%20%20rcsb_entry_info%20%7B%0A%20%20%20%20%20%20resolution_combined%0A%20%20%20%20%7D%0A%20%20%20%20struct%20%7B%0A%20%20%20%20%20%20title%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D"
                csrpurl = csu1 + pdbid + csu2
                rp = requests.get(csrpurl)
                rpres = rp.content.decode("utf-8")
                if (dtval := re.match(r"\{\"data\"\:\{\"entries\"\:\[\{\"rcsb_id\"\:\"(\S+)\",\"exptl\"\:\[\{\"method\"\:\"(.+)\"\}\],\"rcsb_entry_info\"\:\{\"resolution_combined\"\:\[(\S+)\]\},\"struct\"\:\{\"title\"\:\"(.+)\"\}\}\]\}\}", rpres)):
                    #print (dtval.group(4))
                    id = dtval.group(1)
                    method = dtval.group(2)
                    resolution = dtval.group(3)
                    strttl = dtval.group(4)
                    #scorg = re.sub(r"\"\}\]\}\,\{\"rcsb_entity_source_organism\".+", "", scorg)
                    #scorg = re.sub(r"\:\[\{\"ncbi_scientific_name.+", "", scorg)
                    #scorg = re.sub(r"\"\},\{\"ncbi_scientific_name.+", "", scorg)
                    cmbres = id + "\t" + method + "\t" + resolution + "\t" + strttl
                    #cmbres = id + "\t"
                    print (cmbres)
                    f.write (cmbres + "\n")
            f.write ("\n")
        return ""
