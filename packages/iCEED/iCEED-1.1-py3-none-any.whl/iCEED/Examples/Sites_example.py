#.......... Example code for downloading sites and active sites data of enzyme..........#

from iCEED import EC2SITE

#Downloading active site data of a single enzyme using the EC number is an input.

total_as = EC2SITE("1.1.1.1") #Providing EC number as input
#print(total_as.act()) # Calling act function and printing result



#Downloading site data of a single enzyme using the EC number is an input.

total_st = EC2SITE("1.1.1.1")#Providing EC number as input
print(total_st.site())# Calling site function and printing result
