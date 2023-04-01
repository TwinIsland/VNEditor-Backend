from functools import wraps

from module.config_manager import ConfigLoader
from utils.exception import ControllerException
from utils.status import StatusCode
from utils.return_type import ReturnList, ReturnDict, ReturnStatus

from .project_controller import Task
from engine.frame import Frame, FrameModel


def engine_controller_exception_handler(func):
    """
    exception decorator for router

    @param func: function to be decorated

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e_msg:
            print(f"Project Controller Error ({type(e_msg).__name__}): ", str(e_msg))
            return ReturnStatus(status=StatusCode.FAIL, msg=str(e_msg))

    wrapper: func
    return wrapper


class EngineController:
    """
    class for engine controller

    """

    def __init__(self, config_dir: str):
        """
        constructor for router class

        """
        config_loader = ConfigLoader(config_dir=config_dir)
        self.__engine_config: dict = config_loader.engine()

    @engine_controller_exception_handler
    def get_frame(self, task: Task, fid: int) -> ReturnDict:
        """
        get frame by frame id

        @param task: current task
        @param fid: frame id
        @return: dictionary contain frame information

        """
        engine = task.project_engine
        frame = engine.get_frame(fid)
        return ReturnDict(status=StatusCode.OK, content=frame.__dict__)

    @engine_controller_exception_handler
    def get_frame_id(self, task: Task) -> ReturnList:
        """
        get all frame id

        @param task:
        @return: list of ordered frame id

        """
        engine = task.project_engine
        fids = engine.get_ordered_fid()
        if fids == StatusCode.FAIL:
            raise ControllerException("get frame id fails")

        return ReturnList(status=StatusCode.OK, content=fids)

    @engine_controller_exception_handler
    def get_engine_meta(self, task: Task) -> ReturnDict:
        """
        get the metadata for engine

        @return: metadata for engine

        """
        engine = task.project_engine
        return ReturnDict(status=StatusCode.OK, content=engine.get_engine_meta())

    @engine_controller_exception_handler
    def append_frame(self, task: Task, frame_component_raw: FrameModel) -> ReturnList:
        """
        append frame: Frame into game content

        @return: metadata for engine

        """
        engine = task.project_engine
        frame_component = frame_component_raw.to_frame().__dict__
        frame = engine.make_frame(_type=type(Frame), **frame_component)
        fid = engine.append_frame(frame)
        if fid == StatusCode.FAIL:
            return ReturnList(status=StatusCode.FAIL)
        else:
            return ReturnList(status=StatusCode.OK, content=[fid])
