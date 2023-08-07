#.......... Example code for downloading organisms list from which enzyme is characterized ..........#

from iCEED import EC2SORG 

#Downloading the organisms list from which enzyme is characterized using the EC number is an input.

total_org = EC2SORG("1.1.1.1") #Providing EC number as input
print(total_org.org()) # Calling org function and printing result


