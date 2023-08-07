#.......... Example code for downloading Domain and Family data of enzyme..........#

from iCEED import EC2DOMFAM

#Downloading Domain and Family data of an enzyme using the EC number is an input.

total_domfam = EC2DOMFAM("1.1.1.1") #Providing EC number as input
print(total_domfam.domfam()) # Calling domfam function and printing result
