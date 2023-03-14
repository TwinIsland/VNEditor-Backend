"""
frame component for frame
"""

from engine.component.background import Background
from engine.component.character import Character
from engine.component.dialogue import Dialogue
from engine.component.music import Music
from engine.component.action import Action


class BasicFrame:
    """
    base modal for frame
    """

    VOID_FRAME_ID = -1  # indicate no frame

    def __init__(self, fid: int, action: Action):
        self.fid: int = fid
        self.action: Action = action

    def set_id(self, fid: int) -> None:
        """
        set frame id for current frame

        @param fid: new fid
        @return:
        """
        self.fid = fid

    def get_id(self) -> int:
        """
        get the id for current frame

        @return: frame id
        """
        return self.fid


class Frame(BasicFrame):
    """
    a normal frame
    """

    def __init__(
        self,
        fid: int,
        background: Background,
        chara: Character,
        music: Music,
        dialog: Dialogue,
        action: Action,
    ):
        """
        constructor for frame class

        @param fid: frame id, should be unique
        @param background: background
        @param chara: character
        @param music: music
        @param dialog: dialogue
        @param action: action
        """
        super().__init__(fid, action)
        self.background: Background = background
        self.chara: Character = chara
        self.music: Music = music
        self.dialog: Dialogue = dialog
