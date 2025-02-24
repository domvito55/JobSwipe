# -*- coding: utf-8 -*-
"""
File Name: userService.py
Description: This module contains the service class for managing user business logic.
Author: MathTeixeira
Date: October 11, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

from fastapi.encoders import jsonable_encoder
from core.database import getNoSqlConn
from models import User
from bson import ObjectId

import logging

logger = logging.getLogger("uvicorn")


class AuthService:
  """
  A service class for managing user business logic.
  """
  # ----------------------------- Create
  @staticmethod
  async def createUser(collectionName: str, user: User) -> User:
    """
    Create a new user document.

    This method takes a User object, properly handles the UserInfoSchema,
    and inserts the user data into the specified collection in the database.

    Args:
      collectionName (str): The name of the collection to insert the document into.
      user (User): The user data to be inserted.

    Returns:
      User: The created user document, or None if an error occurred.

    Raises:
      Exception: Any exception that occurs during the creation process is caught,
                 logged, and results in returning None.
    """
    # Use 'jsonable_encoder' directly on the 'seeker' object
    user_json = jsonable_encoder(user, exclude={"id"})

    createdUser = getNoSqlConn().insertDocument(collectionName, user_json)

    # Convert the ObjectId to string for the response
    if "_id" in createdUser and isinstance(createdUser["_id"], ObjectId):
      createdUser["id"] = str(createdUser["_id"])
      del createdUser["_id"]  # Remove '_id' to avoid confusion

    return User.model_validate(createdUser)

  # ------------------------------ Retrieve
  @staticmethod
  async def getUserByFilters(collectionName: str, filters: dict) -> User:
    """
    Retrieve a user document by a specified filters.

    Args:
      collectionName (str): The name of the collection to search in.
      filters (dict): The filters to search by.

    Returns:
      User: The seeker document that matches the field-value pair.
    """
    user = getNoSqlConn().findDocumentByFilters(collectionName, filters)
    if "_id" in user and isinstance(user["_id"], ObjectId):
      user["id"] = str(user["_id"])
      del user["_id"]  # Remove '_id' to avoid confusion

    user = User.model_validate(user)
    return user

  # --------------------------- Update
  @staticmethod
  async def updateUser(collectionName: str, filters: dict, user: User) -> bool:
    """
    Update an existing user document by a specified filters.

    Args:
      collectionName (str): The name of the collection to update the document in.
      filters (dict): The filters to search by.
      user (User): The updated user data.

    Returns:
      bool: True if the document was updated, False otherwise.
    """
    try:
      user = jsonable_encoder(user)
      updateResult = getNoSqlConn().setDocument(collectionName, filters, user)
      return updateResult is not None
    except Exception as e:
      logging.error(f"Error updating user: {e}")
      return False

  # --------------------------- Delete
  @staticmethod
  async def deleteUser(collectionName: str, filters: dict) -> bool:
    """
    Delete a user document by a specified field and its value.

    Args:
      collectionName (str): The name of the collection to delete the document from.
      filters (dict): The filters to search by.

    Returns:
      bool: True if the document was deleted, False otherwise.
    """
    try:
      deleteResult = getNoSqlConn().deleteDocument(collectionName, filters)
      return deleteResult
    except Exception as e:
      logging.error(f"Error deleting seeker: {e}")
      return False

