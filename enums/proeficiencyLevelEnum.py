"""
File Name: proficiencyLevelEnum.py
Description: This file contains the ProficiencyLevelEnum enumeration class.
Author: MathTeixeira
Date: September 23, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55

This file contains the ProficiencyLevelEnum enumeration class, which defines the
  possible proficiency levels for a skill.
"""
from enum import Enum

class ProficiencyLevelEnum(str, Enum):
  BEGINNER = 'Beginner'
  INTERMEDIATE = 'Intermediate'
  ADVANCED = 'Advanced'
  EXPERT = 'Expert'
