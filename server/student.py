# -*- coding: utf-8 -*-

from server.administrator import Administrator


class Student(Administrator):
    def __init__(self):
        #self.surname = "Фамилия"
        #self.name = "Имя"
        #self.patronym = "Отчество"
        #self.login = "fio"
        #self.__password = "0000"
        self.course = 1
        self.group = "БИВ000"
        self.subgroup = 1

    # setters

    #def set_surname(self, sur):
        #self.surname = sur

    #def set_name(self, name):
        #self.name = name

    #def set_patronym(self, pat):
        #self.patronym = pat

    def set_login(self, login):
        self.login = login

    #def set_password(self, password):
        #self.__password = password

    def set_course(self, course):
        self.course = course

    def set_group(self, group):
        self.group = group

    def set_subgroup(self, subgroup):
        self.subgroup = subgroup

    # getters

    #def get_surname(self):
        #return self.surname

    #def get_patronym(self):
        #return self.patronym

    #def get_name(self):
        #return self.name

    #def get_login(self):
        #return self.login

    #def get_password(self):
        #return self.__password

    def get_course(self):
        return self.course

    def get_group(self):
        return self.group

    def get_subgroup(self):
        return self.subgroup
