# -*- config: utf-8 -*-
"""
File Name: skillSetModel.py
Description: This script defines the skill set model.
Author: MathTeixeira
Date: September 23, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

### imports ###
from enums.proeficiencyLevelEnum import ProficiencyLevelEnum
from pydantic import BaseModel, Field


class SkillSchema(BaseModel):
  """
  User model for representing and managing user data in the application.

  Attributes:
  """
  # skillName: { type: String, required: true },
  skillName: str = Field(None, description="skill name",
                        json_schema_extra={"example": "JavaScript"})
  # proficiencyLevel: { type: String, required: true },
  #     enum: ['Beginner', 'Intermediate', 'Advanced', 'Expert'] },
  proficiencyLevel: None | ProficiencyLevelEnum = Field(
      None,
      description="Proficiency level",
      json_schema_extra={"example": "Beginner"})
  # yearsOfExperience: { type: Number, required: true },
  yearsOfExperience: None | int = Field(None,
                                 description="years of experience",
                                 json_schema_extra={"example": 3})
  # certified: { type: Boolean, required: false, default: false }
  certified: None | bool = Field(False, description="certified",
      json_schema_extra={"example": True})
