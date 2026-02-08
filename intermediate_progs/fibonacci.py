# function to return first n values of fibonacci series

def fib(x):
    a, b = 0, 1
    while x:
        print(b)
        a,b = b,a+b
        x-=1

if __name__ == "__main__":
    fib(10)
