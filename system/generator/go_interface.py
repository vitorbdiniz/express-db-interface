import time, os

def go_get_id():
    os.system('./main/generator/go_scripts/newId')
    idfile = open('./main/generator/go_scripts/id.txt', 'r').read()
    os.remove('./main/generator/go_scripts/id.txt')
    return idfile

def get_date():
    return int(time.time_ns() / 1000000)
