# write a decorator that prints name given number of times

def greet(num):
    def greet_inner(say_name):
        def wrapper(name):
            names = []
            for i in range(0,num):
                names.append(f"Name is : {say_name(name)}")
            return "\n".join(names)
        return wrapper
    return greet_inner


@greet(10)
def say_name(name):
    return name
    
a = say_name("deepesh")

print(a)