import os
import random
import ISecretObject

#salt can't be encrpted
class User:

    def __init__(self, *args):
        if len(args) == 0:
            self.name = "Bad"
            self.secrets = []
            self.salt = "bad"
            self.control = "bad"
        elif len(args) == 1:
            self.name = args[0]
            self.secrets = []
            self.salt = os.urandom(random.randint(0, 182))
            self.control = ""
        elif len(args) == 4:
            self.name = args[0]
            self.secrets = args[1]
            self.salt = args[2]
            self.control = args[3]
        else:
            raise Exception('No constructor with %d arguments!' % len(args))


    def AddSecret(self, secret):
        self.secrets.append(secret)


    def AddControl(self, control):
        self.control = control

    def DeleteSecter(self, secret):
        self.secrets.remove(secret)