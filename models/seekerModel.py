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
from sqlmodel import Field, SQLModel, Column, VARCHAR

from schemas.educationSchema import EducationSchema
from schemas.skillSchema import SkillSchema
from schemas.personalInfoSchema import PersonalInfoSchema


class Seeker(SQLModel):
  """
  Seeker model class for representing and managing seeker data in the application.

  Attributes:
    userId (str): The user Id.
    personalInfo (PersonalInfoSchema): The user personal information.
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
  # userId: "foregin key to the user",
  userId: str = Field(
      ...,
      sa_column=Column("userId", VARCHAR, unique=True, index=True),
      description="The user Id")
  # personalInfo: { type: PersonalInfoSchema},
  personalInfo: None | PersonalInfoSchema = Field(
      default=None,
      sa_column=Column(JSON),
      description="The user personal information")
  # status: { type: dict[str, List[str]], required: true }
  status: None | Dict[str, List[str]] = Field(
      default={
          "applied": [],
          "rejected": [],
          "accepted": [],
          "declined": []
        },
      sa_column=Column(JSON),
      description="The status of the job")

  # primarySkills: {
  #     required: true,
  #     technicalSkills: {
  #         type: [SkillSchema],
  #         validate: [skillsLimit, '{PATH} must have between 3 and 5 entries']
  #     },
  #     transferableSkills: {
  #         type: [SkillSchema],
  #         validate: [skillsLimit, '{PATH} must have between 3 and 5 entries']
  #     }
  # }
  primarySkills: Dict[str, List[SkillSchema]] = Field(
      sa_column=Column(JSON),
      description=
      "Primary skills, divided into technical and transferable skills")
  # secondarySkills: {
  #     required: true,
  #     technicalSkills: {
  #         type: [SkillSchema],
  #         validate: [skillsLimit, '{PATH} must have between 3 and 5 entries']
  #     },
  #     transferableSkills: {
  #         type: [SkillSchema],
  #         validate: [skillsLimit, '{PATH} must have between 3 and 5 entries']
  #     }
  # }
  secondarySkills: None | Dict[str, List[SkillSchema]] = Field(
      default=None,
      sa_column=Column(JSON),
      description=
      "Secondary skills, divided into technical and transferable skills")
  # education: [EducationSchema],
  educationList: None | List[EducationSchema] = Field(
      default=None,
      sa_column=Column(JSON),
      description="List of education entries for the user")

  # created_date: {
  #     type: Date,
  #     default: Date.now,
  #     description: "When was this entry created? Automatically generated."
  # }
  createdDate: datetime = Field(default_factory=datetime.now,
                            description="Created date")
  # updatedDate: {
  #     type: Date,
  #     default: Date.now,
  #     description: "When was this entry updated? Automatically generated."
  # }
  updatedDate: datetime = Field(default_factory=datetime.now,
                            description="Last Updated date")
  # areaOfInterest: {
  #     type: String,
  #     description: "The area of interest of the user."
  # }
  areaOfInterest: None | str = Field(
      default=None,
      sa_column=Column(VARCHAR),
      description="The area of interest of the user"
      )
  
#   # Validate that each list in primarySkills has between 3 and 5 entries
#   @model_validator(mode='after')
#   def validate_skills_limit(cls, values):
#     for skill_type in ['primarySkills']:  #, 'secondarySkills']:
#       skills_dict = getattr(values, skill_type, {})
#       for key in ['technicalSkills', 'transferableSkills']:
#         skills = skills_dict.get(key, [])
#         if not (3 <= len(skills) <= 5):
#           print(f"{key} in {skill_type} must have between 3 and 5 entries")
#           raise ValueError(
#               f"{key} in {skill_type} must have between 3 and 5 entries")
#     return values

  class Config:
    json_schema_extra = {
        "example": {
            "userId": "6733aec175eb0fba49f14363",
            "personalInfo": {
                "firstName": "Tony",
                "middleName": "Edward",
                "lastName": "Stark",
                "email": "tony.stark@starkindustries.com",
                "phone": 5551234567,
                "street": "10880 Malibu Point",
                "city": "Malibu",
                "province": "California",
                "country": "USA",
                "postalCode": "90265"
            },
            "primarySkills": {
                "technicalSkills": [{
                    "skillName": "Engineering",
                    "proficiencyLevel": "Expert", # TODO Make it int
                    "yearsOfExperience": 25,
                    "certified": True # Remove it
                }, {
                    "skillName": "Artificial Intelligence",
                    "proficiencyLevel": "Expert",
                    "yearsOfExperience": 15,
                    "certified": True
                }, {
                    "skillName": "Materials Science",
                    "proficiencyLevel": "Expert",
                    "yearsOfExperience": 12,
                    "certified": True
                }],
                "transferableSkills": [{
                    "skillName": "Leadership",
                    "proficiencyLevel": "Expert",
                    "yearsOfExperience": 20,
                    "certified": True
                }, {
                    "skillName": "Innovation",
                    "proficiencyLevel": "Expert",
                    "yearsOfExperience": 18,
                    "certified": True
                }, {
                    "skillName": "Project Management",
                    "proficiencyLevel": "Expert",
                    "yearsOfExperience": 15,
                    "certified": True
                }, {
                    "skillName": "Crisis Managementn",
                    "proficiencyLevel": "Expert",
                    "yearsOfExperience": 10,
                    "certified": True
                }, {
                    "skillName": "Public Speaking",
                    "proficiencyLevel": "Expert",
                    "yearsOfExperience": 8,
                    "certified": True
                }]
            },
            "secondarySkills": {
                "technicalSkills": [{
                    "skillName": "Software Development",
                    "proficiencyLevel": "Intermediate",
                    "yearsOfExperience": 10,
                    "certified": True
                }],
                "transferableSkills": [{
                    "skillName": "Teamwork",
                    "proficiencyLevel": "Intermediate",
                    "yearsOfExperience": 5,
                    "certified": True
                }]
            },
            "educationList": [{
                "title": "Master's in Computer Science",
                "levelOfEducation": "Master's", # TODO Make it int enum	
                "institution": "MIT",
                "location": "Massachusetts",
                "expectedDuration": 24,
                "startDate": "2000-09-01",
                "endDate": "2004-06-30",
                "fieldOfStudy": "Computer Science"
                # TODO skills limit it to 10 per education
            }],
            "areaOfInterest": "Artificial Intelligence",
            # TODO ADD workList
            # {
            #     "title": "Master's in Computer Science",
            #     "positionLevel": "Master's", # Make it int enum
            #     "institution": "MIT",
            #     "location": "Massachusetts",
            #     "startDate": "2000-09-01",
            #     "endDate": "2004-06-30",
            #     "fieldOfWork": "Computer Science"
            #     # skills limit it to 10 per education
            # }
        }
    }
