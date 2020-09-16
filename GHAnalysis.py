import argparse
import json
import os

class Data:
    def __init__(self, path:str=None):
        self.__dir_addr = path

        if path:
            print("初次运行初始化")
            if not os.path.exists(self.__dir_addr):
                raise RuntimeError("Path doesn't exist.")
            self.__read_1()
            self.__analysis()
            self.__save2json()
        else:
            self.__read_2()

    def __read_1(self):
        self.__dicts = []
        for root, dirs, files in os.walk(self.__dir_addr):
            for file in files:
                if file[-5:] == '.json' and file[-6:] != '1.json' and file[-6:] != '2.json' and file[-6:] != '3.json':
                    with open(file, 'r', encoding='utf-8') as f:
                        self.__jsons = [x for x in f.read().split('\n') if len(x)>0]
                        for self.__json in self.__jsons:
                            self.__dicts.append(json.loads(self.__json))


def run():
    my_parser = argparse.ArgumentParser(description='analysis the json file')
    my_parser.add_argument('-i', '--init', help='json file path')
    my_parser.add_argument('-u', '--user', help='username')
    my_parser.add_argument('-r', '--repo', help='repository name')
    my_parser.add_argument('-e', '--event', help='type of event')
    args = my_parser.parse_args()
if __name__ == '__main__':
    run()