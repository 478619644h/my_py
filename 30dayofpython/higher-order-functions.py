

def uppercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase
    return wrapper

def lowercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.lower()
        return make_uppercase
    return wrapper

@uppercase_decorator
@lowercase_decorator
@uppercase_decorator
def greeting():
    return 'Welcome to Python'


def decorator_with_parameters(function):
    def wrapper_accepting_parameters(para1, para2, para3):
        a = function(para1, para2, para3)
        print(a)
        print("I live in {}".format(para3))
        function(para1, para2, para3)
    return wrapper_accepting_parameters

@decorator_with_parameters
def print_full_name(first_name, last_name, country):
    print("I am {} {}. I love to teach.".format(
        first_name, last_name, country))
    return 123

numbers = [1,2,3,4,5]

def is_even(num):
    if num % 2 == 0:
        return True
    return False
from functools import reduce
import re


def packing_person_info(**kwargs):
    # check the type of kwargs and it is a dict type
    # print(type(kwargs))
	# Printing dictionary items
    for key in kwargs:
        print("{} = {}".format(key,kwargs.get(key)))
    return kwargs

paragraph = 'I love teaching. If you do not love teaching what else can you love. I love Python if you do not love something which can give you all the capabilities to develop an application what else can you love.'


if __name__=='__main__':
    # print(greeting())
    # print_full_name("Asabeneh", "Yetayeh", 'Finland')
    # print(numbers)
    # numbers = map(lambda x:x*x,numbers)
    # print(list(numbers))
    # a_numbers = filter(lambda x:x%2 != 0,numbers)
    # print(list(a_numbers))

    # total = reduce(lambda x,y:x+y,numbers)
    # print(total)

    # print(packing_person_info(name="Asabeneh",
    #                           country="Finland", city="Helsinki", age=250))

    pattern = r'[\w]+'
    match = re.findall(pattern,paragraph)
    a = map(lambda x:(match.count(x),x),match)
    b = list(a)
    b.sort(key=lambda x:x[0],reverse=True)
    print(set(b))
