# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from student import Student
from discipline import Discipline
from administrator import Administrator

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
            adm = Administrator():
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
                break
        if flag == "0":
            client.send(bytes("0", "utf8"))

    msg = client.recv(1024).decode("utf8")  # получаем код продвинутого\упрощенного меню

    if msg == "1": # продвинутое меню для администратора
        msg1 = client.recv(1024).decode("utf8")
        if msg1 == "1":  # внести изменения в учетную запись
            while True:
                surname = client.recv(1024).decode("utf8")
                for stud in students:
                    if stud.get_surname() == surname:
                        break 
                z = client.recv(1024).decode("utf8")
                if z == 1: # меняем фамилию
                    new_surname = client.recv(1024).decode("utf8")
                    

            





        flag = "0"
        while flag == "0":
            print("Logging in") #вход
            login = client.recv(1024).decode("utf8")
            password = client.recv(1024).decode("utf8")
            for stud in students:
                if stud.get_login() == login and stud.get_password() == password:
                    client.send(bytes("1", "utf8")) # логин и пароль верны
                    flag = "1"
                    break
            if flag == "0":
                client.send(bytes("0", "utf8"))

    else:
        stud = Student()
        print("Signing in") # регистрация
        surname = client.recv(1024).decode("utf8")
        stud.set_surname(surname)
        name = client.recv(1024).decode("utf8")
        stud.set_name(name)
        patronym = client.recv(1024).decode("utf8")
        stud.set_patronym(patronym)
        login = client.recv(1024).decode("utf8")
        stud.set_login(login)
        password = client.recv(1024).decode("utf8")
        stud.set_password(password)
        course = client.recv(1024).decode("utf8")
        stud.set_course(int(course))
        group = client.recv(1024).decode("utf8")
        stud.set_group(group)
        subgroup = client.recv(1024).decode("utf8")
        stud.set_subgroup(int(subgroup))
        students.append(stud)
        f = open("list.txt", "a") # открытие файла на дозапись
        f.write("\n"+surname+"*"+name+"*"+patronym+"*"+login+"*"+password+"*"+course+"*"+group+"*"+subgroup)
        f.close()
    
    while True:
        msg = client.recv(1024).decode("utf8") # меню
        print(msg)
        if msg == "1":  # зачетка
            msg = str(stud.get_surname()) + " " + str(stud.get_name()) + " " + str(stud.get_patronym()) + \
                "\n" + "Студент бакалавриата " + str(stud.get_course()) + " курс" + "\n" + "-------------------------------------------------"
            for obj in disciplines:
                msg = msg + "\n" + str(obj.get_name()) + " " + str(obj.find_mark(str(stud.get_surname())))
            client.send(bytes(msg, "utf8"))
        elif msg == "2":  # рейтинг
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
            client.send(bytes(msg, "utf8"))
        else:
            client.send(bytes("До свидания!", "utf8"))
            client.close()
            break
 

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(('localhost', 81))
 
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
