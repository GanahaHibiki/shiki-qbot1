from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from config import Config


class MessageHandler(ABC):
    """消息处理器基类"""

    def __init__(self, config: "Config"):
        self.config = config

    @abstractmethod
    async def should_handle(self, event: dict[str, Any]) -> bool:
        """判断是否处理该消息"""
        pass

    @abstractmethod
    async def handle(self, event: dict[str, Any], send_func) -> None:
        """处理消息

        Args:
            event: OneBot 消息事件
            send_func: 发送消息的回调函数
        """
        pass
