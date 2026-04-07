import random
import logging
from typing import Any

from .base import MessageHandler

logger = logging.getLogger(__name__)


class RepeatHandler(MessageHandler):
    """随机复读处理器 (F2)"""

    async def should_handle(self, event: dict[str, Any]) -> bool:
        """判断是否处理: 群消息 + 随机概率命中"""
        if not self.config.repeat.enabled:
            return False

        if event.get("post_type") != "message":
            return False

        if event.get("message_type") != "group":
            return False

        # 随机概率判断
        roll = random.randint(0, 99)
        hit = roll < self.config.repeat.probability
        if hit:
            logger.debug(f"复读命中: roll={roll}, prob={self.config.repeat.probability}")
        return hit

    async def handle(self, event: dict[str, Any], send_func) -> None:
        """复读消息"""
        group_id = event.get("group_id")
        raw_message = event.get("raw_message", "")

        logger.info(f"复读消息: group={group_id}, message={raw_message[:50]}")

        await send_func(
            action="send_group_msg",
            params={
                "group_id": group_id,
                "message": raw_message,
            },
        )
