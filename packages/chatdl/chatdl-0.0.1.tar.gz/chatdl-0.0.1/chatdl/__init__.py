# -*- coding:utf-8 -*-

__version__ = '0.0.1'

if __name__ == '__main__':
    from os.path import split

    n = split(split(__file__)[0])[1]
    print(n, __version__)
