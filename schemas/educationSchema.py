# -*- config: utf-8 -*-
"""
File Name: EducationModel.py
Description: This script defines the Education model.
Author: MathTeixeira
Date: September 23, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

### imports ###
from typing import List
from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import date

from schemas.skillSchema import SkillSchema


class EducationSchema(BaseModel):
  """
  User model for representing and managing user data in the application.

  Attributes:
  """
  # title: { type: String, required: true },
  title: str = Field(
      None,
      description="Education Title",
      json_schema_extra={"example": "Bachelor of Science"})
  # levelOfEducation: {type: String, required: true},
  levelOfEducation: str = Field(
      None,
      description="Level of education Primary, Secondary, Post-Secondary, etc.",
      json_schema_extra={"example": "Primary"})
  # fieldOfStudy: { type: String, required: true },
  fieldOfStudy: str = Field(
      None,
      description="Field of study, e.g. Computer Science, Engineering, etc.",
      json_schema_extra={"example": "Computer Science"})
  # institution: { type: String, required: true },
  institution: str = Field(
      None,
      description="Institution where the education was obtained.",
      json_schema_extra={"example": "MIT"})
  # location: { type: String, required: true },
  location: str = Field(None,
                        description="Location of the institution.",
                        json_schema_extra={"example": "Cambridge"}
                        )
  # expectedDuration: { type: Number, required: true },
  expectedDuration: float = Field(
      None,
      description="Expected duration of the education in months.",
      json_schema_extra={"example": 48})
  # startDate: { type: Date, required: true },
  startDate: date = Field(None,
                          description="Starting date of the education.",
                          json_schema_extra={"example": "2020-09-01"}
                        )
  # endDate: { type: Number, required: true },
  endDate: date = Field(None,
                        description="Ending date of the education.",
                        json_schema_extra={"example": "2024-09-01"})
  # technicalSkills: [SkillSchema],
  technicalSkills: List[SkillSchema] = Field(
      default=[],
      description="List of technical skills",
      json_schema_extra={"example": [{"skillName": "JavaScript",
                                      "proficiencyLevel": "Beginner",
                                      "yearsOfExperience": 3,
                                      "certified": True}]})
  # transferableSkills: [SkillSchema]
  transferableSkills: List[SkillSchema] = Field(
      default=[],
      description="List of technical skills",
      json_schema_extra={"example": [{"skillName": "Communication",
                                      "proficiencyLevel": "Advanced",
                                      "yearsOfExperience": 5,
                                      "certified": True}]})
  # gpa: { type: Number, required: false },
  gpa: float | None = Field(None,
                            description="gpa of the user",
                            json_schema_extra={"example": 3.5})
  # gpaScale: {
  #     type: Number,
  #     required: function() { return this.gpa != null; } // Only required if gpa is provided
  # },
  gpaScale: float | None = Field(
      None,
      description="gpa scale of the user",
      json_schema_extra={"example": 4.0})

  @model_validator(mode='after')
  def check_gpa_and_scale(cls, values):
    gpa = values.gpa
    gpaScale = values.gpaScale

    if gpa is not None and gpaScale is None:
      raise ValueError('gpaScale is required if gpa is provided.')

    return values

  model_config = ConfigDict(from_attributes=True)
