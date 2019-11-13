import User as us
import subprocess
import os
import ISecretObject as isec
import Secreter as sec


# return user with list of secrets and his salt


def get_user(username, key):
    try:
        file = open("users\\%s\\sa" % username + ".txt", "r")
        salt = file.readline()
        file1 = open("users\\%s\\cn" % username + ".txt", "rb")
        control = file1.readline()
        sec.decrypt_data(control, key)  # should throw exception if password is wrong
        secs = get_secret_list(username)
        return us.User(username, salt, secs, control)
    except Exception as e:
        wrong_pas_msg()
        return us.User()
    finally:
        file.close()
        file1.close()

def get_secret(username, info):
    file = open("users\\" + username.lower() + "\\data\\%s" % info + ".txt", "rb")
    return isec.ISecretObject(info, file.readline())


def get_salt(username):
    file = open("users\\" + username.lower() + "\\sa" + ".txt", "rb")
    ct = file.readline()
    return ct


def wrong_pas_msg():
    print("Sorry, wrong password!")


def copy2clip(txt):
    cmd = 'echo ' + str(txt) + '|clip'
    return subprocess.check_call(cmd, shell=True)


def get_available_user_list():
    us = []
    try:
        return os.listdir("users\\")
    except FileNotFoundError as e:
        return us


def get_available_secret_list(username):
    se = []
    try:
        return os.listdir("users\\" + username.lower() + "\\data\\")
    except FileNotFoundError as e:
        return se


def get_secret_list(username):
    sec_list = []
    for s in get_available_secret_list(username):
        file = open("users\\" + username.lower() + "\\data\\%s" % s, "rb")
        se_data = file.readline()
        file.close()
        sec_list.append(isec.ISecretObject(s, se_data))

    return sec_list


def add_secret(user, secret):
    file = open("users\\" + user.name.lower() + "\\data\\%s" % secret.info + ".txt", "wb")
    file.write(secret.data_en)
    file.close()


def create_user_file(user):
    file = None

    create_user_folder(user)

    file = open("users\\" + user.name.lower() + "\\sa" + ".txt", "wb")
    file1 = open("users\\" + user.name.lower() + "\\cn" + ".txt", "wb")
    file.write(user.salt)
    file1.write(user.control)
    if file is not None:
        file.close()
    if file1 is not None:
        file1.close()



def create_user_folder(user):
    try:
        os.mkdir("users")
    except FileExistsError as e:
        a = "Folder exists"
    finally:
        try:
            os.mkdir("users\\%s" % user.name.lower())
            os.mkdir("users\\%s\\data" % user.name.lower())

        except Exception as e:
            nothing_happens = ""
