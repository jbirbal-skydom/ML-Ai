from random import randint
import keyboard

def get_random_ints(count, begin, end):
    print("get_random_ints start")
    list_numbers = []
    for x in range(0, count):
        list_numbers.append(randint(begin, end))
    print("get_random_ints end")
    return list_numbers


def gen_random_ints(count, begin, end):
    print("get_random_ints start")
    for x in range(0, count):
        yield randint(begin, end)
    print("get_random_ints end")



nums_generator = gen_random_ints(10, 0, 100)
print(type(nums_generator))


while(True):
    a = keyboard.read_key()
    if a == '1' or a == '2':
        print("Option {} was pressed\n".format(a))
        try: 
            num = next(nums_generator)
        except StopIteration as e:
            print (e)
        print(num)
