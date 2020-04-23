# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from student import Student
from discipline import Discipline

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)  # "{}:{} qwerty".format(a,b)
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    
    f = open("list.txt")  # файл со списком учеников
    students = []  # список объектов 
    text = f.read().splitlines()
    for line in text:
        spl = line.split("*")
        stud = Student(spl[0],spl[1],spl[2],spl[3],spl[4],spl[5],spl[6],spl[7])
        students.append(stud)  
    f.close()

    g = open("disciplines.txt")  # файл со списком дисциплин
    disciplines = []
    text = g.read().splitlines()
    for line in text:
        spl = line.split("*")
        subj = Discipline(spl[0],spl[1],spl[2],spl[3])
        disciplines.append(subj)
    g.close()

    msg = client.recv(1024).decode("utf8")
    if msg == "1":
        flag = "0"
        while flag == "0":
            print("Logging in") #вход
            login = client.recv(1024).decode("utf8")
            password = client.recv(1024).decode("utf8")
            for stud in students:
                if stud.your_login_password(login, password) == True:
                    client.send(bytes("1", "utf8")) # логин и пароль верны
                    flag = "1"
                    break
            if flag == "0":
                client.send(bytes("0", "utf8"))

    else:
        print("Signing in") # регистрация
        surname = client.recv(1024).decode("utf8")
        name = client.recv(1024).decode("utf8")
        patronym = client.recv(1024).decode("utf8")
        login = client.recv(1024).decode("utf8")
        password = client.recv(1024).decode("utf8")
        course = client.recv(1024).decode("utf8")
        group = client.recv(1024).decode("utf8")
        subgroup = client.recv(1024).decode("utf8")
        stud = Student(surname,name,patronym,login,password,course,group,subgroup)
        students.append(stud)
        f = open("list.txt", "a") # открытие файла на дозапись
        f.write("\n"+surname+"*"+name+"*"+patronym+"*"+login+"*"+password+"*"+course+"*"+group+"*"+subgroup)
        f.close()
    
    while True:
        msg = client.recv(1024).decode("utf8") # меню
        print(msg)
        if msg == "1":  # зачетка
            msg = stud.say_fio_course() + "\n--------------------------------"
            for obj in disciplines:
                msg = msg + "\n" + str(obj.say_name()) + " " + str(obj.find_mark(str(stud.say_surname())))
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
                    avg = avg + int(obj.find_mark(str(st.say_surname())))
                    cr = cr + int(obj.say_credits())
                    gpa = gpa + int(obj.say_credits()) * int(obj.find_mark(str(st.say_surname())))
                avg = avg/n
                gpa = gpa/cr
                rating[gpa] = str(st.say_fio()) + " " + str(round(avg,2))
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
SERVER.bind(('localhost', 84))
 
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
