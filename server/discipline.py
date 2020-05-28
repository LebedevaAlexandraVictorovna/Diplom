# -*- coding: utf-8 -*-

import boto3

#########

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

    return component.read()


class Resource:

    def aws(self):
        s3 = boto3.resource('s3')
        return s3
    
    def bucket(self, bucket_name) -> Bucket:
        bucket = Bucket(self.aws(), bucket_name)
        return bucket

########

class Discipline:  # можно и препода добавить
    def __init__(self):
        self.name = "Название дисциплины"
        self.course = 0  # на каком курсе проходят дисциплину
        self.credits = 5
        self.__vedomost = ""  # файл с оценками

    # setters
    def set_name(self, name):
        self.name = name

    def set_course(self, course):
        self.course = course

    def set_credits(self, credit):
        self.credits = credit

    def set_vedomost(self, ved):
        self.__vedomost = ved

    # getters
    def get_name(self):
        return self.name

    def get_course(self):
        return self.course

    def get_credits(self):
        return self.credits

    def get_vedomost(self):
        return self.__vedomost
    
    '''

    # нормальные методы
    def find_mark(self, student):
        s3 = boto3.resource('s3')
        obj3 = s3.Object('liststudentsadmins', self.get_vedomost())
        text = obj3.get()['Body'].read().decode('utf-8').splitlines()
        mark = "0"
        for line in text:
            if student in line:
                mark = line[-2:]
                if mark != "10":
                    mark = mark[-1]
                break
        return mark
    '''

    def find_mark(self, student):
        resource = Resource()
        bucket = resource.bucket('liststudentsadmins')
        ocket_1 = bucket.ocket(self.get_vedomost())
        decorator1 = DecodeDecorator(ocket_1)
        decorator2 = SplitlinesDecorator(decorator1)
        text = client_code(decorator2)
        for line in text:
            if student in line:
                mark = line[-2:]
                if mark != "10":
                    mark = mark[-1]
                break
        return(mark)
