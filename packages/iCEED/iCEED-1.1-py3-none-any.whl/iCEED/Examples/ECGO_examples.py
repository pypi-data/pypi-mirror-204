#.......... Example code for downloading GO data of enzyme..........#

from iCEED import EC2AllGO
from iCEED import EC2SoGO

#Get the GO data of an enzyme using the EC number as input.

allgo = EC2AllGO("7.1.1.2")#Providing EC number as input
print(allgo.go())# Calling go function and printing result


#Get the protein sequence of an enzyme from a certain organism using the EC number and Taxonomy ID as input.

orggo = EC2SoGO("1.1.1.1","9606")#Providing EC number and taxonomy ID as input
print(orggo.sogo())# Calling sogo function and printing result

