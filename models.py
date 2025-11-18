from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id=id
        self.username=username
        self.password=password

class Task:
    def __init__(self,id,title,completed):
        self.id=id
        self.title=title
        self.completed=completed
