#.......... Example code for downloading Nucleotide and Protein sequence data of enzyme..........#

from iCEED import NucEC2SEQ
from iCEED import ProtEC2SEQ

#Get the nucleotide sequence of an enzyme from a certain organism using the EC number and Taxonomy ID as input.

nseq = NucEC2SEQ("9606", "1.1.1.1")#Providing Taxonomy ID and EC number as input
print(nseq.nucseq())# Calling nucseq function and printing result


#Get the protein sequence of an enzyme from a certain organism using the EC number and Taxonomy ID as input.

prseq = ProtEC2SEQ("1.1.1.1", "9606")#Providing EC number and taxonomy ID as input
print(prseq.protseq())# Calling domfam function and printing result

