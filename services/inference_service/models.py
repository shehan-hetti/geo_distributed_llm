# Description: This file contains the model for the todo item.
# The model is a pydantic model which is a data validation library.
# The model is used in the main.py file
from pydantic import BaseModel


class Prompts(BaseModel):
    id: int
    prompt: str
