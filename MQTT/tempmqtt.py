import glob
import paho.mqtt.publish as publish #Libreria de mqtt
import string
import smbus
import time
import datetime
import random
import RPi.GPIO as iO
import os
from w1thermsensor import W1ThermSensor #Libreria para el sensor de temperatura

"""Install paho-mqtt, w1thermsensor"""

def temp_mqtt_func():

    channel_ID = "1509577" #Id unico del canal extraido de Thingspeak
    mqtt_host = "mqtt3.thingspeak.com" #Nombre del host de teamspeak

    mqtt_client_ID = "JhgWCisEHiwuOCgqLBsDCiA" #Id del cliente unico para el topic
    mqtt_username = os.environ['USER_THINGSPEAK'] #Username unico de Thingspeak
    mqtt_password = os.environ['PASS_THINGSPEAK'] #Contraseña unica Thingspeak

    t_transport = "websockets" #Metodo comunicacion
    t_port = 80 #Puerto para la comunicacion

    topic = "channels/" + channel_ID + "/publish" #El topic se contruye en base al ID de canal unico

    os.system('modprobe w1-gpio') #Añadir modulo en linux de w1-gpio
    os.system('modprobe w1-therm')

    mySensor = W1ThermSensor() #Crear un objeto del sensor de temperatura

    # curGas = 20 #valor cualquiera de inicializacion 
    
    try:
         for mySensor in W1ThermSensor.get_available_sensors(): #Hace un escaneo de los sensores que puede identificar en los puertos GPIO
             curSensorID = mySensor.id #Obtiene el Id del sensor
             curTemp = mySensor.get_temperature() #Utiliza un metodo del objeto para obtener la temperatura
             curGas = random.randint(800,880)
             curTemp = round(curTemp,1) #Redondea la temperatura
             #print(f"temp: {curTemp}")
             myTimeStamp = datetime.datetime.now().strftime("%Y%m%d.%H%M%S")#Se obtiene la fehca y hora 
             print(curSensorID + " Temp = " + str(curTemp) + " at " + datetime.datetime.now().strftime("%Y-%m-%d %H%M%S"))
             payload = "field1=" + str(curTemp) + "&field2=" + str(curGas) + "&field3=" + str(myTimeStamp) # "2021-12-12-10:10" #Se construye el payload con los datos del sensor de temperatura y sensor de gas
         print("Escribiendo mensaje=", payload, "al host: ", mqtt_host, "clientID= ", mqtt_client_ID)
        
         publish.single(topic, payload, hostname=mqtt_host, transport =t_transport, port =t_port, client_id=mqtt_client_ID, auth={'username':mqtt_username, 'password':mqtt_password})#Se publica la informacion del payload hacia el servidor Thingspeak
    except (KeyboardInterrupt): #Que salga cuando exista una interrupcion de teclado
        exit()
    
    except Exception as e: #Cuando haya una excepcion donde no se pueda enviar los datos, que imprima la excepcion
         print(e)
