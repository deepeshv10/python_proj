# example that shows demonstration of a decorator usage in Python

import functools

def repeat_num_times(num):
    def decorator_repeat_num_times(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat_num_times

@repeat_num_times(num=3)               # decorator
def say_name(name):         # original function
    print(f'Hello {name}!')


if __name__ == "__main__":
    say_name('Deepesh Verma')
