# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import random

from student import Student
from discipline import Discipline
from administrator import Administrator

def generate_password():  
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password =''
    for i in range(8):
        password += random.choice(chars)
    return(password)

def update_file(students, admins):
    f = open("list.txt", "w")
    for stud in students:
        f.write(stud.get_surname() +"*"+stud.get_name()+"*"+stud.get_patronym()+\
            "*"+stud.get_login() +"*"+stud.get_password() +"*"+str(stud.get_course()) +"*"+stud.get_group()+"*"+str(stud.get_subgroup()) + "\n")
    for adm in admins:
        f.write(adm.get_surname()+"*"+adm.get_name() +"*"+adm.get_patronym() +\
        "*"+adm.get_login()+"*"+adm.get_password()+"\n")
    f.close()

def translit(string): 
    d = {
        "А": "a", "а": "a", "Б": "b", "б": "b", "В": "v", "в": "v",
        "Г": "g", "г": "g", "Д": "d", "д": "d", "Е": "e", "е": "e",
        "Ж": "zh", "ж": "zh", "З": "z", "з": "z", "И": "i", "и": "i",
        "Й": "y", "й": "y", "К": "k", "к": "k", "Л": "l", "л": "l",
        "М": "m", "м": "m", "Н": "n", "н": "n", "О": "o", "о": "o",
        "П": "p", "п": "p", "Р": "r", "р": "r", "С": "s", "с": "s",
        "Т": "t", "т": "t", "У": "u", "у": "u", "Ф": "f", "ф": "f",
        "Х": "kh", "х": "kh", "Ц": "ts", "ц": "ts", "Ч": "ch", "ч": "ch",
        "Ш": "sh", "ш": "sh", "Щ": "shch", "щ": "shch",
        "ъ": "", "ы": "y", "ь": "i",
        "Э": "e", "э": "e", "Ю": "yu", "ю": "yu", "Я": "ya", "я": "ya", "-": ""
    }
    login = ""
    for c in string:
        login = login + d[c]
    return login

