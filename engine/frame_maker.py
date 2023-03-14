from engine.frame import BasicFrame, Frame
from typing import Optional
from module.config_manager import ConfigLoader


class FrameMaker:
    def __init__(self):
        self.__config = ConfigLoader

    def maker(self, frame: BasicFrame) -> list[bool, Optional[str]]:
        """
        entry for frame check, register your own checker there

        @param frame: frame to be checked
        @return: status

        """
        if isinstance(frame, Frame):
            pass

        # add your own checker here !

        return [False, None]
