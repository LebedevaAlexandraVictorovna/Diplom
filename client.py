# -*- coding: utf-8 -*-

# Пересмотрим программу. Пусть у всех пользователей есть свой пароль 
# и он им заранее известен. Добавить, удалить и т.п. может только админ.

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

def isalpha_ru(string):
    flag = True
    for c in string:
        if (c < 'А' or c > 'я'): 
            flag = False
    return flag

def input_course():
    print("Введите курс")
    while True: 
        try:
            course = int(input())
            if course > 0 and course < 5: # бакалавриат
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
            if (group[:3].isalpha() == True or isalpha_ru(group[:3]) == True) and group[3:].isdigit() == True and len(group) == 6: 
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

def communication():
    print("Добро пожаловать в ЛМС 2.0\nПожалуйста, войдите в систему!")
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
    
    client_socket.send(bytes(str(p).encode('utf-8'))) # send to server the menu code
    if p == 1:  #  вход выполнил администратор
        print("Меню:\n1 - Внести изменения в учетную запись студента\n2 - Зарегистрировать студента\n3 - Удалить студента\n4 - Посмотреть зачетку студента\n5 - Посмотреть рейтинг\n6 - Изменить пароль\n7 - Выйти из приложения")
        while True:
            while True:  # ввод цифры из продвинутого меню
                try:
                    y = int(input())
                    if y == 1 or y == 2 or y == 3 or y == 4 or y == 5 or y == 6 or y == 7:
                        break
                    else:
                        print("Введено неправильное значение.\n1 - Изменение\n2 - Регистрация\n3 - Удаление \n4 - Зачетка\n5 - Рейтинг\n6 - Смена пароля\n7 - Выход")
                except ValueError:
                    print("Введено неправильное значение.\n1 - Изменение\n2 - Регистрация\n3 - Удаление \n4 - Зачетка\n5 - Рейтинг\n6 - Смена пароля\n7 - Выход")
            
            client_socket.send(bytes(str(y).encode('utf-8') )) # отправка цифры на сервер

            if y == 1:
                print("Введите фамилию студента для идентификации его учетной записи")
                surname = input()
                client_socket.send(bytes(surname.encode('utf-8')))
                print("Выберите, что нужно изменить\n1 - Фамилия, 2 - Имя, 3 - Отчество, 4 - Курс, 5 - Группа, 6 - Подгруппа, 7 - Стоп")
                while True:
                    # корректный ввод цифры
                    while True:
                        try:
                            z = int(input())
                            if z == 1 or z == 2 or z == 3 or z == 4 or z == 5 or z == 6 or z == 7:
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
                        #client_socket.send(bytes(translit(surname).encode('utf-8'))) # для сменя логина на сервере
                    elif z == 2:
                        print("Введите новое имя студента:")
                        name = input()
                        client_socket.send(bytes(name.encode('utf-8')))
                        #client_socket.send(bytes(translit(name[0]).encode('utf-8')))
                    elif z == 3:
                        print("Введите новое отчество студента:")
                        patronym = input()
                        client_socket.send(bytes(patronym.encode('utf-8')))
                        #client_socket.send(bytes(translit(patronym[0]).encode('utf-8')))
                    elif z == 4:
                        print("Курс студента:")
                        course = input_course()
                        client_socket.send(bytes(str(course).encode('utf-8')))
                    elif z == 5:
                        print("Введите новую группу студента:")
                        group = input_group()
                        client_socket.send(bytes(group.encode('utf-8')))
                    elif z == 6:
                        print("Введите новую подгруппу студента:")
                        subgroup = input_subgroup()
                        client_socket.send(bytes(str(subgroup).encode('utf-8')))
                    else:  # дублирование меню для избежания путаницы
                        print("Меню:\n1 - Внести изменения в учетную запись студента\n2 - Зарегистрировать студента\n3 - Удалить студента\n4 - Посмотреть зачетку студента\n5 - Посмотреть рейтинг\n6 - Выйти из приложения")
                        break  
            
            if y == 2: # регистрация студента в системе
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

                print("Регистрация прошла успешно!")
            
            if y == 3:  # удаление
                print("Введите фамилию студента, которого надо отчислить")
                surname = input()
                client_socket.send(bytes(str(surname).encode('utf-8')))
                print("Готово!")

            if y == 4: # зачетка
                print("Введите фамилию студента для поиска его зачетки")
                surname = input()
                client_socket.send(bytes(str(surname).encode('utf-8')))
            
            if y == 6: # смена пароля
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
            
            try:
                msg = client_socket.recv(1024).decode("utf8")
                print(msg)
                if y == 7:
                    client_socket.close()
                    break
            except OSError:
                break            
    
    else:  # в систему вошел студент, упрощенное меню
        print("Меню:\n1 - Зачетка\n2 - Рейтинг\n3 - Изменить пароль\n4 - Выйти из приложения")
        while True:
            while True: # ввод цифры из меню
                try:
                    y = int(input())
                    if y == 1 or y == 2 or y == 3 or y == 4:
                        break
                    else:
                        print("Введено неправильное значение.\n1 - Зачетка\n2 - Рейтинг\n3 - Смена пароля\n4 - Выход")
                except ValueError:
                    print("Введено неправильное значение.\n1 - Зачетка\n2 - Рейтинг\n3 - Смена пароля\n4 - Выход")
            
            if y == 3:
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

            client_socket.send(bytes(str(y).encode('utf-8') )) # отправка цифры на сервер
            try:
                msg = client_socket.recv(1024).decode("utf8")
                print(msg)
                if y == 3:
                    client_socket.close()
                    break
            except OSError:
                break

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 84))

receive_thread = Thread(target=communication)
receive_thread.start()
