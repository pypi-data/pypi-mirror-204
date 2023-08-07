#.......... Example code for downloading physico-chemical parameters of enzyme..........#

from iCEED import EC2PARAM

#Downloading km value of a single enzyme using the EC number is an input.

total_km = EC2PARAM("1.1.1.1") #Providing EC number as input
print(total_km.kmv()) # Calling kmv function and printing result


#Downloading ki value of a single enzyme using the EC number is an input.

total_ki = EC2PARAM("1.1.1.1")#Providing EC number as input
print(total_ki.kiv())# Calling kiv function and printing result

#Downloading ic50 value of a single enzyme using the EC number is an input.

total_ic = EC2PARAM("1.1.1.1")#Providing EC number as input
print(total_ic.ic50())# Calling ic50 function and printing result

#Downloading pH value of a single enzyme using the EC number is an input.

total_pH = EC2PARAM("1.1.1.1")#Providing EC number as input
print(total_pH.pH())# Calling pH function and printing result

#Downloading temperature value of a single enzyme using the EC number is an input.

total_temp = EC2PARAM("1.1.1.1")#Providing EC number as input
print(total_temp.temp())# Calling temp function and printing result


#Downloading pI value of a single enzyme using the EC number is an input.

total_pI = EC2PARAM("1.1.1.1")#Providing EC number as input
print(total_pI.pI())# Calling pI function and printing result
