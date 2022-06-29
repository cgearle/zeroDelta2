from pathlib import Path


def create_file(path, name, ext):
    try:
        if not file_exists(path, name, ext):
            open(path + name + '.' + ext, 'x')  # x = create
    except Exception as e:
        print(e)


def file_exists(path, name, ext):
    try:
        path = Path(path + name + '.' + ext)
        return path.is_file()
    except Exception as e:
        print(e)


def file_empty(path, name, ext):
    try:
        path = Path(path + name + '.' + ext)
        return path.stat().st_size == 0
    except Exception as e:
        print(e)


def read_dictionary_file(path, name, ext):
    try:
        if file_exists(path, name, ext):
            file = open(path + name + '.' + ext, 'r')
            lines = file.readlines()
            results = {}
            for line in lines:
                delimited = line.split('\t')
                results[delimited[0]] = delimited[1]
            file.close()
            return results
    except Exception as e:
        print(e)


def dump_dictionary_in_file(path, name, ext, d):
    try:
        file = open(path + name + '.' + ext, 'w')
        for k, v in d.items():
            file.write(k + '\t' + v + '\n')
    except Exception as e:
        print(e)