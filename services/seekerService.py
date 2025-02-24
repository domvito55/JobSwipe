# -*- coding: utf-8 -*-
"""
File Name: seekerService.py
Description: This module contains the business logic for managing chat history.
Author: MathTeixeira
Date: December 3, 2024
Version: 3.0.1
License: MIT License
Contact Information: mathteixeira55
"""

from datetime import datetime
from fastapi.encoders import jsonable_encoder
from core.database import getNoSqlConn
from core.config import noSql
from models import Seeker
from schemas import PersonalInfoSchema, SkillSchema, EducationSchema

import logging

logger = logging.getLogger("uvicorn")

class SeekerService:
  """
  A service class for managing seeker business logic.
  """
  # ----------------------------- Create
  @staticmethod
  async def createSeeker(seekerCollection: str, seeker: Seeker) -> Seeker:
    """
    Create a new seeker document.

    This method takes a Seeker object, properly handles the PersonalInfoSchema,
    and inserts the seeker data into the specified collection in the database.

    Args:
      collectionName (str): The name of the collection to insert the document into.
      seeker (Seeker): The seeker data to be inserted.

    Returns:
      Seeker: The created seeker document, or None if an error occurred.

    Raises:
      Exception: Any exception that occurs during the creation process is caught,
                 logged, and results in returning None.
    """
    try:
      seeker = SeekerService.parsing(seeker)
    except Exception as e:
      logger.error(f"Error parsing seeker: {e}")
      return Exception(f"Error parsing seeker: {e}")

    # Use 'jsonable_encoder' directly on the 'seeker' object
    seeker_json = jsonable_encoder(seeker)

    # Check if the user exists
    if not getNoSqlConn().findDocumentByFilters(noSql.USERS_COLLECTION,
                                                {"id":  seeker_json["userId"]}):
      logger.error(f"User does not exist with id {str(seeker_json['userId'])}")
      raise Exception(f"User does not exist with id {str(seeker_json['userId'])}")

    createdSeeker = getNoSqlConn().insertDocument(seekerCollection, seeker_json)

    return Seeker.model_validate(createdSeeker)

  # ------------------------------ Retrieve
  @staticmethod
  async def getSeekers(collectionName: str) -> list[Seeker]:
    """
    Retrieve all seeker documents from a specified collection.

    Args:
      collectionName (str): The name of the collection to retrieve the documents from.

    Returns:
      list[Seeker]: A list of all seeker documents in the collection.
    """
    listSeekers = getNoSqlConn().findAllDocuments(collectionName)
    listSeekers = [Seeker.model_validate(seeker) for seeker in listSeekers]

    return listSeekers

  @staticmethod
  async def getSeekerByFilters(collectionName: str, filters: dict) -> Seeker:
    """
    Retrieve a seeker document by a specified filters.

    Args:
      collectionName (str): The name of the collection to search in.
      filters (dict): The filters to search by.

    Returns:
      Seeker: The seeker document that matches the field-value pair.
    """
    seeker = getNoSqlConn().findDocumentByFilters(collectionName, filters)

    if seeker is None:
      logger.warning(f"Seeker not found with filters: {filters}")
      return None

    seeker = Seeker.model_validate(seeker)
    return seeker

  @staticmethod
  async def getListSeekerByQuery(collectionName: str, query: dict) -> list[Seeker]:
    """
    Retrieve a list of seekers using a query.

    Args:
      collectionName (str): The name of the collection to search in.
      query (dict): The mongo query to search by.

    Returns:
      Seeker: The seeker document that matches the field-value pair.
    """
    listSeeker = getNoSqlConn().findListDocumentsByQuery(collectionName, query)
    listSeeker = [Seeker.model_validate(seeker) for seeker in listSeeker]

    return listSeeker

  # --------------------------- Update
  @staticmethod
  async def patchSeeker(collectionName: str, filters: dict,
                              seeker: Seeker) -> bool:
    """
    Update an existing seeker document by a specified filters.

    Args:
      collectionName (str): The name of the collection to update the document in.
      filters (dict): The filters to search by.
      seeker (Seeker): The updated seeker data.

    Returns:
      bool: True if the chat history was successfully updated, False otherwise.
    """
    try:
      seeker = jsonable_encoder(seeker)
      updateResult = getNoSqlConn().setDocument(collectionName,
                                                   filters, seeker)
      return Seeker.model_validate(updateResult)
    except Exception as e:
      logger.error(f"Error updating seeker: {e}")
      return None

  # --------------------------- Delete
  @staticmethod
  async def deleteSeeker(seekerCollection: str, filters: dict) -> bool:
    """
    Delete a chat history document by a specified field and its value.

    Args:
      collectionName (str): The name of the collection to delete the document from.
      filters (dict): The filters to search by.

    Returns:
      bool: True if the document was deleted, False otherwise.
    """
    try:
      deleteResult = getNoSqlConn().deleteDocument(seekerCollection, filters)
      return deleteResult
    except Exception as e:
      logger.error(f"Error deleting seeker: {e}")
      return None

  # --------------------------- Auxiliary Methods
  @staticmethod
  def parsing(seeker: Seeker) -> Seeker:
    """
    Parse the Seeker object to ensure the correct data types.

    Args:
      seeker (Seeker): The seeker object to parse.

    Returns:
      Seeker: The parsed seeker object.
    """
    # Ensure 'personalInfo' is an instance of 'PersonalInfoSchema'
    if isinstance(seeker.personalInfo, dict):
      seeker.personalInfo = PersonalInfoSchema(**seeker.personalInfo)
    # Ensure 'createdDate' is a 'date' object
    if isinstance(seeker.createdDate, str):
      seeker.createdDate = datetime.strptime(seeker.createdDate,
                                             '%Y-%m-%d').date()
    for skill_type in ['primarySkills', 'secondarySkills']:
      skills_dict = getattr(seeker, skill_type, {})
      if not isinstance(skills_dict, dict):
        logger.warning(f"Seeker {skill_type} is not a dictionary")
        continue
      for key in ['technicalSkills', 'transferableSkills']:
        skills = skills_dict.get(key, [])
        for i, skill in enumerate(skills):
          if isinstance(skill, dict):
            skills[i] = SkillSchema(**skill)
        skills_dict[key] = skills
      setattr(seeker, skill_type, skills_dict)
    if isinstance(seeker.educationList, list):
      for key, education in enumerate(seeker.educationList):
        if isinstance(education, dict):
          seeker.educationList[key] = EducationSchema(**seeker.educationList[key])
    return seeker
