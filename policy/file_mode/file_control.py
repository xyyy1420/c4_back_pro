import os


class FileControl(object):
    def __init__(self) -> None:
        self.base_path = '/home/jxy/policy/'

    def create_base_path(self):
        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)

    def create_new_policy_path(self):
        pass

    def delete_policy_path(self):
        pass
