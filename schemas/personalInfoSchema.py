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
from pydantic import ConfigDict, Field, BaseModel, ConfigDict


class PersonalInfoSchema(BaseModel):
  """
  User model for representing and managing user data in the application.

  Attributes:
    firstName (str): The first name of the seeker.
    middleName (str): The middle name of the seeker.
    lastName (str): The last name of the seeker.
    email (str): The email address of the seeker.
    phone (int): The phone number of the seeker.
    street (str): The street address of the seeker.
    city (str): The city address of the seeker.
    province (str): The province address of the seeker.
    postalCode (str): The postal code of the seeker.
    country (str): The country address of the seeker.
  """
  # firstName: { type: String, required: true,
  #     description: "The first name of the seeker" },
  firstName: str = Field(None,
                         description="The first name of the seeker",
                         json_schema_extra={"example": "Anthony"})
  # middleName: { type: String, required: false,
  #     description: "The middle name of the seeker" },
  middleName: None | str = Field(None,
                          description="The middle name of the seeker",
                          json_schema_extra={"example": "Edward"})
  # lastName: { type: String, required: true,
  #     description: "The last name of the seeker" },
  lastName: str = Field(None,
                        description="The last name of the seeker",
                        json_schema_extra={"example": "Stark"})
  # email: { type: String, required: true,
  #     description: "The email address of the seeker" },
  email: str = Field(None,
                     description="The email of the seeker",
                     json_schema_extra={"example": "tony.stark@starkindustries.com"})
  # phone: { type: Number, description: "The phone number of the seeker" },
  phone: None | int = Field(None,
                     description="The phone number of the seeker",
                     json_schema_extra={"example": 5551234567})
  # street: { type: String, description: "The street address of the seeker" },
  street: None | str = Field(None,
                      description="The street address of the seeker",
                      json_schema_extra={"example": "10880 Malibu Point"})
  # city: { type: String, description: "The city address of the seeker" },
  city: None | str = Field(None,
                    description="The city address of the seeker",
                    json_schema_extra={"example": "Malibu"})
  # province: { type: String,
  #     description: "The province address of the seeker" },
  province: None | str = Field(None,
                        description="The province address of the seeker",
                        json_schema_extra={"example": "California"})
  # postalCode: { type: String,
  #     description: "The postal code address of the seeker" },
  postalCode: None | str = Field(None,
                          description="The postal code of the seeker",
                          json_schema_extra={"example": "90265"})
  # country: { type: String, description: "The country address of the seeker" }
  country: None | str = Field(None,
                        description="The Country address of the seeker",
                        json_schema_extra={"example": "United States of America"})

  model_config = ConfigDict(from_attributes=True)

