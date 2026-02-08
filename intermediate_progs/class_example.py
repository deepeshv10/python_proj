class User:
    def __init__(self, user_name, user_city):
        self.name = user_name
        self.city = user_city
    
    def introduce(self):
        print("Hello, I am ",self.name, ', and I am from ',self.city)

user = User("Deepesh", "Pune")

user.introduce()
print(user.name)