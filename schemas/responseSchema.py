# -*- coding: utf-8 -*-
"""
File Name: responseSchema.py
Description: This module defines the ResponseSchema using Pydantic for data
 validation and serialization. The ResponseSchema is used to structure the API
 responses in the chat application.
Author: MathTeixeira
Date: July 11, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

from pydantic import BaseModel, ConfigDict
from typing import List, Union

from models import Seeker, Job
from .userProtectedSchema import UserProtectedSchema

class ResponseSchema(BaseModel):
  """
    ResponseSchema for structuring API responses.

    This schema defines the structure of responses sent from the API.
    It can accommodate different types of messages and includes a status code.

    Attributes:
        message (Union[str, ChatHistory, UserProtectedSchema]): The message returned in the response.
            It can be a string, a ChatHistory object, or a UserProtectedSchema object.
        code (int): The status code of the response.
    """
  message: Union[str, Seeker, List[Seeker], Job, List[Job], UserProtectedSchema]
  code: int

  model_config = ConfigDict(json_schema_extra={
      "example": {
          "message": "Operation successful",
          "code": 200
      }
  })
