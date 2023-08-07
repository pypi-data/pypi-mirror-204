#.......... Example code for downloading smallmolecule data of enzyme..........#

from iCEED import EC2MOL

#Downloading substrate and product data of a single enzyme using the EC number is an input.

total_subpr = EC2MOL("1.1.1.1") #Providing EC number as input
print(total_subpr.subpr()) # Calling subpr function and printing result


#Downloading cofactor data of a single enzyme using the EC number is an input.

total_cof = EC2MOL("1.1.1.1")#Providing EC number as input
print(total_cof.cof())# Calling cof function and printing result

#Downloading metal and ion data of a single enzyme using the EC number is an input.

total_metion = EC2MOL("1.1.1.1")#Providing EC number as input
print(total_metion.metion())# Calling metion function and printing result

#Downloading inhibitor data of a single enzyme using the EC number is an input.

total_inhib = EC2MOL("1.1.1.1")#Providing EC number as input
print(total_inhib.inhib())# Calling inhib function and printing result

#Downloading activating compound data of a single enzyme using the EC number is an input.

total_actcpd = EC2MOL("1.1.1.1")#Providing EC number as input
print(total_actcpd.actcpd())# Calling actcpd function and printing result
