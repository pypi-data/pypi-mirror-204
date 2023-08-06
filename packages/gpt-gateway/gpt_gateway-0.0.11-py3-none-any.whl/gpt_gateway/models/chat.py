"""
Config for chat-related functionality
"""

from pydantic import BaseModel, Field
from .chatmodel import ChatModelName
from typing import Optional


class CollectionChatConfig(BaseModel):
    """Config for Collection chat-related functionality"""    
    model_name          : ChatModelName = Field(description="The model associated with this configuration")
    rate_limit_messages : int           = Field(description="The total number of messages allowed in the rate limit time period across all collection users")
    rate_limit_hours    : int           = Field(description="The number of hours in the rate limit time period")
    prompt_task_id      : Optional[int] = Field(description="The prompt task id of the prompt to use chat with this collection")


    