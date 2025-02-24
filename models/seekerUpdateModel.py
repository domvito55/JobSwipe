# -*- config: utf-8 -*-
"""
File Name: seekerModel.py
Description: This script defines the seeker model for representing and managing
 user data in the application.
Author: MathTeixeira
Date: September 23, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

### imports ###
from datetime import datetime
from typing import Dict, List
from pydantic import model_validator
from sqlalchemy import JSON
from sqlmodel import Field, Column, VARCHAR

from schemas.educationSchema import EducationSchema
from schemas.skillSchema import SkillSchema
from schemas.personalInfoSchema import PersonalInfoSchema

from .seekerModel import Seeker

class SeekerUpdate(Seeker):
  """
  Seeker model class for representing and managing seeker data in the application.

  Attributes:
    userId (str): The user Id.
    primarySkills (Dict[str, List[SkillSchema]]): Primary skills, divided into technical and transferable skills.
    secondarySkills (Dict[str, List[SkillSchema]]): Secondary skills, divided into technical and transferable skills.
    
    educationList (List[EducationSchema]): List of education entries for the user.
    createdDate (date): Created date.
    updatedDate (date): Last Updated date.
    areaOfInterest (str): The area of interest of the user.


    TODO:
    remove  personalInfo (PersonalInfoSchema): The user personal information.
    add     list of roles
    add     add workList
    add     calculate the years of experience

  """
  primarySkills: None | Dict[str, List[SkillSchema]] = Field(
      None,
      sa_column=Column(JSON),
      description=
      "Primary skills, divided into technical and transferable skills")
  
  createdDate: None | datetime = Field(
      default=None,
      description="Starting date of the education"
  )


  class Config:
    pass
