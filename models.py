from flask_login import UserMixin

class User(UserMixin):
          def __init__(self, id, name, surname, email, mode, password, hasTicket):
                    self.id = id
                    self.name = name
                    self.surname = surname
                    self.email = email
                    self.mode = mode
                    self.password = password
                    self.hasTicket = hasTicket