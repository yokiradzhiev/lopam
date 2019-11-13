import Secreter as sec
class ISecretObject:
    def __init__(self, *args):
        if len(args) == 2:
            self.info = args[0]
            self.data_en = args[1]
        elif len(args) == 3:
            self.info = args[0]
            self.data_en = sec.encrypt_data(args[1], args[2])
        else:
            raise Exception('No constructor with %d arguments!' % len(args))



    def change_info(self, new_info):
        self.info = new_info

    def delete_all(self):
        self.info = ""
        self.data_en = ""
