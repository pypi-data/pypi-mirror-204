#.......... Example code for downloading synonyms for enzyme ..........#

from iCEED import EC2SYN

#Downloading the organisms list from which enzyme is characterized using the EC number is an input.

total_syn = EC2SYN("1.1.1.1") #Providing EC number as input
print(total_syn.syn()) # Calling syn function and printing result
