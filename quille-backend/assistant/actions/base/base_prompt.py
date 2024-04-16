from abc import ABC, abstractmethod


class BasePrompt(ABC):

    @abstractmethod
    def format(self) -> str:
        """Formats the prompt"""
        raise NotImplementedError
