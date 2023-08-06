from cd2t.types.base import BaseDataType
from cd2t.RunTimeEnv import RunTimeEnv


class NoneDataType(BaseDataType):
    type = 'none'
    path_symbol = '°'

    def __init__(self) -> None:
        super().__init__()
        self.matching_classes.append(type(None))
