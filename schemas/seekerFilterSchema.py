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
from datetime import date
from typing import Dict, List
from pydantic import BaseModel, Field, ConfigDict, model_validator
from sqlalchemy import JSON
from passlib.context import CryptContext

from schemas import EducationSchema, SkillSchema, PersonalInfoSchema


class SeekerFilterSchema(BaseModel):
  """
  Seeker model class for representing and managing seeker data in the application.

  Attributes:
    id (int): The unique identifier for the user.
    username (str): The username of the user.
    passwordHash (str): The hashed password of the user.
    personalInfo (PersonalInfoSchema): The user personal information.
    primarySkills (Dict[str, List[SkillSchema]]): Primary skills, divided into technical and transferable skills.
    secondarySkills (Dict[str, List[SkillSchema]]): Secondary skills, divided into technical and transferable skills.
    educationList (List[EducationSchema]): List of education entries for the user.
    createdDate (date): Starting date of the education.
  """
  # username
  username: str | None = Field(
      None,
      description="The username of the user",
      json_schema_extra={"example": "tonystark"})
  # personalInfo: { type: PersonalInfoSchema, required: true },
  personalInfo: PersonalInfoSchema | None = Field(
    None,
    description="The user personal information")
  # primarySkills: {
  #     technicalSkills: {
  #         type: [SkillSchema],
  #         validate: [skillsLimit, '{PATH} must have between 3 and 5 entries']
  #     },
  #     transferableSkills: {
  #         type: [SkillSchema],
  #         validate: [skillsLimit, '{PATH} must have between 3 and 5 entries']
  #     }
  # }
  primarySkills: Dict[str, List[SkillSchema]] | None = Field(
      None,
      description=
      "Primary skills, divided into technical and transferable skills")
  # secondarySkills: {
  #     technicalSkills: {
  #         type: [SkillSchema],
  #         validate: [skillsLimit, '{PATH} must have between 3 and 5 entries']
  #     },
  #     transferableSkills: {
  #         type: [SkillSchema],
  #         validate: [skillsLimit, '{PATH} must have between 3 and 5 entries']
  #     }
  # }
  secondarySkills: Dict[str, List[SkillSchema]] | None = Field(
      None,
      description=
      "Secondary skills, divided into technical and transferable skills")
  # education: [EducationSchema],
  educationList: List[EducationSchema] | None = Field(
      None,
      description="List of education entries for the user")

  # created_date: {
  #     type: Date,
  #     default: Date.now,
  #     description: "When was this entry created? Automatically generated."
  # }
  createdDate: date | None = Field(None,
                            description="Starting date of the education")

#   class Config:
#     json_schema_extra = {
#         "example": {
#             "username": "tonystark",
#             "personalInfo": {
#                 "firstName": "Tony",
#                 "middleName": "Edward",
#                 "lastName": "Stark",
#                 "email": "tony.stark@starkindustries.com",
#                 "phone": 5551234567,
#                 "street": "10880 Malibu Point",
#                 "city": "Malibu",
#                 "province": "California",
#                 "country": "USA",
#                 "postalCode": "90265"
#             },
#             "primarySkills": {
#                 "technicalSkills": [{
#                     "skillName": "Engineering",
#                     "proficiencyLevel": "Expert",
#                     "yearsOfExperience": 25,
#                     "certified": True
#                 }, {
#                     "skillName": "Artificial Intelligence",
#                     "proficiencyLevel": "Expert",
#                     "yearsOfExperience": 15,
#                     "certified": True
#                 }, {
#                     "skillName": "Materials Science",
#                     "proficiencyLevel": "Expert",
#                     "yearsOfExperience": 12,
#                     "certified": True
#                 }],
#                 "transferableSkills": [{
#                     "skillName": "Leadership",
#                     "proficiencyLevel": "Expert",
#                     "yearsOfExperience": 20,
#                     "certified": True
#                 }, {
#                     "skillName": "Innovation",
#                     "proficiencyLevel": "Expert",
#                     "yearsOfExperience": 18,
#                     "certified": True
#                 }, {
#                     "skillName": "Project Management",
#                     "proficiencyLevel": "Expert",
#                     "yearsOfExperience": 15,
#                     "certified": True
#                 }, {
#                     "skillName": "Crisis Managementn",
#                     "proficiencyLevel": "Expert",
#                     "yearsOfExperience": 10,
#                     "certified": True
#                 }, {
#                     "skillName": "Public Speaking",
#                     "proficiencyLevel": "Expert",
#                     "yearsOfExperience": 8,
#                     "certified": True
#                 }]
#             },
#             "secondarySkills": {
#                 "technicalSkills": [{
#                     "skillName": "Software Development",
#                     "proficiencyLevel": "Intermediate",
#                     "yearsOfExperience": 10,
#                     "certified": True
#                 }],
#                 "transferableSkills": [{
#                     "skillName": "Teamwork",
#                     "proficiencyLevel": "Intermediate",
#                     "yearsOfExperience": 5,
#                     "certified": True
#                 }]
#             },
#             "educationList": [{
#                 "title": "Master's in Computer Science",
#                 "levelOfEducation": "Master's",
#                 "institution": "MIT",
#                 "location": "Massachusetts",
#                 "expectedDuration": 24,
#                 "startDate": "2000-09-01",
#                 "endDate": "2004-06-30",
#                 "fieldOfStudy": "Computer Science"
#             }],
#             "createdDate": "2024-09-23"
#         }
#     }
