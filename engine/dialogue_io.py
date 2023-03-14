import pickle
from module.config_manager import ConfigLoader


class DialogueIO:
    BUFFER_LIMIT = 5e8

    def __init__(self, project_dir: str, config: ConfigLoader):
        self.__config = config
        self__meta_file_name = config.engine()["dialogue_meta"]
        self.__buffer: int = 0
        self.__id: int = 0
        self.__cur_file_stream = 0

    def dumper(self, content: str):
        if self.__buffer + len(content) > self.BUFFER_LIMIT:
            pass
