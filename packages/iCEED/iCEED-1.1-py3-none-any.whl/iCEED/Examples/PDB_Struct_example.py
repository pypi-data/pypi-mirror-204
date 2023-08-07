#.......... Example code for downloading 3D structure of enzymes from PDB database ..........#

from iCEED import EC2PDB 
from iCEED import ORGEC2PDB

#Downloading the 3D structure(s) of a single enzyme using the EC number is an input.

total_struct = EC2PDB("1.1.1.1") #Providing EC number as input
print(total_struct.str()) # Calling str function and printing result


#Downloading the 3D structure(s) of multiple enzyme using the EC numbers is an input.

eclist = ["2.1.1.2","4.1.1.1","10.1.1.1"] #List of EC number
for abc in eclist:
    print (abc,"\n")
    total_struct = EC2PDB(abc)
    pout=total_struct.str()
    print (pout)


#Downloading 3D structure(s) of an enzyme from a specific organism using taxonomic ID

orgst = ORGEC2PDB("1.1.1.1", "9606")#Providing EC number and taxonomic ID as input
print(orgst.orgstr())# Calling orgstr function and printing result
