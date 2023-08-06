from configparser import ConfigParser
import os
from tkinter import *
from tkinter import filedialog


def get_ini_file():
    ws = Tk()
    ws.title('Database config file is missing')
    ws.geometry('400x100')

    returned_values = {}

    def get_file():
        returned_values['filename'] = filedialog.askopenfilename()
        ws.quit()

    def quit():
        returned_values['filename'] = None
        ws.quit()

    label1 = Label(ws, text="Would You like to select the configuration file?",
                   font=('Aerial', 12))
    label1.pack(pady=20)

    btn1 = Button(ws, text='select file', command=get_file)
    btn1.pack(expand=True, side=LEFT)

    btn2 = Button(ws, text='cancel', command=quit)
    btn2.pack(expand=True, side=RIGHT)
    ws.mainloop()

    ini_file = returned_values.get('filename')
    return ini_file


def config(ini_file):
    if not os.path.exists(ini_file):
        ini_file1 = get_ini_file()
        if ini_file1 is None:
            raise FileNotFoundError('{}'.format(ini_file))
        else:
            ini_file = ini_file1

    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(ini_file)

    db = {}
    if parser.has_section(parser.sections()[0]):
        params = parser.items(parser.sections()[0])
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(parser.sections()[0], ini_file))
    return db


if __name__ == '__main__':
    config(r"D:\Python\MySQL\database.ini")