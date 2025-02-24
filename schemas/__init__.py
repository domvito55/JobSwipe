# -*- coding: utf-8 -*-
"""
Package Name: schemas
Description: This package contains the Pydantic schemas for data validation and
 serialization in the chat application.
Author: MathTeixeira
Date: July 11, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55

This package includes the following schemas:
- ResponseSchema: Used for structuring API responses.
- UserSchema: Defines the structure for user data.
- UserProtectedSchema: A version of UserSchema with protected fields.
- ChatRequestSchema: Structures incoming chat requests.

These schemas are used throughout the application to ensure data consistency
and to provide clear interfaces for API requests and responses.
"""

# from .responseSchema import ResponseSchema
from .skillSchema import SkillSchema
from .educationSchema import EducationSchema
from .personalInfoSchema import PersonalInfoSchema
from .responseSchema import ResponseSchema
from .seekerFilterSchema import SeekerFilterSchema
from .jobInfoSchema import JobInfoSchema
from .userProtectedSchema import UserProtectedSchema
from .applicationSchema import ApplicationSchema

__all__ = [
    'ResponseSchema', 'SkillSchema', 'EducationSchema', 'PersonalInfoSchema',
    'SeekerFilterSchema', 'JobInfoSchema', 'UserProtectedSchema', 'ApplicationSchema']
