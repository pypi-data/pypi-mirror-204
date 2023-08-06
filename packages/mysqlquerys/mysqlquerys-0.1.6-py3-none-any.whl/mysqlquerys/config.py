from configparser import ConfigParser
import os


def config(ini_file):
    if not os.path.exists(ini_file):
        raise FileNotFoundError('{}'.format(ini_file))
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(ini_file)
    # print(len(parser.sections()))
    # get section, default to postgresql
    db = {}
    if parser.has_section(parser.sections()[0]):
        params = parser.items(parser.sections()[0])
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(parser.sections()[0], ini_file))
    return db


if __name__ == '__main__':
    params = config(r"D:\Python\MySQL\database.ini")
    params = config(r"D:\Python\MySQL\web_db.ini")
    print(params)