import argparse
import json
import os

class Data:
    def __init__(self, path:str=None):
        self.__dir_addr = path
        if path:
            print("初次运行初始化")
            self.__read_json()
            self.__analysis()
            self.__save_newjson()
        else:
            self.__read_newjson()

    def __read_json(self):
        self.__dicts = []
        for root, dirs, files in os.walk(self.__dir_addr):
            for file in files:
                if file[-5:] == '.json' and file[-6:] != '1.json' and file[-6:] != '2.json' and file[-6:] != '3.json':
                    with open(file, 'r', encoding='utf-8') as f:
                        self.__jsons = [x for x in f.read().split('\n') if len(x)>0] #列表生成式，读取json文件并按行分割
                        for self.__json in self.__jsons:
                            self.__dicts.append(json.loads(self.__json))  #将json文件转换成字典，并添加到列表中

    def __analysis(self):
        self.__types = ['PushEvent', 'IssueCommentEvent', 'IssuesEvent', 'PullRequestEvent']
        self.__cnt_perP = {}
        self.__cnt_perR = {}
        self.__cnt_perPperR = {}
        for self.__dict in self.__dicts:
            # 如果属于四种事件之一 则增加相应值
            if self.__dict['type'] in self.__types:
                self.__event = self.__dict['type']
                self.__name = self.__dict['actor']['login']
                self.__repo = self.__dict['repo']['name']
                self.__cnt_perP[self.__name + self.__event] = self.__cnt_perP.get(self.__name + self.__event, 0) + 1
                self.__cnt_perR[self.__repo + self.__event] = self.__cnt_perR.get(self.__repo + self.__event, 0) + 1
                self.__cnt_perPperR[self.__name + self.__repo + self.__event] = self.__cnt_perPperR.get(self.__name
                                    + self.__repo + self.__event, 0) + 1

    def __save_newjson(self):
        with open("1.json", 'w', encoding='utf-8') as f:
            json.dump(self.__cnt_perP, f)
        with open("2.json", 'w', encoding='utf-8') as f:
            json.dump(self.__cnt_perR, f)
        with open("3.json", 'w', encoding='utf-8') as f:
            json.dump(self.__cnt_perPperR, f)
        print("Save to json files successfully!")


    def __read_newjson(self):
        self.__cnt_perP = {}
        self.__cnt_perR = {}
        self.__cnt_perPperR = {}
        with open("1.json", encoding='utf-8') as f:
            self.__cnt_perP = json.load(f)
        with open("2.json", encoding='utf-8') as f:
            self.__cnt_perR = json.load(f)
        with open("3.json", encoding='utf-8') as f:
            self.__cnt_perPperR = json.load(f)

    def query_cnt_user(self, user:str, event:str) -> int:
        return self.__cnt_perP.get(user + event, 0)

    def query_cnt_repo(self, repo:str, event:str) -> int:
        return self.__cnt_perR.get(repo + event, 0)

    def query_cnt_user_and_repo(self, user, repo, event) -> int:
        return self.__cnt_perPperR.get(user + repo + event, 0)

def run():
    my_parser = argparse.ArgumentParser(description='analysis the json file')
    my_parser.add_argument('-i', '--init', help='json file path')
    my_parser.add_argument('-u', '--user', help='username')
    my_parser.add_argument('-r', '--repo', help='repository name')
    my_parser.add_argument('-e', '--event', help='type of event')
    args = my_parser.parse_args()

    if args.init:
        my_data = Data(path=args.init)
    else:
        my_data =  Data()
        if args.event:
            if args.user:
                if args.repo:
                    print(my_data.query_cnt_user_and_repo(args.user, args.repo, args.event))
                else:
                    print(my_data.query_cnt_user(args.user, args.event))
            else:
                if args.repo:
                    print(my_data.query_cnt_repo(args.repo, args.event))
                else:
                    print("missing argument: user or repo")
        else:
            print("missing argument: event")


if __name__ == '__main__':
    run()