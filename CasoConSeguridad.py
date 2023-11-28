from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import os

class Sensor:
    def __init__(self, sensor_id=1):
        self.sensor_id = sensor_id
        self.informe = ""

    def generar_informe_temperatura(self, temperatura):
        self.informe = f"Sensor {self.sensor_id} - Temperatura: {temperatura} grados Celsius"

    def enviar_informe(self, filename, clave_publica_servidor):
        clave_aes = get_random_bytes(16)
        cipher_aes = AES.new(clave_aes, AES.MODE_CCM, nonce=get_random_bytes(11))
        ciphertext, tag = cipher_aes.encrypt_and_digest(self.informe.encode())

        # Usar RSA para cifrar la clave AES y enviarla junto con el informe cifrado
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(clave_publica_servidor))
        enc_key = cipher_rsa.encrypt(clave_aes)

        with open(filename, 'wb') as file:
            file.write(len(enc_key).to_bytes(2, byteorder='big') + enc_key + cipher_aes.nonce + tag + ciphertext)

        print("\nInforme enviado y cifrado con AES en modo CCM.")

class Atacante:
    def __init__(self):
        self.informe = ""
        
    def interceptar_informe(self, filename):
        file = open(filename, 'r') 
        self.informe = file.read()
        print("Informe Interceptado:")
        print(self.informe)
        
    def modificar_informe(self, filename, temperatura):
        self.informe = f"Sensor 1 - Temperatura: {temperatura} grados Celsius"
        with open(filename, 'w') as file:
            file.write(self.informe + '\n')
        print("Informe Modificado:")
        print(self.informe,'\n')

class Servidor:
    def recibir_informe(self, filename, clave_privada_servidor):
        with open(filename, 'rb') as file:
            key_len = int.from_bytes(file.read(2), byteorder='big')
            enc_key = file.read(key_len)
            nonce = file.read(11)
            tag = file.read(16)
            ciphertext = file.read()

        cipher_rsa = PKCS1_OAEP.new(clave_privada_servidor)
        clave_aes = cipher_rsa.decrypt(enc_key)

        cipher_aes = AES.new(clave_aes, AES.MODE_CCM, nonce=nonce)
        try:
            informe = cipher_aes.decrypt_and_verify(ciphertext, tag)
            print("\nInforme recibido y descifrado correctamente:")
            print(informe.decode())
        except ValueError:
            print("\nError al descifrar el informe (Clave incorrecta).")

# Ejemplo de uso
if __name__ == "__main__":
    filename = "informe_sensor_1.txt"

    # Generar claves RSA para el sensor y el servidor
    clave_privada_sensor = RSA.generate(2048)
    clave_publica_sensor = clave_privada_sensor.publickey().export_key()

    clave_privada_servidor = RSA.generate(2048)
    clave_publica_servidor = clave_privada_servidor.publickey().export_key()

    # Crear un sensor y generar un informe
    sensor1 = Sensor()
    sensor1.generar_informe_temperatura(25.5)
    sensor1.enviar_informe(filename, clave_publica_servidor)
    
    # Un atacante intercepta el canal
    accion = input("lea o modifique el archivo, luego escriba 'LISTO':\n")
    

    # Crear un servidor y recibir el informe cifrado
    servidor = Servidor()
    servidor.recibir_informe(filename, clave_privada_servidor)
