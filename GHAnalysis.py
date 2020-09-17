import json
import os
import argparse

class Data:
    def __init__(self, dict_address : str = None, reload : int = 0):
        if reload == 1:
            self.load(dict_address)
        if dict_address is None and not os.path.exists("people_event.json") and not os.path.exit("obj_event.json") and not os.path.exists("people_obj_event.path"):
            raise RuntimeError("Error:Failed")

    def load(self,dict_address):
        people_event = {}
        obj_event = {}
        people_obj_event = {}
        for root, dic, files in os.walk(dict_address):
            for fil in files:
                if fil[-5:] == ".json":
                    event = ["PushEvent","IssueCommentEvent","IssuesEvent","PullRequestEvent"]
                    json_path = fil
                    x = open(dict_address + "/" + json_path, "r", encoding="UTF-8").readlines()
                    for i in x:
                        i = json.loads(i)
                        if i["type"] in event:
                            self.add_people_event(i, people_event)
                            self.add_obj_event(i, obj_event)
                            self.add_people_obj_event(i, people_obj_event)

        with open("people_event.json", "a") as fil:
            json.dump(people_event,fil)
        with open("obj_event.json", "a") as fil:
            json.dump(obj_event,fil)
        with open("people_obj_event.json", "a") as fil:
            json.dump(people_obj_event, fil)

    def add_people_event(self, dic, people_event):
        id = dic["actor"]["login"]
        event = dic["type"]
        if id not in people_event:
            people_event[id] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        people_event[id][event] += 1

    def add_obj_event(self, dic, obj_event):
        obj = dic["repo"]["name"]
        event = dic["type"]
        if obj not in obj_event:
            obj_event[obj] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        obj_event[obj][event] += 1

    def add_people_obj_event(self, dic, people_obj_event):
        id = dic["actor"]["login"]
        obj = dic["repo"]["name"]
        event = dic["type"]
        if id not in people_obj_event:
            people_obj_event[id] = {}
            people_obj_event[id][obj] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        if obj not in people_obj_event[id]:
            people_obj_event[id][obj] = {"PushEvent":0,"IssueCommentEvent":0,"IssuesEvent":0,"PullRequestEvent":0}
        people_obj_event[id][obj][event] += 1

    def get_people_event(self, user, event):
        x = open("people_event.json", "r", encoding="utf-8").read()
        data = json.loads(x)
        return data[user][event]

    def get_obj_event(self, repo, event):
        x = open("obj_event.json", "r", encoding="utf-8").read()
        data = json.loads(x)
        return data[repo][event]

    def get_people_obj_event(self, user, repo, event):
        x = open("people_obj_event.json", "r", encoding="utf-8").read()
        data = json.loads(x)
        return data[user][repo][event]

class Run:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-i', '--init')
        self.parser.add_argument('-u', '--user',type=str)
        self.parser.add_argument('-r', '--repo',type=str)
        self.parser.add_argument('-e', '--event',type=str)
        self.doing()

    def doing(self):
        args = self.parser.parse_args()
        if args.init:
            data = Data(args.init, 1)
        elif args.user and args.event and not args.repo:
            data = Data()
            print(data.get_people_event(args.user, args.event))
        elif args.repo and args.event and not args.user:
            data = Data()
            print(data.get_obj_event(args.repo, args.event))
        elif args.user and args.repo and args.event:
            data = Data()
            print(data.get_people_obj_event(args.user, args.repo, args.event))

if __name__ == '__main__':
    a = Run()
