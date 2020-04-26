# -*- coding: utf-8 -*-

class Student():
    def __init__(self):
        self.surname = "Фамилия"
        self.name = "Имя"
        self.patronim = "Отчество"
        self.login = "fio"
        self.password = "0000"
        self.course = 1
        self.group = "БИВ000"
        self.subgroup = 1
    
    #setters
    
    def set_surname(self, sur):
        self.surname = sur

    def set_name(self, name):
        self.name = name
    
    def set_patronim(self, pat):
        self.patronim = pat
    
    def set_login(self, login):
        self.login = login

    def set_password(self, password):
        self.password = password 
    
    def set_course(self, course):
        self.course = course
    
    def set_group(self, group):
        self.group = group
    
    def set_subgroup(self, subgroup):
        self.subgroup = subgroup
    
    # getters
    
    def get_surname(self):
        return(self.surname)
    
    def get_patronim(self):
        return(self.patronim)

    def get_name(self):
        return(self.name)
    
    def get_login(self):
        return(self.login)

    def get_password(self):
        return(self.password)
    
    def get_course(self):
        return(self.course)

    def get_group(self):
        return(self.group)
    
    def get_subgroup(self):
        return(self.subgroup)
