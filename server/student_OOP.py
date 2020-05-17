# -*- coding: utf-8 -*-


class Student:
    def __init__(self, surname, name, patr, login, password, c, group, subgroup):
        self.surname = surname
        self.name = name
        self.patronym = patr
        self.__login = login
        self.__password = password
        self.course = c
        self.group = group
        self.subgroup = subgroup

    def your_login_password(self, login, password):
        if self.__login == login and self.__password == password:
            return True
        return False

    def say_fio_course(self):
        return self.surname + " " + \
               self.name + " " + \
               self.patronym + "\n" + \
               "Студент бакалавриата " + \
               self.course + " курс"

    def say_fio(self):
        return self.surname + " " + self.name + " " + self.patronym

    def say_surname(self):
        return self.surname
