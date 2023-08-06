from Aciembler import translator
from tabulate import tabulate
from HHLtools.prints import *
import os
import sys
import shutil
import time
from tkinter import filedialog
import random
import platform




def new_file():
    base = os.getcwd()
    while ((path := filedialog.asksaveasfilename(defaultextension='.xlsx')) == ''):
        pass
    try:
        shutil.copy('../data/Template.xlsx', path)
        edit_file(path)
    except Exception as e:
        print(e)


def edit_file(path=''):
    if path != '':
        print('File found! Opening file')
        time.sleep(1.5)
        if platform.system() == 'Windows':
            os.startfile(path)
        else:
            os.system(f'open {path}')
    else:
        while ((path := filedialog.askopenfilename(defaultextension='.xlsx')) == ''):
            pass

        print('File found! Opening file')
        time.sleep(1.5)
        if platform.system() == 'Windows':
            os.startfile(path)
        else:
            os.system(f'open {path}')

    while ((choice:=input('Finished editing? [y/n]: ')) != 'y'):
        pass

    load_file(path)


def load_file(path=''):
    if path == '':
        while((path := filedialog.askopenfilename(defaultextension='.xlsx')) == ''):
            pass

    print('Scanning source code...')
    time.sleep(0.5)
    print('Which base are you using for the memory address in the source code')
    print(tabulate([['[1]', 'Denary'], ['[2]', 'Binary'], ['[3]', 'Hexadecimal']]))

    while ((choice := input('Input your choice [1], [2], [3]: ')) not in ['1', '2', '3']):
        print('Invalid input, please input again')

    choice = int(choice)
    base = ['d', 'b', 'h'][choice - 1]

    while (input('Code Loaded Successfully, execute now? [y/n]: ') != 'y'):
        pass

    print('')
    print('Preparing translation...')
    time.sleep(1)
    print('Loading translator...')
    time.sleep(0.5)
    if platform.system() == 'Windows':
        print(os.getcwd() + r'\translator.py')
    else:
        print(os.getcwd() + '/translator.py')
    for i in range(0, 100, 10):
        print(i, end='...')
        time.sleep(random.random() * 0.5 + 0.5)

    print(99, end='...')
    time.sleep(random.randint(2, 3))
    print(100)
    print('Translator loaded successfully, doing first pass...')
    time.sleep(0.5)
    translator.run(base, path)
    exit()

def exit():
    sys.exit(0)


prints(' Welcome to the Acciembler-preter ', fontStyle=FontStyle.BOLD, fontColor=FontColor.BLACK,
           backgroundColor=BackgroundColor.WHITE)
print('v1.0.0')
print('developed by 黄浩霖 & 姚安北')
print('Guangdong Country Garden School')

while True:
    table = [['[1]', 'Create New File'], ['[2]', 'Edit exsiting file'], ['[3]', 'Load Existing File'],
    ['[4]', 'Help'], ['[5]', 'Exit']]
    print(tabulate(table))
    choice = input('Input your choice 1, 2, 3, 4, 5: ')

    match choice:
        case '1':
            new_file()
        case '2':
            edit_file()
        case '3':
            load_file()
        case '4':
            help("__init__")
        case '5':
            exit()
        case _:
            print('Invalid input, please input again!')

