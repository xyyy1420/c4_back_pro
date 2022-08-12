from .file_mode.file_control import FileControl


class BaseControl(object):
    def __init__(self) -> None:
        self.file_control = FileControl()

    def create_policy(self, data):
        pass

    def update_policy(self, data):
        pass

    def delete_policy(self, data):
        pass

    def set_policy_to_sensor(self, data):
        pass
