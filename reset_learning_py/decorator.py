def log(func):
    def wrapper(*args, **k):
        print('call %s():' % func.__name__)
        return func(*args, **k)
    return wrapper
@log
def now():
    print('2015-3-25')
now()