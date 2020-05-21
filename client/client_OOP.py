# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


def isalpha_ru(string):
    flag = True
    for c in string:
        if c < 'А' or c > 'я':
            flag = False
    return flag


def input_course():
    while True:
        try:
            course = int(input())
            if 0 < course < 5:  # бакалавриат
                break
            else:
                print("Введено неправильное значение. Попробуйте еще раз")
        except (ValueError, NameError):
            print("Введено неправильное значение. Попробуйте еще раз")
    return course


def input_group():
    while True:
        try:
            group = input()
            if (group[:3].isalpha() or isalpha_ru(group[:3])) and group[3:].isdigit() and len(
                    group) == 6:
                break
            else:
                print("Введите строку, состоящую из трех букв и трех цифр. Например, бив162")
        except ValueError:
            print("Введите строку, состоящую из трех букв и трех цифр. Например, бив162")
    return group


def input_subgroup():
    while True:
        try:
            subgroup = int(input())
            if subgroup == 1 or subgroup == 2:
                break
            else:
                print("Введено неправильное значение. Введите 1 или 2")
        except ValueError:
            print("Введено неправильное значение. Введите 1 или 2")
    return subgroup


class Handler(ABC):
    """
    Интерфейс Обработчика объявляет метод построения цепочки обработчиков. Он
    также объявляет метод для выполнения запроса.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    Поведение цепочки по умолчанию может быть реализовано внутри базового класса
    обработчика.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Возврат обработчика отсюда позволит связать обработчики простым
        # способом, вот так:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request: Any) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None


"""
Все Конкретные Обработчики либо обрабатывают запрос, либо передают его
следующему обработчику в цепочке.
"""


class UpdateHandler(AbstractHandler):  # самое сложное, разделить на более мелкие классы вроде UpdateName
    def handle(self, request: Any) -> str:
        if request == "5":  
            print("Введите фамилию студента для идентификации его учетной записи")
            surname = input()
            client_socket.send(bytes(surname.encode('utf-8')))
            flag = client_socket.recv(1024).decode("utf8")
            if flag == "1":
                print(
                    "Выберите, что нужно изменить\n1 - Фамилия, 2 - Имя, 3 - Отчество, 4 - Курс, 5 - Группа, "
                    "6 - Подгруппа")
                # корректный ввод цифры
                while True:
                    try:
                        z = int(input())
                        if z == 1 or z == 2 or z == 3 or z == 4 or z == 5 or z == 6:
                            break
                        else:
                            print("Введено неправильное значение. Попробуйте еще раз.")
                    except ValueError:
                        print("Введено неправильное значение. Попробуйте еще раз.")

                client_socket.send(bytes(str(z).encode('utf-8')))
                if z == 1:
                    print("Введите новую фамилию студента:")
                    surname = input()
                    client_socket.send(bytes(surname.encode('utf-8')))
                elif z == 2:
                    print("Введите новое имя студента:")
                    name = input()
                    client_socket.send(bytes(name.encode('utf-8')))
                elif z == 3:
                    print("Введите новое отчество студента:")
                    patronym = input()
                    client_socket.send(bytes(patronym.encode('utf-8')))
                elif z == 4:
                    print("Курс студента:")
                    course = input_course()
                    client_socket.send(bytes(str(course).encode('utf-8')))
                elif z == 5:
                    print("Введите новую группу студента:")
                    group = input_group()
                    client_socket.send(bytes(group.encode('utf-8')))
                else:
                    print("Введите новую подгруппу студента:")
                    subgroup = input_subgroup()
                    client_socket.send(bytes(str(subgroup).encode('utf-8')))
            msg = client_socket.recv(1024).decode("utf8") + "\n"
            return msg
        else:
            return super().handle(request)


class RegistrationHandler(AbstractHandler):  # регистрация студента в системе
    def handle(self, request: Any) -> str:
        if request == "6":

            print("Введите фамилию студента:")
            surname = input()
            client_socket.send(bytes(surname.encode('utf-8')))
            print("Введите имя студента:")
            name = input()
            client_socket.send(bytes(name.encode('utf-8')))
            print("Введите отчество (при отсутствии введите тире):")
            patronym = input()
            client_socket.send(bytes(patronym.encode('utf-8')))
            print("Введите курс")
            course = input_course()
            client_socket.send(bytes(str(course).encode('utf-8')))
            print("Группа студента? Введите строку, состоящую из трех букв и трех цифр")
            group = input_group()
            client_socket.send(bytes(group.encode('utf-8')))
            print("Введите подгруппу студента. (1 или 2)")
            subgroup = input_subgroup()
            client_socket.send(bytes(str(subgroup).encode('utf-8')))

            msg = client_socket.recv(1024).decode("utf8") + "\n"
            return msg
        else:
            return super().handle(request)


class RemoveHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "7":

            print("Введите фамилию студента, которого надо отчислить")
            surname = input()
            client_socket.send(bytes(str(surname).encode('utf-8')))

            msg = client_socket.recv(1024).decode("utf8") + "\n"
            return msg
        else:
            return super().handle(request)


class ZachetkaHandler(AbstractHandler):  # добавить ветвление
    def handle(self, request: Any) -> str:
        if request == "1":

            print("Введите фамилию студента для поиска его зачетки")
            surname = input()
            client_socket.send(bytes(str(surname).encode('utf-8')))

            msg = client_socket.recv(1024).decode("utf8") + "\n"
            return msg
        else:
            return super().handle(request)


class RatingHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "2":

            msg = client_socket.recv(1024).decode("utf8") + "\n"
            return msg
        else:
            return super().handle(request)


class ChangePasswordHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "3":

            flag = 0
            while flag == 0:
                print("Придумайте пароль")
                password1 = input()
                print("Повторите пароль")
                password2 = input()
                if password1 == password2:
                    flag = 1
                else:
                    print("Пароли не совпадают. Попробуйте еще раз")
            client_socket.send(bytes(password1.encode('utf-8')))

            msg = client_socket.recv(1024).decode("utf8") + "\n"
            return msg
        else:
            return super().handle(request)


class ExitHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "4":

            msg = client_socket.recv(1024).decode("utf8") + "\n"
            client_socket.close()
            return msg
        else:
            return super().handle(request)


def client_code(handler: Handler, event) -> None:

    print(f"\nClient has chosen {event}")
    result = handler.handle(event)
    if result:
        print(f"  {result}")
    else:
        print(f"  {event} was left untouched.")


def communication():
    print("Добро пожаловать в ЛМС 2.0\n"
          "Пожалуйста, войдите в систему!")
    p = 0
    flag = "0"
    while flag == "0":
        print("Введите Ваш логин")
        login = input()
        client_socket.send(bytes(login.encode('utf-8')))
        print("Введите Ваш пароль")
        password1 = input()
        client_socket.send(bytes(password1.encode('utf-8')))
        flag = client_socket.recv(1024).decode("utf8")
        if flag == "1":
            print("Вы вошли в систему!")
            if login == "admin":
                p = 1  # продвинутое меню для админа
            break
        else:
            print("Неверный логин или пароль, попробуйте ещё раз!")

    client_socket.send(bytes(str(p).encode('utf-8')))  # send to server the menu code
    if p == 1:  # вход выполнил администратор
        
        print(
            "Меню:\n"
            "5 - Внести изменения в учетную запись студента\n"
            "6 - Зарегистрировать студента\n"
            "7 - Удалить студента\n"
            "1 - Посмотреть зачетку студента\n"
            "2 - Посмотреть рейтинг\n"
            "3 - Изменить пароль\n"
            "4 - Выйти из "
            "приложения")
        while True:
            while True:  # ввод цифры из продвинутого меню
                try:
                    event = input()
                    if event == "1" or event == "2" or event == "3" or event == "4" or \
                        event == "5" or event == "6" or event == "7":
                        break
                    else:
                        print(
                            "Введено неправильное значение.\n"
                            "5 - Изменение\n"
                            "6 - Регистрация\n"
                            "7 - Удаление \n"
                            "1 - Зачетка\n"
                            "2 - Рейтинг\n"
                            "3 - Смена пароля\n"
                            "4 - Выход")
                except ValueError:
                    print(
                        "Введено неправильное значение.\n"
                        "5 - Изменение\n"
                        "6 - Регистрация\n"
                        "7 - Удаление \n"
                        "1 - Зачетка\n"
                        "2 - Рейтинг\n"
                        "3 - Смена пароля\n"
                        "4 - Выход")

            client_socket.send(bytes(event.encode('utf-8')))  # отправка цифры на сервер

            client_code(upd, event)

            if event == "4":
                break

    else:  # в систему вошел студент, упрощенное меню
        
        print("Меню:\n"
              "1 - Зачетка\n"
              "2 - Рейтинг\n"
              "3 - Изменить пароль\n"
              "4 - Выйти из приложения")
        while True:
            while True:  # ввод цифры из меню
                try:
                    event = input()
                    if event == "1" or event == "2" or event == "3" or event == "4":
                        break
                    else:
                        print("Введено неправильное значение.\n"
                              "1 - Зачетка\n"
                              "2 - Рейтинг\n"
                              "3 - Смена пароля\n"
                              "4 - Выход")
                except ValueError:
                    print("Введено неправильное значение.\n"
                          "1 - Зачетка\n"
                          "2 - Рейтинг\n"
                          "3 - Смена пароля\n"
                          "4 - Выход")

            client_socket.send(bytes(event.encode('utf-8')))  # отправка цифры на сервер
            client_code(zach, event)
            if event == "4":
                break

if __name__ == "__main__":
    upd = UpdateHandler()
    reg = RegistrationHandler()
    rem = RemoveHandler()
    zach = ZachetkaHandler()
    rat = RatingHandler()
    chp = ChangePasswordHandler()    
    ext = ExitHandler()

    upd.set_next(reg).set_next(rem).set_next(zach).set_next(rat).set_next(chp).set_next(ext)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))

    receive_thread = Thread(target=communication)
    receive_thread.start()
