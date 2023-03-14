"""
character component for frame
"""
from typing import Optional


class CharacterPosition:
    """
    coordinate of character

    """

    x: float = 0
    y: float = 0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Character:
    """
    character component in frame

    """

    def __init__(
        self,
        res_name: Optional[str] = None,
        position: Optional[CharacterPosition] = CharacterPosition(0, 0),
    ):
        """
        constructor for character

        @param res_name: character file name, if leave none, default is voice over
        @param position: choose from 1, 2, 3, 4, the character position on stage
        """
        self.res_name: str = res_name
        self.position: CharacterPosition = position

    def get_character(self) -> str:
        """
        getter for character resources

        @return:
        """
        return self.res_name

    def set_character(
        self, res_name: str, position: CharacterPosition = Optional[CharacterPosition]
    ):
        """
        setter for character
        @param res_name: new resources name
        @param position: new position for this character
        @return:
        """
        self.res_name = res_name
        self.position = position
