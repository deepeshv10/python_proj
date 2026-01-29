class Car:
    def __init__(self, model, colour, speed = 0):
        self.model = model
        self.colour = colour
        if speed<0:
            self.__speed=0
        else:
            self.__speed = speed
    
    def speed_up(self):
        self.__speed+=5
    
    def speed_down(self):
        if self.__speed<5:
            self.__speed=0    
        else:
            self.__speed-=5
    
    def showspeed(self):
        print("current speed:", self.__speed)

car = Car("bmw","red",100)
car.showspeed()
car.speed = 105
car.showspeed()
car.speed_up()
car.showspeed()