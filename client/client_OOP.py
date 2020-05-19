# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

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
        if request == "Update":
            return "Update"
        else:
            return super().handle(request)


class RegistrationHandler(AbstractHandler):  # регистрация студента в системе
    def handle(self, request: Any) -> str:
        if request == "Registration":
            y = 2
            client_socket.send(bytes(str(y).encode('utf-8')))

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

            msg = client_socket.recv(1024).decode("utf8")
            return msg
        else:
            return super().handle(request)


class RemoveHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "Remove":
            y = 3
            client_socket.send(bytes(str(y).encode('utf-8')))

            print("Введите фамилию студента, которого надо отчислить")
            surname = input()
            client_socket.send(bytes(str(surname).encode('utf-8')))

            msg = client_socket.recv(1024).decode("utf8")
            return msg
        else:
            return super().handle(request)


class ZachetkaHandler(AbstractHandler):  # добавить ветвление
    def handle(self, request: Any) -> str:
        if request == "Zachetka":
            y = 4
            client_socket.send(bytes(str(y).encode('utf-8')))

            print("Введите фамилию студента для поиска его зачетки")
            surname = input()
            client_socket.send(bytes(str(surname).encode('utf-8')))

            msg = client_socket.recv(1024).decode("utf8")
            return msg
        else:
            return super().handle(request)


class RatingHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "Rating":
            y = 5
            client_socket.send(bytes(str(y).encode('utf-8')))

            msg = client_socket.recv(1024).decode("utf8")
            return msg
        else:
            return super().handle(request)


class ChangePasswordHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "ChangePassword":
            y = 6
            client_socket.send(bytes(str(y).encode('utf-8')))

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

            msg = client_socket.recv(1024).decode("utf8")
            return msg
        else:
            return super().handle(request)


class ExitHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "Exit":
            y = 7
            client_socket.send(bytes(str(y).encode('utf-8')))

            msg = client_socket.recv(1024).decode("utf8")
            client_socket.close()
            return msg
        else:
            return super().handle(request)


def client_code(handler: Handler) -> None:
    """
    Обычно клиентский код приспособлен для работы с единственным обработчиком. В
    большинстве случаев клиенту даже неизвестно, что этот обработчик является
    частью цепочки.
    """

    for event in ["Registration", "Rating", "Remove", "Remove", "Exit" ]:  # а здесь порядок
        print(f"\nClient has chosen {event}")
        result = handler.handle(event)
        if result:
            print(f"  {result}", end="")
        else:
            print(f"  {event} was left untouched.", end="")


if __name__ == "__main__":
    monkey = RegistrationHandler()
    squirrel = RatingHandler()
    dog = RemoveHandler()
    cat = ExitHandler()
    dog1 = RemoveHandler()

    monkey.set_next(squirrel).set_next(dog).set_next(cat).set_next(dog1)  # ааа это просто цепочка

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8094))

    receive_thread = Thread(target=communication)
    receive_thread.start()

    # Клиент должен иметь возможность отправлять запрос любому обработчику, а не
    # только первому в цепочке.
    print("Chain: Monkey > Squirrel > Dog")
    client_code(monkey)
    print("\n")

    print("Subchain: Squirrel > Dog")
    client_code(squirrel)
    print("\n")

    # если админ, цепочка начнется с начала, круть