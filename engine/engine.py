"""
----------------------------
The Best Visual Novel Engine
        Yui Engine
----------------------------

contain all basic information to build a visual novel
"""

import os
import time
import engine_io

from typing import Optional
from module.exception import EngineError
from module.config_manager import ConfigLoader
from utils.file_utils import check_file_valid, check_folder_valid, abs_dir
from utils.status import StatusCode
from .frame import BasicFrame, Frame
from .frame_checker import FrameChecker

VERSION = "1.0.0"


def engine_exception_handler(func):
    """
    exception decorator for engine

    @param func: function to be decorated
    @return:
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e_msg:
            print("Engine Error: ", str(e_msg))
            return StatusCode.FAIL

    return wrapper


class Engine:
    """
    Engine main class, used to edit frame in project
    """

    # metadata for the game file, update automatically
    # through calling update_metadata() function
    __metadata: dict = {}

    # activated variables, initialized after class construct,
    # should be UPDATED ON TIME every time they changed
    __game_content: dict[int, BasicFrame] = {}
    __head: int = BasicFrame.VOID_FRAME_ID  # the head of the frame list
    __tail: int = BasicFrame.VOID_FRAME_ID  # the tail of the frame list
    __last_fid: int = BasicFrame.VOID_FRAME_ID  # the last used fid (frame id)
    __all_fids: set[int] = set()  # all fids in set

    def __init__(
        self,
        project_dir: str,
        config_dir: str,
        game_file_name: Optional[str] = None,
    ):
        """
        constructor for engine

        @param project_dir: project directory
        @param config_dir: config file directory
        @param game_file_name: game file name (not directory)
        @return:
        """
        if not check_folder_valid(project_dir):
            raise EngineError(f"project {project_dir} not exist")

        # self.__project_dir = project_dir
        self.__config = ConfigLoader(config_dir=config_dir)
        self.__engine_config = self.__config.engine()

        resource_config_raw = self.__config.resources()
        resource_config_abs = {}
        for k, v in resource_config_raw.items():
            resource_config_abs[k] = abs_dir(project_dir, v)
        self.__frame_checker = FrameChecker(
            project_dir=project_dir, config=self.__config
        )

        if not game_file_name:
            game_file_name = self.__config.engine()["default_game_file"]
        self.__game_file_dir = abs_dir(project_dir, game_file_name)

        loader = self.__engine_config["loader"]
        dumper = self.__engine_config["dumper"]
        if hasattr(engine_io, loader) and hasattr(engine_io, dumper):
            self.__loader = getattr(engine_io, loader)
            self.__dumper = getattr(engine_io, dumper)
        else:
            raise EngineError("initialize fail due to cannot find loader/dumper")

        if check_file_valid(self.__game_file_dir):
            with open(self.__game_file_dir, "r", encoding="UTF-8") as file_stream:
                game_content_raw = self.__loader(file_stream)
            self.__metadata = game_content_raw[0]
            self.__game_content = game_content_raw[1]
            self.__last_fid = self.__metadata["last_fid"]
            self.__head = self.__metadata["head"]
            self.__tail = self.__metadata["tail"]
            self.__all_fids = set(self.__game_content.keys())

    @engine_exception_handler
    def __update_metadata(self):
        """
        update the metadata by global variable

        @return:
        """
        self.__metadata["engine_version"] = VERSION
        self.__metadata["update_at"] = time.time()
        self.__metadata["total_frame_len"] = len(self.__game_content.keys())
        self.__metadata["last_fid"] = self.__last_fid
        self.__metadata["head"] = self.__head
        self.__metadata["tail"] = self.__tail

    @engine_exception_handler
    def append_frame(self, frame: BasicFrame, force: bool = False) -> int:
        """
        add frame to the end of the frame list

        @param force: force push mode, ignore checking frame valid
        @param frame: frame to be added
        @return:  frame id

        """
        # check frame
        if not force:
            check_output = self.__frame_checker.check(frame)
            if check_output[0] == Frame:
                raise EngineError(check_output[1])

        # generate the fid
        if self.__last_fid == Frame.VOID_FRAME_ID:
            fid = 0
        else:
            fid = self.__last_fid + 1

        # change the current last frame's next frame pointer
        if self.__last_fid != Frame.VOID_FRAME_ID:
            self.__game_content[self.__last_fid].action.change_next_f(next_f_id=fid)

        # update activated variables
        self.__game_content[fid] = frame
        self.__last_fid = fid
        self.__all_fids.add(fid)

        # update head and tail
        if self.__head == Frame.VOID_FRAME_ID:
            self.__head = fid

        self.__tail = fid

        return fid

    @engine_exception_handler
    def insert_frame(self, dest_frame_id: int, from_frame_id: int):
        """
        move the from_frame to the next of the dest_frame_id

        @param dest_frame_id: distinct frame id
        @param from_frame_id: from which frame

        """
        if dest_frame_id not in self.__all_fids or from_frame_id not in self.__all_fids:
            raise EngineError("insert fail, frame not exist")

        from_frame = self.__game_content[from_frame_id]
        dest_frame = self.__game_content[dest_frame_id]

        from_frame.action.next_f = dest_frame.action.next_f
        from_frame.action.prev_f = dest_frame_id

        if dest_frame.action.next_f != Frame.VOID_FRAME_ID:
            self.__game_content[dest_frame.action.next_f].action.prev_f = from_frame
        else:
            self.__tail = from_frame_id

        dest_frame.action.next_f = from_frame

    @engine_exception_handler
    def remove_frame(self, frame_id: int):
        """
        remove the frame from game content

        @param frame_id: id of frame

        """
        if frame_id not in self.__all_fids:
            raise EngineError("remove fail, frame not exist")

        cur_frame = self.__game_content[frame_id]
        if cur_frame.action.prev_f != Frame.VOID_FRAME_ID:
            self.__game_content[
                cur_frame.action.prev_f
            ].action.next_f = cur_frame.action.next_f
        else:
            self.__head = cur_frame.action.next_f

        if cur_frame.action.next_f != Frame.VOID_FRAME_ID:
            self.__game_content[
                cur_frame.action.next_f
            ].action.prev_f = cur_frame.action.prev_f
        else:
            self.__tail = cur_frame.action.prev_f

        # update metadata
        self.__all_fids.remove(frame_id)

    @engine_exception_handler
    def commit(self):
        """
        commit all the change to the local game file

        @return: commit status
        """
        self.__update_metadata()
        game_content_raw = [self.__metadata, self.__game_content]
        try:
            with open(self.__game_file_dir, "w", encoding="UTF-8") as file_stream:
                self.__dumper(game_content_raw, file_stream)
        except Exception as e_msg:
            raise EngineError("fail to commit due to: " + str(e_msg))
