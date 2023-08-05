from abc import ABCMeta, abstractmethod


class BaseEngineModel(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def _from_engine_format(cls, data: dict) -> "BaseEngineModel":
        pass

    @abstractmethod
    def _to_engine_format(self) -> dict:
        pass
