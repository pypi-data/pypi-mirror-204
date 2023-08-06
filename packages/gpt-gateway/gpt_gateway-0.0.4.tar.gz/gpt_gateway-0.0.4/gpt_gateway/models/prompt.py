from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum
from time import time


class PrompRole(str, Enum):
    system   : str = "system"
    user     : str = "user"
    assistant: str = "assistant"
    
    def __str__(self):
        return str(self.value)


class Prompt(BaseModel):
   id     : int        = Field(description="The unique ID of the prompt")
   org_id : int        = Field(description="The unique ID of the org that this prompt belongs to")
   role   : PrompRole  = Field(description="The role of the prompt")
   content: str        = Field(description="The text of the prompt")
   created_at: float   = Field(description="The time the prompt was created")


class PromptPostRequest(BaseModel):
   role   : PrompRole  = Field(description="The role of the prompt")
   content: str        = Field(description="The text of the prompt")


   
   
   