# -*- coding: utf-8 -*-
"""
File Name: authRouter.py
Description: This script defines the routers for user authentication.
Author: MathTeixeira
Date: October 11, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""
import json
from fastapi import APIRouter, HTTPException, status

from models import User
from schemas import ResponseSchema, UserProtectedSchema
from services import AuthService
from utils import userCollectionPath, userFiltersPath

authRouter = APIRouter()


# Create
@authRouter.post("/{collectionName}",
                summary="Create new user",
                status_code=status.HTTP_201_CREATED,
                response_model=ResponseSchema)
async def createUser(*, collectionName: str = userCollectionPath, user: User):
  """
  Create a new user entry.

  This endpoint accepts a User object and stores it in the database.

  Args:
      collectionName (str): The name of the collection to insert the document into.
      user (User): The user to be created.

  Returns:
      ResponseSchema: A response containing the created user and a status code.

  Raises:
      HTTPException: If there's an error creating the user.
  """
  try:
    createdUser = await AuthService.createUser(collectionName, user)
    createdUser = UserProtectedSchema.model_validate(createdUser)
    return ResponseSchema(message=createdUser, code=status.HTTP_201_CREATED)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=str(e))


# Retrieve
@authRouter.get("/{collectionName}/{filters}",
               summary="Get one user based on filter dictionary",
               response_model=ResponseSchema)
async def getUserByFilters(collectionName: str = userCollectionPath,
                             filters: str = userFiltersPath):
  """
  Retrieve a user document by a specified filter dictionary.

  Args:
    collectionName (str): The name of the collection to retrieve the document from.
    filters (str): The filters to apply to the database query.

  Returns:
    ResponseSchema: A response containing the role and a status code.
  """
  try:
    filters = json.loads(filters)
    user = await AuthService.getUserByFilters(collectionName, filters)
    user = UserProtectedSchema.model_validate(user)
    if user:
      return ResponseSchema(message=user, code=status.HTTP_200_OK)
    else:
      return ResponseSchema(message="User not found",
                            code=status.HTTP_404_NOT_FOUND)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=str(e))


# # -*- coding: utf-8 -*-
# """
# File Name: auth.py
# Description: This script defines the routers for user authentication.
# Author: MathTeixeira
# Date: July 6, 2024
# Version: 3.0.0
# License: MIT License
# Contact Information: mathteixeira55
# """
# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlmodel import Session, select
# from starlette import status

# from core.database.sqlDatabase import sqlDb
# from models import User

# router = APIRouter()

# @router.post("/token")
# async def login(formData: OAuth2PasswordRequestForm = Depends(),
#                 session: Session = Depends(sqlDb.getSession)) -> dict:
#   """
#   Get the authentication token for the user.

#   Args:
#     formData (OAuth2PasswordRequestForm): The user's login credentials.
#     session (Session): The database session.

#   Returns:
#     dict: The user's authentication token.
#   """
#   query = select(User).where(User.username == formData.username)
#   user = session.exec(query).first()

#   if not user or not user.verifyPassword(formData.password):
#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                         detail="Invalid credentials",
#                         headers={"WWW-Authenticate": "Bearer"})
#   # ########## NOTE: FOR SIMPLICITY, IN THIS SMALL PROJECT, TOKEN CONTAINS THE
#   # USERNAME ONLY; BEFORE SENDING TO PRODUCTION THIS SHOULD BE ENHANCED.
#   # ##########
#   return {"access_token": user.username, "token_type": "bearer"}
