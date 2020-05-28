# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import random
import boto3

class Okt():  # ocket interface
    def read(self):
        pass


class Ocket(Okt):
    def __init__(self, resrc, bucket_name, file_name):
        self.resrc = resrc
        self.bucket_name = bucket_name
        self.file_name = file_name
        self.obj = self.resrc.Object(self.bucket_name, self.file_name)
    
    def read(self):
        return self.obj.get()['Body'].read()  #.decode('utf-8').splitlines()   сделать декораторы
    
    def write(self, data):
        self.obj.put(Body = data)


class Decorator(Okt):  
    """
    Базовый класс Декоратора следует тому же интерфейсу, что и другие
    компоненты. Основная цель этого класса - определить интерфейс обёртки для
    всех конкретных декораторов. Реализация кода обёртки по умолчанию может
    включать в себя поле для хранения завёрнутого компонента и средства его
    инициализации.
    """

    _component: Okt = None

    def __init__(self, component: Okt) -> None:
        self._component = component

    @property
    def component(self) -> str:
        """
        Декоратор делегирует всю работу обёрнутому компоненту.
        """

        return self._component

    def read(self) -> str:
        return self._component.read()

class DecodeDecorator(Decorator):  # read с декодом
    """
    Конкретные Декораторы вызывают обёрнутый объект и изменяют его результат
    некоторым образом.
    """

    def read(self) -> str:
        return (self.component.read()).decode('utf-8')

class SplitlinesDecorator(Decorator):

    def read(self) -> str:
        return (self.component.read()).splitlines()

class Bucket:
    def __init__(self, resrc, bucket_name):
        self.bucket_name = bucket_name
        self.resrc = resrc
    
    def name(self):
        return self.bucket_name

    def ocket(self, file_name) -> Ocket:
        ocket = Ocket(self.resrc, self.bucket_name, file_name)
        return ocket


def client_code(component: Okt) -> None:

    print(f"RESULT: {component.read()}", end="")


class Resource:

    def aws(self):
        s3 = boto3.resource('s3')
        return s3
    
    def bucket(self, bucket_name) -> Bucket:
        bucket = Bucket(self.aws(), bucket_name)
        return bucket

resource = Resource()
bucket = resource.bucket('liststudentsadmins')
ocket = bucket.ocket('list.txt')
#content = ocket.read()
#print(content)

print("Client: I've got a simple component:")
client_code(ocket)
print("\n")
decorator1 = DecodeDecorator(ocket)
decorator2 = SplitlinesDecorator(decorator1)
print("Client: Now I've got a decorated component:")
client_code(decorator2)
print("\n")