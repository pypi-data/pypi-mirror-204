from Aciembler import translator
from tabulate import tabulate
from HHLtools.prints import *
import os
import sys
import shutil
import time
from tkinter import filedialog
import tkinter as tk
import random
import platform


def new_file():
    base = os.path.dirname(os.path.abspath(__file__))
    if ((path := filedialog.asksaveasfilename(defaultextension='.xlsx')) == ''):
        return
    try:
        shutil.copy(base + '/data/Template.xlsx', path)
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
        if ((path := filedialog.askopenfilename(defaultextension='.xlsx')) == ''):
            return

        print('File found! Opening file')
        time.sleep(1.5)
        if platform.system() == 'Windows':
            os.startfile(path)
        else:
            os.system(f'open {path}')

    while ((choice := input('Finished editing? [y/n]: ')) != 'y'):
        pass

    load_file(path)


def load_file(path=''):
    if path == '':
        if ((path := filedialog.askopenfilename(defaultextension='.xlsx')) == ''):
            return

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


root = 0


def start():
    global root
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
        root = tk.Tk()
        root.withdraw()
        match choice:
            case '1':
                new_file()
            case '2':
                edit_file()
            case '3':
                load_file()
            case '4':
                ins = \
                    """
                    INSTRUCTION
                    ======================================================
                    1. Create New File
                        Select a directory you will create your program at, no need to add the file extension,
                        it will be automatically added

                    2. Edit exsiting file
                        Select your program, and it will open automatically

                    3. Load Existing File
                        Select your program, and it will be loaded and executed
                    ======================================================
                    """
                print(ins)
            case '5':
                exit()
            case _:
                print('Invalid input, please input again!')

