# -*- config: utf-8 -*-
"""
File Name: jobUpdateModel.py
Description: This script defines the job update model for representing and managing
 job update data in the application.
Author: MathTeixeira
Date: November 13, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

### imports ###
from .jobModel import Job
from datetime import datetime
from typing import Dict, List
from sqlmodel import Field

class JobUpdate(Job):
    jobTitle: None | str = Field(
        default=None,
        description="The job title"
    )
    status: None | Dict[str, List[str]] = Field(
        default=None,
        description="The status of the job"
    )
    createdDate: None | datetime = Field(
        default=None,
        description="Starting date of the education"
    )

    class Config:
        # Inherit any necessary configuration from the base model
        pass