def show_rating(students, disciplines):
    # рейтинг будет считаться в соответствии с gpa
    rating = {}
    msg = "Фамилия Имя Отчество  Ср. балл  GPA\n-------------------------------------------------------"
    for st in students:
        n = 0  # количество дисциплин
        cr = 0  # сумма кредитов
        avg = 0  # средний балл
        gpa = 0
        for obj in disciplines:
            n = n + 1
            avg = avg + int(obj.find_mark(str(st.get_surname())))
            cr = cr + int(obj.get_credits())
            gpa = gpa + int(obj.get_credits()) * int(obj.find_mark(str(st.get_surname())))
        avg = avg/n
        gpa = gpa/cr
        rating[gpa] = str(st.get_surname()) + " " + str(st.get_name()) + " " + str(st.get_patronym()) + " " + str(round(avg,2))
    r_list = list(rating.keys())
    r_list.sort()
    r_list.reverse()
    n = 0
    for i in r_list:
        n = n + 1
        msg = msg + "\n" + str(n) + " " + rating[i] + " " + str(round(i,2))
    return msg
    
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)  # "{}:{} qwerty".format(a,b)
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    
    f = open("list.txt")  # файл со списком учеников и администраторов
    students = []  # список студентов
    admins = [] # список админов
    text = f.read().splitlines()
    for line in text:
        spl = line.split("*")
        if spl[3] == "admin":
            adm = Administrator()
            adm.set_surname(spl[0])
            adm.set_name(spl[1])
            adm.set_patronym(spl[2])
            adm.set_password(spl[4])
            admins.append(adm)
        else:
            stud = Student()
            stud.set_surname(spl[0])
            stud.set_name(spl[1])
            stud.set_patronym(spl[2])
            stud.set_login(spl[3])
            stud.set_password(spl[4])
            stud.set_course(int(spl[5]))
            stud.set_group(spl[6])
            stud.set_subgroup(int(spl[7]))
            students.append(stud)  
    f.close()

    g = open("disciplines.txt")  # файл со списком дисциплин
    disciplines = []
    text = g.read().splitlines()
    for line in text:
        spl = line.split("*")
        subj = Discipline()
        subj.set_name(spl[0])
        subj.set_course(spl[1])
        subj.set_credits(spl[2])
        subj.set_vedomost(spl[3])
        disciplines.append(subj)
    g.close()

    flag = "0"
    while flag == "0":
        print("Logging in") #вход
        login = client.recv(1024).decode("utf8")
        password = client.recv(1024).decode("utf8")
        for stud in students+admins:
            if stud.get_login() == login and stud.get_password() == password:
                client.send(bytes("1", "utf8")) # логин и пароль верны
                flag = "1"
                user = stud.get_surname()
                break
        if flag == "0":
            client.send(bytes("0", "utf8"))

    msg = client.recv(1024).decode("utf8")  # получаем код продвинутого\упрощенного меню

    if msg == "1": # продвинутое меню для администратора
        while True:
            msg1 = client.recv(1024).decode("utf8")
            if msg1 == "1":  # внести изменения в учетную запись
                surname = client.recv(1024).decode("utf8")
                for stud in students:
                    if stud.get_surname() == surname:
                        break 
                z = client.recv(1024).decode("utf8")
                if z == "1": # меняем фамилию
                    new_surname = client.recv(1024).decode("utf8")
                    stud.set_surname(new_surname)
                    new_login = translit(stud.get_name()[0] + stud.get_patronym()[0] + new_surname)
                    stud.set_login(new_login)
                    client.send(bytes("Фамилия и логин изменены", "utf8"))
                    # меняем старую фамилию в ведомостях
                    for subj in disciplines:
                        m = subj.find_mark(surname)
                        f = open(subj.get_vedomost())
                        text = f.read().splitlines()
                        new_lines = []
                        for line in text:
                            if surname in line:
                                new_lines.append(new_surname + " " + m)
                            else:
                                new_lines.append(line)
                        f.close()
                        f = open(subj.get_vedomost(), "w")
                        for line in new_lines:
                            f.write("%s\n" % line)
                        f.close()

                elif z == "2": # имя
                    new_name = client.recv(1024).decode("utf8")
                    stud.set_name(new_name)
                    new_login = translit(new_name[0] + stud.get_patronym()[0] + stud.get_surname())
                    stud.set_login(new_login)
                    client.send(bytes("Имя и логин изменены", "utf8"))
                elif z == "3":
                    new_patronym = client.recv(1024).decode("utf8")
                    stud.set_patronym(new_patronym)
                    new_login = translit(stud.get_name()[0] + new_patronym[0] + stud.get_surname())
                    stud.set_login(new_login)
                    client.send(bytes("Отчество и логин изменены", "utf8"))
                elif z == "4": # курс
                    new_course = client.recv(1024).decode("utf8")
                    stud.set_course(int(new_course))
                    client.send(bytes("Курс изменен", "utf8"))
                elif z == "5":
                    new_group = client.recv(1024).decode("utf8")
                    stud.set_group(new_group)
                    client.send(bytes("Группа изменена", "utf8"))                    
                else:
                    new_subgroup = client.recv(1024).decode("utf8")
                    stud.set_subgroup(int(new_subgroup))
                    client.send(bytes("Подгруппа изменена", "utf8"))
                # перезапись файла list.txt
                update_file(students, admins)
                                            
            elif msg1 == "2":
                stud = Student()
                print("Signing in") # регистрация
                surname = client.recv(1024).decode("utf8")
                stud.set_surname(surname)
                name = client.recv(1024).decode("utf8")
                stud.set_name(name)
                patronym = client.recv(1024).decode("utf8")
                stud.set_patronym(patronym)

                # генерация логина
                login = translit(name[0] + patronym[0] + surname)
                stud.set_login(login)

                # генерация пароля
                password = generate_password()
                stud.set_password(password)
                
                course = client.recv(1024).decode("utf8")
                stud.set_course(int(course))
                group = client.recv(1024).decode("utf8")
                stud.set_group(group)
                subgroup = client.recv(1024).decode("utf8")
                stud.set_subgroup(int(subgroup))
                students.append(stud)
                f = open("list.txt", "a") # открытие файла на дозапись
                f.write(surname+"*"+name+"*"+patronym+"*"+login+"*"+password+"*"+course+"*"+group+"*"+subgroup+"\n")
                f.close()
                client.send(bytes("Регистрация прошла успешно", "utf8"))
            
            elif msg1 == "3": # удаление
                surname = client.recv(1024).decode("utf8")
                for stud in students:
                    if stud.get_surname() == surname:
                        students.remove(stud)
                update_file(students, admins)
                client.send(bytes("Студент отчислен!", "utf8"))
            
            elif msg1 == "4":  # зачетка
                surname = client.recv(1024).decode("utf8")
                for stud in students:
                    if stud.get_surname() == surname:
                        break
                msg = str(stud.get_surname()) + " " + str(stud.get_name()) + " " + str(stud.get_patronym()) + \
                    "\n" + "Студент бакалавриата " + str(stud.get_course()) + " курс" + "\n" + "-------------------------------------------------"
                for obj in disciplines:
                    msg = msg + "\n" + str(obj.get_name()) + " " + str(obj.find_mark(str(stud.get_surname())))
                client.send(bytes(msg, "utf8"))
            
            elif msg1 == "5":  # рейтинг
                msg = show_rating(students, disciplines)
                client.send(bytes(msg, "utf8"))
            
            elif msg1 == "6":  # смена пароля
                password = client.recv(1024).decode("utf8")
                for adm in admins:
                    if adm.get_surname() == user:
                        adm.set_password(password)
                update_file(students, admins)
                client.send(bytes("Пароль изменен", "utf8"))
            
            else: # закрываем соединение
                client.send(bytes("До свидания!", "utf8"))
                client.close()
                break

    else:    
        while True:
            msg = client.recv(1024).decode("utf8") # меню
            if msg == "1":  # зачетка
                msg = str(stud.get_surname()) + " " + str(stud.get_name()) + " " + str(stud.get_patronym()) + \
                    "\n" + "Студент бакалавриата " + str(stud.get_course()) + " курс" + "\n" + "-------------------------------------------------"
                for obj in disciplines:
                    msg = msg + "\n" + str(obj.get_name()) + " " + str(obj.find_mark(str(stud.get_surname())))
                client.send(bytes(msg, "utf8"))
            elif msg == "2":  # рейтинг
                msg = show_rating(students, disciplines)
                client.send(bytes(msg, "utf8"))
            elif msg == "3":
                password = client.recv(1024).decode("utf8")
                for stud in students:
                    if stud.get_surname() == user:
                        stud.set_password(password)
                update_file(students, admins)
                client.send(bytes("Пароль изменен", "utf8"))
            else:
                client.send(bytes("До свидания!", "utf8"))
                client.close()
                break
 

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(('localhost', 85))
 
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
