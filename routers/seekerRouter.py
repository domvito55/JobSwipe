# -*- coding: utf-8 -*-
"""
File Name: seekerRouter.py
Description: This module defines the API routes for managing seeker.
Author: MathTeixeira
Date: September 23, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

import json
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError

from services import SeekerService
from models import Seeker, SeekerUpdate
from schemas import ResponseSchema
from utils import seekerCollectionPath, userIdFilterPath, seekerQueryPath

seekerRouter = APIRouter()

# -------------------------------- Create
@seekerRouter.post("/{seekerCollection}",
                        summary="Create new seeker",
                        status_code=status.HTTP_201_CREATED,
                        response_model=ResponseSchema)
async def createSeeker(*,
                        seekerCollection: str = seekerCollectionPath,
                        seeker: Seeker):
  """
  Create a new seeker entry.

  This endpoint accepts a ChatHistory object and stores it in the database.

  Args:
      collectionName (str): The name of the collection to insert the document into.
      chatHistory (ChatHistory): The seeker to be created.

  Returns:
      ResponseSchema: A response containing the created seeker and a status code.

  Raises:
      HTTPException: If there's an error creating the seeker.
  """
  try:
    createdSeeker = await SeekerService.createSeeker(
        seekerCollection, seeker)
    responseContent = {
      "message": jsonable_encoder(createdSeeker),
      "code": status.HTTP_201_CREATED
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_201_CREATED)
  except Exception as e:
    responseContent = {
      "message": f"Error - Not able to create job: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --------------------------------- Retrieve
# 1. ----- Get all seekers
@seekerRouter.get("/{seekerCollection}",
                  summary="Get all seekers",
                  response_model=ResponseSchema)
async def getSeekers(seekerCollection: str = seekerCollectionPath):
  """
  Retrieve all seeker documents from a specified collection.

  Args:
      collectionName (str): The name of the collection to retrieve the documents from.

  Returns:
      ResponseSchema: A response containing all seekers and a status code.

  Raises:
      HTTPException: If there's an error retrieving the seekers.
  """
  try:
    seekers = await SeekerService.getSeekers(seekerCollection)
    return ResponseSchema(message=seekers, code=status.HTTP_200_OK)
  except Exception as e:
    responseContent = {
      "message": f"Error - Not able to retrieve seekers: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 2. ----- Get one seeker
@seekerRouter.get("/{seekerCollection}/{filters}",
                       summary="Get one seeker based on filter dictionary",
                       response_model=ResponseSchema)
async def getSeekerByFilters(seekerCollection: str = seekerCollectionPath,
                                filters: str = userIdFilterPath):
  """
  Retrieve a seeker document by a specified filter dictionary.

  Args:
    collectionName (str): The name of the collection to retrieve the document from.
    filters (str): The filters to apply to the database query.

  Returns:
    ResponseSchema: A response containing the seeker document and a status code.
  """
  try:
    filters = json.loads(filters)
    seeker = await SeekerService.getSeekerByFilters(
        seekerCollection, filters)
    if seeker:
      return ResponseSchema(message=seeker, code=status.HTTP_200_OK)
    else: # send a 404 response if the seeker is not found
      responseContent = {
        "message": f"Seeker not found with {filters}",
        "code": status.HTTP_404_NOT_FOUND
      }
      return JSONResponse(content=responseContent, status_code=status.HTTP_404_NOT_FOUND)
  except PyMongoError as e:
    responseContent = {
      "message": f"Database error: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  except Exception as e:
    responseContent = {
      "message": f"Error - Not able to retrieve job: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 3. ----- Get one seeker by query
@seekerRouter.get("/{seekerCollection}/list/{query}",
                        summary="Get one seeker based on query dictionary",
                        response_model=ResponseSchema)
async def getSeekerByQuery(seekerCollection: str = seekerCollectionPath,
                              query: str = seekerQueryPath):
  """
  Retrieve a seeker document by a specified query dictionary.

  Args:
    collectionName (str): The name of the collection to retrieve the document from.
    query (str): The query to apply to the database query.

  Returns:
    ResponseSchema: A response containing the seeker document and a status code.
  """
  try:
    query = json.loads(query)
    seeker = await SeekerService.getListSeekerByQuery(seekerCollection, query)
    if seeker:
      return ResponseSchema(message=seeker, code=status.HTTP_200_OK)
    else: # send a 404 response if the seeker is not found
      responseContent = {
        "message": f"Seeker not found with {query}",
        "code": status.HTTP_404_NOT_FOUND
      }
      return JSONResponse(content=responseContent, status_code=status.HTTP_404_NOT_FOUND)
  except PyMongoError as e:
    responseContent = {
      "message": f"Database error: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  except Exception as e:
    responseContent = {
      "message": f"Error - Not able to retrieve job: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# -------------------------------- Update
@seekerRouter.patch("/{seekerCollection}/{filters}",
                       summary="Update Seeker",
                       response_model=ResponseSchema)
async def patchSeeker(seekerCollection: str = seekerCollectionPath, filters: str = userIdFilterPath, *,
                            seeker: SeekerUpdate):
  """
  Update an existing seeker document by a specified filters

  Args:
    collectionName (str): The name of the collection to update the document in.
    filters (str): The filters to search by.
    seeker (Seeker): The updated

  Returns:
    ResponseSchema: A response containing a success message and a status code.

  Raises:
    HTTPException: If there's an error updating the seeker.
  """
  try:
    filters = json.loads(filters)
    updateResult = await SeekerService.patchSeeker(
        seekerCollection, filters, seeker)
    if updateResult:
      return ResponseSchema(message=f"Seeker updated successfully {updateResult}",
                            code=status.HTTP_200_OK)
    else: # send a 404 response if the job is not found
      responseContent = {
        "message": f"Error - Either seeker do not exist or not updated {filters}",
        "code": status.HTTP_404_NOT_FOUND
      }
      return JSONResponse(content=responseContent, status_code=status.HTTP_404_NOT_FOUND)
  except Exception as e:
    responseContent = {
      "message": f"Error - Not able to update seker: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ------------------------------------ Delete
@seekerRouter.delete("/{seekerCollection}/{filters}",
                          summary="Delete Seeker",
                          response_model=ResponseSchema)
async def deleteSeeker(seekerCollection: str = seekerCollectionPath, filters: str = userIdFilterPath):
  """
  Delete a seeker by filters.

  Args:
    collectionName (str): The name of the collection to delete the seeker from.
    filters (str): The filters to search by.

  Returns:
    ResponseSchema: A response containing a confirmation message and a status code.

  Raises:
    HTTPException: If there's an error deleting the seeker.
  """
  try:
    filters = json.loads(filters)
    deleteResult = await SeekerService.deleteSeeker(
        seekerCollection, filters)
    if deleteResult:
      return ResponseSchema(message="Seeker deleted successfully.",
                            code=status.HTTP_200_OK)
    else:
      responseContent = {
        "message": f"Error - Either seeker was not found or not deleted {filters}",
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR
      }
      return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  except Exception as e:
    responseContent = {
      "message": f"Error - Unable to delete seeker: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
