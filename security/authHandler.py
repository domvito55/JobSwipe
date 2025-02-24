# -*- config: utf-8 -*-
"""
File Name: auth.py
Description: This script defines the AuthHandler class for handling user
 authentication and authorization in the application.
Author: MathTeixeira
Date: July 6, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

### Imports ###
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from starlette import status

from core.database.sqlDatabase import sqlDb
from schemas import UserProtectedSchema
from models import Job

# User will send password and username to that url to get the token, that will
# be returned to oauth2Scheme.
oauth2Scheme = OAuth2PasswordBearer(tokenUrl=f"/auth/token")


class AuthHandler:
  """
  The AuthHandler class provides methods for handling user authentication and authorization.
  """

  def getCurrentUser(
      self,
      token: str = Depends(oauth2Scheme),
      session: Session = Depends(sqlDb.getSession)
  ) -> UserProtectedSchema:
    """
        Get the current user from the database using the provided credentials.

        Args:
          token (str): The user's authentication token.
          session (Session): The database session.

        Returns:
          UserProtectedSchema: The current user from the database.
        """
    ########## NOTE: FOR SIMPLICITY, IN THIS SMALL PROJECT, TOKEN CONTAINS THE
    # USERNAME ONLY; BEFORE SENDING TO PRODUCTION THIS SHOULD BE ENHANCED.
    # ##########
    query = select(Job).where(Job.username == token)
    user = session.exec(query).first()

    if not user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail="Invalid credentials",
                          headers={"WWW-Authenticate": "Bearer"})
    return UserProtectedSchema.model_validate(user)
