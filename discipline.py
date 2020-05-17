# -*- coding: utf-8 -*-


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

    # нормальные методы
    def find_mark(self, student):
        f = open(self.get_vedomost(), encoding="utf8")
        text = f.read().splitlines()
        for line in text:
            if student in line:
                mark = line[-2:]
                if mark != "10":
                    mark = mark[-1]
                break
        f.close()
        return mark
