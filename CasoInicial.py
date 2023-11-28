# Este caso supone el envío de datos de un sensor a un servidor

import os

class Sensor:
    def __init__(self, sensor_id=1):
        self.sensor_id = sensor_id
        self.informe = ""

    def generar_informe_temperatura(self, temperatura):
        self.informe = f"Sensor {self.sensor_id} - Temperatura: {temperatura} grados Celsius"

    def enviar_informe(self, filename):
        with open(filename, 'w') as file:
            file.write(self.informe + '\n')
        print("\nInforme enviado:")
        print(self.informe,'\n')

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
    def recibir_informe(self, filename):
        file = open(filename, 'r') 
        informe = file.read()
        print("Informe recibido:")
        print(informe,'\n')


# Ejemplo de uso

filename = "informe_sensor_1.txt"

# Crear un sensor y generar un informe
sensor1 = Sensor()
sensor1.generar_informe_temperatura(25.5)
sensor1.enviar_informe(filename)

# Un atacante logra interceptar el informe enviado
atacante = Atacante()
atacante.interceptar_informe(filename)
atacante.modificar_informe(filename, 15.4)

# Crear un servidor y procesar los archivos
servidor = Servidor()
servidor.recibir_informe(filename)