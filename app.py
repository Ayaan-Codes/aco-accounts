from tkinter import *
import json

def login(user):
    uN = input('Please enter your username: ')
    pW = input('Please enter your password: ')

    if uN in user.keys():
        if pW == user[uN]:
            print('Welcome Back!')
        else:
            print('Password Incorrect')
            return False

    else:
        print('Hello! Welcome to ACO!')
        user[uN] = pW
        writeUsers(user)
        return True


def readUsers():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def writeUsers(user):
    with open('users.json', 'w+') as f:
        json.dump(user, f)

users =readUsers()
success = login(users)