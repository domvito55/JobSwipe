# -*- config: utf-8 -*-
"""
File Name: personalInfoSchema.py
Description: This script defines the seeker model for representing and managing
 user data in the application.
Author: MathTeixeira
Date: July 6, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

### imports ###
from datetime import date
from pydantic import ConfigDict, Field, BaseModel, ConfigDict


class UserProtectedSchema(BaseModel):
  """
  User model for representing and managing user data in the application.

  Attributes:
  """
  # userId: { type: String, required: true,
  #     description: "The user Id" },
  id: str = Field(None,
                      description="The user Id of the user",
                      json_schema_extra={"example": "123456"})
  # username: { type: String, required: true,
  #     description: "The username" },
  username: str = Field(None,
                         description="The username of the user",
                         json_schema_extra={"example": "tonystark"})
  # role: { type: String, required: false,
  #     description: "the role of the user" },
  role: None | str = Field(None,
                          description="The role of the user",
                          json_schema_extra={"example": "seeker"})
  # createdDate: { type: Date, required: true,
  #     description: "The date of creation" },
  createdDate: date = Field(None,
                           description="The date of creation",
                           json_schema_extra={"example": "2024-09-23"})

  model_config = ConfigDict(from_attributes=True)
