#.......... Example code for downloading research articles from PUBMED database ..........#

from iCEED import EC2PUB 
from iCEED import EC2PUBSO

#Downloading the articles of a single enzyme using the EC number is an input.

total_articles = EC2PUB("1.1.1.1") #Providing EC number as input
print(total_articles.pub()) # Calling pub function and printing result


#Downloading articles of an enzyme from a specific organism using taxonomic ID

org_art = EC2PUBSO("1.1.1.100", "9606")#Providing EC number and taxonomic ID as input
print(org_art.pubso())# Calling pubso function and printing result
