class Administrator:   # наследование с student?
    def __init__(self):
        self.surname = "Фамилия"
        self.name = "Имя"
        self.patronym = "Отчество"
        self.login = "admin"  # логин всегда admin, setter не нужен
        self._password = ""
    
    # setters
    def set_surname(self, s):
        self.surname = s
    
    def set_name(self, n):
        self.name = n

    def set_patronym(self, p):
        self.patronym = p
    
    def set_password(self, password):
        self._password = password
    
    # getters
    def get_surname(self):
        return self.surname

    def get_name(self):
        return self.name

    def get_patronym(self):
        return self.patronym
    
    def get_login(self):
        return self.login
    
    def get_password(self):
        return self._password
