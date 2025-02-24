# -*- coding: utf-8 -*-
"""
File Name: noSqlDatabase.py
Description: This module provides a class for interacting with a NoSQL database.
Author: MathTeixeira
Date: December 3, 2024
Version: 3.0.1
License: MIT License
Contact Information: mathteixeira55
"""

### Imports ###
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from pymongo.database import Database
from core.config import noSql

from bson import ObjectId

import logging

logger = logging.getLogger("uvicorn")


class NoSqlConnection:
  """
  A class to handle connections and operations with a NoSQL database.

  This class provides methods to connect to a NoSql database and perform basic
  operations.

  Attributes:
    dbUrl (str): The URL for the NoSql connection.
    dbName (str): The name of the database to connect to.
    NoSqlClient (MongoClient): The NoSql client instance.
    database (Database): The NoSql database instance.
  """

  _instance: 'NoSqlConnection | None' = None

  def __init__(self, dbUrl: str = noSql.URL, dbName: str = noSql.NAME):
    """
    Initialize the NoSqlConnection instance.

    Args:
      dbUrl (str): The URL for the NoSql connection. Defaults to the URL from noSqlConfig.
      dbName (str): The name of the database to connect to. Defaults to the NAME from noSqlConfig.
    """
    self.dbUrl: str = dbUrl
    self.dbName: str = dbName

    try:
      self.NoSqlClient: MongoClient = MongoClient(dbUrl)
      self.database: Database = self.NoSqlClient[dbName]
      logger.info("Connected to the NoSql database!")
    except ConnectionFailure as e:
      logger.error(f"Connection error: {e}")

  @classmethod
  def getInstance(cls) -> 'NoSqlConnection':
    """
    Get the singleton instance of NoSqlConnection.

    Returns:
      NoSqlConnection: The singleton instance of NoSqlConnection.
    """
    if cls._instance is None:
      cls._instance = cls()
    return cls._instance

  def shutdownDbClient(self) -> None:
    """
    Close the NoSql client connection.
    """
    self.NoSqlClient.close()
    logger.info("NoSql connection closed.")

  # Create
  def insertDocument(self, collectionName: str, document: dict) -> dict:
    """
    Insert a document into a specified collection.

    Args:
      collection_name (str): The name of the collection to insert the document into.
      document (dict): The document to be inserted.

    Returns:
      dict: The inserted document with its ID.
    """
    try:
      document = self.convertStringsToObjectIds(document)
      newDocument = self.database[collectionName].insert_one(document)
      insertedDocument = self.database[collectionName].find_one(
          {"_id": newDocument.inserted_id})
      insertedDocument = self.convertObjectIdsToStrings(insertedDocument)
      return insertedDocument
    except DuplicateKeyError as e:
      # Handle documents with duplicate identifiers
      logger.error(f"A document with this identifier already exists. {e}")
      raise ValueError(f"A document with this identifier already exists. {e}")
    except Exception as e:
      logger.error(f"Error inserting document: {e}")
      raise  Exception(f"Error inserting document: {e}")

  # Retrieve
  def findAllDocuments(self, collectionName: str) -> list:
    """
    Find all documents in a specified collection.

    Args:
      collectionName (str): The name of the collection to search in.

    Returns:
      list: A list of all documents in the collection.
    """
    try:
      documents = list(self.database[collectionName].find())
      documents = [self.convertObjectIdsToStrings(document) for document in documents] 
      return documents
    except Exception as e:
      logger.error(f"Error finding documents: {e}")
      return None

  def findDocumentByFilters(self, collection_name: str, filters: dict) -> dict:
    """
    Find a document in a specified collection by a filters.

    Args:
      collection_name (str): The name of the collection to search in.
      filters (dict): The filters to search by.
    Returns:
      dict: The found document or None if no document is found.
    """
    try:
      filters = self.convertStringsToObjectIds(filters)
      document = self.database[collection_name].find_one(filters)
      document = self.convertObjectIdsToStrings(document)
      return document
    except Exception as e:
      logger.error(f"Error finding document: {e}")
      return None

  def findListDocumentsByQuery(self, collection_name: str, query: dict) -> list[dict]:
    """
    Find a list of document in a specified collection given some.

    Args:
      collection_name (str): The name of the collection to search in.
      filters (dict): The filters to search by.
    Returns:
      list[dict]: The list of found documents.
    """
    try:
      query = self.convertStringsToObjectIds(query)
      listDocument = list(self.database[collection_name].find(query))
      listDocument = [self.convertObjectIdsToStrings(document) for document in listDocument]
      return listDocument
    except Exception as e:
      logger.error(f"Error finding documents: {e}")
      return None

  # ---------------------------------- Update
  # 1. ----- set operation
  def setDocument(self, collectionName: str, filters: dict,
                     newInfoDoc: dict) -> dict:
    """
    Update a document in a specified collection.

    Args:
      collectionName (str): The name of the collection to update the document in.
      filters (dict): The filters to find the document to update.
      newInfoDoc (dict): The new information to update the document with.

    Returns:
      dict: The updated document or None if the document was not updated.
    """
    try:
      filters = self.convertStringsToObjectIds(filters)
      newInfoDoc = self.convertStringsToObjectIds(newInfoDoc)

      newInfoDoc = {k: v for k, v in newInfoDoc.items() if v is not None}
      newInfoDoc["updatedDate"] = str(datetime.now())
      updatedDocument = self.database[collectionName].find_one_and_update(
          filters, {"$set": newInfoDoc}, return_document=True)
      
      updatedDocument = self.convertObjectIdsToStrings(updatedDocument)
      return updatedDocument
    except Exception as e:
      logger.error(f"Error updating document: {e}")
      return None


  def documentOperation(self, collectionName: str, filters: dict,
                     operation: dict) -> dict:
    """
    Update a document in a specified collection.

    Args:
      collectionName (str): The name of the collection to update the document in.
      filters (dict): The filters to find the document to update.
      operation (dict): The operation to update the document with.
      
    Returns:
      dict: The updated document or None if the document was not updated.
    """
    try:
      operation = {k: v for k, v in operation.items() if v is not None}
      operation.setdefault("$set", {})
      operation["$set"]["updatedDate"] = str(datetime.now())

      updatedDocument = self.database[collectionName].find_one_and_update(
          filters, operation, return_document=True)
      updatedDocument = self.convertObjectIdsToStrings(updatedDocument)
      return updatedDocument
    except Exception as e:
      logger.error(f"Error updating document: {e}")
      return None

  # Delete
  def deleteDocument(self, collectionName: str, filters: dict) -> bool:
    """
    Delete a document in a specified collection.

    Args:
      collectionName (str): The name of the collection to delete the document from.
      filters (dict): The filters to find the document to delete.

    Returns:
      bool: True if the document was deleted, False otherwise.
    """
    try:
      filters = self.convertStringsToObjectIds(filters)

      deleteResult = self.database[collectionName].delete_one(filters)
      return deleteResult.deleted_count > 0
    except Exception as e:
      logger.error(f"Error deleting document: {e}")
      return False
  
  def convertObjectIdsToStrings(self,  data: dict) -> dict:
    """
    Convert specific ObjectId fields to strings if they exist.

    Args:
      data (dict): The input dictionary.

    Returns:
      dict: The updated dictionary with fields converted to strings.
    """
    try:
      # _id is special case
      if "_id" in data and isinstance(data["_id"], ObjectId):
        data["id"] = str(data["_id"])
        del data["_id"]
      
      # Other fields can be added to this array
      for field in ["userId"]:
        if field in data and isinstance(data[field], ObjectId):
          data[field] = str(data[field])

      # Status is a dictionary with lists of ObjectIds
      if "status" in data and data["status"] is not None:
        defaultStatus = {
          "applied": [],
          "rejected": [],
          "accepted": [],
          "declined": []
        }
        status = data.get("status", defaultStatus)
        data["status"] = {
          key: [str(value) for value in values] if isinstance(values, list) else []
          for key, values in status.items()
        }
      return data

    except Exception as e:
      logger.error(f"Error converting ObjectIds to strings: {e}")
      raise Exception(f"Error converting ObjectIds to strings: {e}")
    
  def convertStringsToObjectIds(self, data: dict) -> dict:
    """
    Convert specific string fields to ObjectId if they exist.

    Args:
      data (dict): The input dictionary.

    Returns:
      dict: The updated dictionary with fields converted to ObjectId.
    """
    try:
      # id is a special case, convert to _id
      if "id" in data:
        if isinstance(data["id"], str):
          data["_id"] = ObjectId(data["id"])

        elif isinstance(data["id"], dict) and "$in" in data["id"]:
          # Handle the case where _id is a dictionary with the $in operator
          # For example: {"id": {"$in": ["id1", "id2"]}}
          # id in list of rankedIds
          data["_id"] = {}
          data["_id"]["$in"] = [ObjectId(oid) for oid in data["id"]["$in"]]
        del data["id"]

      if "userId" in data:
        if isinstance(data["userId"], str):
          data["userId"] = ObjectId(data["userId"])

        elif isinstance(data["userId"], dict) and "$in" in data["userId"]:
          # Handle the case where _id is a dictionary with the $in operator
          # For example: {"id": {"$in": ["id1", "id2"]}}
          # id in list of rankedIds
          data["userId"]["$in"] = [ObjectId(oid) for oid in data["userId"]["$in"]]

      # Status is a dictionary with lists of strings
      if "status" in data and data["status"] is not None:
        defaultStatus = {
          "applied": [],
          "rejected": [],
          "accepted": [],
          "declined": []
        }
        status = data.get("status", defaultStatus)
        data["status"] = {
          key: [ObjectId(value) for value in values if isinstance(value, str)] if isinstance(values, list) else []
          for key, values in status.items()
        }
      return data

    except Exception as e:
      logger.error(f"Error converting strings to ObjectIds: {e}")
      raise Exception(f"Error converting strings to ObjectIds: {e}")



# Alias for NoSqlConnection.getInstance
# This alias allows for easier access to the NoSqlDatabase singleton instance.
getNoSqlConn = NoSqlConnection.getInstance
