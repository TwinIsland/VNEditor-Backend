"""
action component for frame
"""
from engine.component.branch import BranchTree
from typing import Optional


class Action:
    """
    Frame attribute, guild the next step after current frame
    """

    def __init__(
        self, next_f_id: int, prev_f_id: int, branch: Optional[BranchTree] = None
    ):
        """
        constructor for Action

        @param prev_f_id: previous frame id
        @param next_f_id: next frame id
        @param branch: special action, i.e. branch frame
        """
        self.prev_f: int = prev_f_id
        self.next_f: int = next_f_id
        self.branch: BranchTree = branch

    def change_next_f(self, next_f_id: int):
        """
        change the next frame pointer

        @param next_f_id: the new next frame
        @return:
        """
        self.next_f = next_f_id

    def change_prev_f(self, prev_f_id: int):
        """
        change the prev frame pointer

        @param prev_f_id: the new next frame
        @return:
        """
