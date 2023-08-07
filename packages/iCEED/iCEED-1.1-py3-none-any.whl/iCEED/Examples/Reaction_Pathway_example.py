#.......... Example code for downloading reaction and pathways data of enzyme..........#

from iCEED import EC2REPATH 

#Downloading reaction data of a single enzyme using the EC number is an input.

total_rec = EC2REPATH("1.1.1.1") #Providing EC number as input
print(total_rec.rcn()) # Calling rcn function and printing result



#Downloading pathway data of a single enzyme using the EC number is an input.

total_path = EC2REPATH("1.1.1.1")#Providing EC number as input
print(total_path.pth())# Calling pth function and printing result
