# -*- coding: utf-8 -*-

class Discipline():  # можно и препода добавить
    def __init__(self, name, course, cr, file):
        self.name = name
        self.course = course
        self.credits = cr
        self.__vedomost = file  # файл с оценками
        
    def say_name(self):
        return(self.name)
    
    def say_credits(self):
        return(self.credits)
        
    def find_mark(self, student):
        f = open(self.__vedomost)
        text = f.read().splitlines()
        for line in text:
            if student in line:
                mark = line[-2:]
                if mark != "10":
                    mark = mark[-1]
                break
        f.close()
        return(mark)

