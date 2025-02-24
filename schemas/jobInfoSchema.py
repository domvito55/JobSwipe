# -*- config: utf-8 -*-
"""
File Name: personalInfoSchema.py
Description: This script defines the seeker model for representing and managing
 job data in the application.
Author: MathTeixeira
Date: Octouber 10, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

### imports ###
from pydantic import ConfigDict, Field, BaseModel, ConfigDict


class JobInfoSchema(BaseModel):
  """
  User model for representing and managing job data in the application.

  Attributes:
  """
  # jobDescription: { type: String
  #     description: "The job title" },
  jobDescription: None | str = Field(None,
                        description="The job description",
                        json_schema_extra={"example": "Software Engineer"})
  # email: { type: String,
  #     description: "The email address associated wiht this job" },
  email: None | str = Field(None,
                     description="The email associated with this job",
                     json_schema_extra={"example": "tony.stark@starkindustries.com"})
  # phone: { type: Number, description: "The phone number associated wiht this job" },
  phone: None | int = Field(None,
                     description="The phone number associated wiht this job",
                     json_schema_extra={"example": 5551234567})
  # street: { type: String, description: "The street address for this job" },
  street: None | str = Field(None,
                      description="The street address for this job",
                      json_schema_extra={"example": "10880 Malibu Point"})
  # city: { type: String, description: "The city address for this job" },
  city: None | str = Field(None,
                    description="The city address for this job",
                    json_schema_extra={"example": "Malibu"})
  # province: { type: String,
  #     description: "The province address for this job" },
  province: None | str = Field(None,
                        description="The province address for this job",
                        json_schema_extra={"example": "California"})
  # postalCode: { type: String,
  #     description: "The postal code address for this job" },
  postalCode: None | str = Field(None,
                          description="The postal code for this job",
                          json_schema_extra={"example": "90265"})
  # country: { type: String, description: "The country address for this job" }
  country: None | str = Field(None,
                        description="The Country address for this job",
                        json_schema_extra={"example": "United States of America"})

  model_config = ConfigDict(from_attributes=True)
