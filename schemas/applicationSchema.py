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


class ApplicationSchema(BaseModel):
  """
  User model for representing and managing user data in the application.

  Attributes:
  """
  # userId: { type: String, required: true,
  #     description: "The user Id" },
  userId: str = Field(None,
                      description="The user Id of the user",
                      json_schema_extra={"example": "6733aec175eb0fba49f14363"})
  # jobId: { type: String, required: true,
  #     description: "The job Id" },
  jobId: str = Field(None,
                      description="The job Id of the job",
                      json_schema_extra={"example": "6735a696d6cff11d57b1d9b1"})
  # status: { type: String, required: true,
  #     description: "The status of the application" },
  newStatus: str = Field(None,
                      description="The new status for the application",
                      json_schema_extra={"example": "apply"})
  oldStatus: str | None = Field(None,
                      description="The new status for the application",
                      json_schema_extra={"example": "apply"})

  model_config = ConfigDict(from_attributes=True)
