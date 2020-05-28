# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import random
import boto3


class Ocket:
    def __init__(self, resrc, bucket_name, file_name):
        self.resrc = resrc
        self.bucket_name = bucket_name
        self.file_name = file_name
        self.obj = self.resrc.Object(self.bucket_name, self.file_name)
    
    def read(self):
        return self.obj.get()['Body'].read()  #.decode('utf-8').splitlines()   сделать декораторы
    
    def write(self, data):
        self.obj.put(Body = data)


class Bucket:
    def __init__(self, resrc, bucket_name):
        self.bucket_name = bucket_name
        self.resrc = resrc
    
    def name(self):
        return self.bucket_name

    def ocket(self, file_name) -> Ocket:
        ocket = Ocket(self.resrc, self.bucket_name, file_name)
        return ocket


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
content = ocket.read()
print(content)
