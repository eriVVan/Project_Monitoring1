import paho.mqtt.client as mqtt
from django.http import JsonResponse
from django.urls import path, include
from django.contrib import admin
from django.db import models
from django.conf import settings

mqtt_broker_address = "broker.example.com"     
mqtt_broker_port = 1883                             #В данных указать mqtt сервер для получения данных

def on_connect(client, userdata, flags, rc): 
    print("Connected with result code " + str(rc))
    client.subscribe("cash_terminal_data")          #подключение к терминалу


def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode('utf-8'))


def get_cash_terminal_data(request):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker_address, mqtt_broker_port, 60)
    client.loop_start()
    client.publish("cash_terminal_request", "Get data")
    return JsonResponse({"message": "Request sent to get cash terminal data"}) #Получение данны со сканера в виде сообщения на сервер


urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
]


class ModelName(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100) #сортировка данных для двух модулей терминала


def write_model_data_to_file():
    with open(settings.BASE_DIR + '/output.txt', 'w') as file:
        objects = ModelName.objects.all()
        for obj in objects:
            file.write(f'{obj.field1} {obj.field2}\n')


write_model_data_to_file()
