import os
import time
import re
from itertools import permutations

##validacion de IP
def ip_valida(ip):
    regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(regex, ip) is not None

#Solicitud de datos
ip= input("ingrese su ip: ")
if not ip_valida(ip):
    print("La direccion IP no es valida. Ingrese una dirección IP correcta.")
    exit(1)

puertos= int(input("Ingrese los puertos: "))
#permutacion de puertos
lista_puertos=[int(puerto) for puerto in puertos.split()]
variaciones =list(permutations(lista_puertos))

##Ejecucion de las variaciones
for variacion in variaciones:
    puertos_str = " ".join(map(str, variacion))
    os.system(f"echo IP: {ip} - Puertos: {puertos_str}")
    os.system(f"knock {ip} {puertos_str} -v")
    os.system(f"nmap -sC -sV -Pn {ip}")
    time.sleep(2)
