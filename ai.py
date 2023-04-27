#!/usr/bin/env python

from requests import session
from json import load, dump
from os.path import exists
import inquirer

black = "\033[30m"
red = "\033[31m"
green = '\033[32m'
yellow = "\033[33m"
blue = "\033[34m"
magenta = '\033[35m'
cyan = "\033[36m"
white = "\033[37m"
defualt = "\033[0m"
clear = "\033c"

hfchaturl = "https://huggingface.co/chat/"
hfconurl = "https://huggingface.co/chat/conversation/"

sess = session()
if exists("config.json"):
    with open("config.json", "r") as cf:
        cookie = load(cf)
    sess.cookies.update(cookie)
else:
    sess.get(hfchaturl)
    with open("config.json", "w") as cf:
        dump(sess.cookies.get_dict(), cf)

settings = {
    'parameters': {
        'temperature': 0.9,
        'top_p': 0.95,
        'repetition_penalty': 1.2,
        'top_k': 50,
        'truncate': 1024,
        'watermark': False,
        'max_new_tokens': 1024,
        'stop': [
            '<|endoftext|>',
        ],
        'return_full_text': False,
    },
    'stream': False,
    'options': {
        'use_cache': False,
    },
}


def format(ans):
    return ans.replace("<br>", "\n").replace("<|endoftext|>", "").replace("<|linktofact>", "\n")


def chat(ask, id, loop=0):

    settings['inputs'] = ask
    response = sess.post(
        f'{hfconurl}{id}',
        json=settings,
    ).json()

    if isinstance(response, dict):
        err_msg = f'{red}Error : {response.get("error", response.get("message", "Unknown"))}'
        if loop > 3:
            return err_msg
        print(f"{err_msg}, {yellow}({loop+1}) retrying...")
        return chat(ask, id, loop+1)
    elif isinstance(response, list):
        try:
            return format(response[0].get("generated_text"))
        except:
            return f"{red}--Error--"
    else:
        return f"{red}--Error--"


def delete(id, title):
    response = sess.delete(
        f'{hfconurl}{id}')
    if response.status_code == 200:
        print(f"{green}Conversation Deleted Successfully : {title} - {id}")
    else:
        print(f'{red}Conversation Deletion : {response.json().get("message", "Failed")}')


def new():
    res = sess.post(hfconurl).json()
    return res["conversationId"]


def start(id=None, title=None):
    print(clear)
    if id is None:
        id = new()
        neww = True
    else:
        neww = False
    print(f"{magenta}Conversation ID: {white}{id}")
    if title != None:
        print(f"{magenta}Conversation Title: {white}{title}")
    print(f'{yellow}Type just the word "back" to go back to the menu')
    print()
    while True:
        ask = input(f"{white}> ")
        if ask == "back":
            print(clear)
            return
        print(f'{green}{chat(ask, id)}')
        if neww:
            sess.post(f'{hfconurl}{id}/summarize').json()
            neww = False


def getall():
    data = sess.get(
        f'{hfchaturl}__data.json?x-sveltekit-invalidated=1_').json()["nodes"][0]["data"]
    return [{"id": data[i+1], "title": data[i+2] if i+2 < len(data) and isinstance(data[i+2], str) else "Untitled"}
            for i in range(len(data)) if isinstance(data[i], dict) and "id" in data[i]]


def deleteall():
    data = getall()
    if len(data) == 0:
        print(clear)
        print(f'{red}No Conversations Available')
        print()
        return
    print(clear)
    for ele in data:
        delete(ele["id"], ele["title"])
    print()


def choose():
    data = getall()
    if len(data) == 0:
        print(clear)
        print(f'{red}No Conversations Available')
        print()
        return None,None
    options = [
        inquirer.List('id',
                      message="Choose conversation?",
                      choices=[*[x["title"] + " - " + x["id"] for x in data
                                 ],
                               'Back'
                               ]

                      )
    ]
    id = inquirer.prompt(options)['id']
    if id == "Back":
        print(clear)
        return None, None
    return id.split(" - ")


def main():
    print(clear)
    print(f'\t{red}Welcome to {green}HugChat - AI in your Terminal, {yellow}visit {hfchaturl} for Graphical Interface.')
    print("\n")
    
    while True:
        options = [
            inquirer.List('action',
                          message="What would you like to do?",
                          choices=[
                              'Chat',
                              'Start new conversation',
                              'Delete conversation',
                              'Delete all conversations',
                              'Quit'
                          ]
                          )
        ]

        answer = inquirer.prompt(options)['action']

        if answer == 'Chat':
            title, id = choose()
            if id != None:
                start(id, title)

        elif answer == 'Start new conversation':
            start()

        elif answer == 'Delete conversation':
            title, id = choose()
            if id != None:
                print(clear)
                delete(id, title)
                print()

        elif answer == 'Delete all conversations':
            deleteall()

        else:
            print(clear)
            print(defualt)
            exit(1)


if __name__ == "__main__":
    main()
