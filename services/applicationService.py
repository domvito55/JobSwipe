# -*- coding: utf-8 -*-
"""
File Name: applicationService.py
Description: This module contains the service class for managing application business logic.
Author: MathTeixeira
Date: December 3, 2024
Version: 3.1.0
License: MIT License
Contact Information: mathteixeira55
"""
from bson import ObjectId
from core.database import getNoSqlConn
from core.config import noSql

from schemas import ApplicationSchema

from models import Job
from models import Seeker

import logging

logger = logging.getLogger("uvicorn")


class ApplicationService:
  """
  A service class for managing application business logic.

  This class contains methods for handling the application process, such as applying for a job.

  Attributes:


  Methods:
    jobOperation(appdict: dict) -> Job: Update the job document with the application details.
    seekerOperation(appdict: dict) -> Seeker: Update the seeker document with the application details.
  """
  # --------------------------- Update
  # 1. ----- job operation
  @staticmethod
  async def jobOperation(appdict: ApplicationSchema) -> Job:
    """
    Update the job document with the application details.

    This method takes a dictionary containing the application details and updates the job document
    with the user's application status.

    Args:
      appdict (ApplicationSchema): A dictionary containing the application details.
        - userId (str): The ID of the user applying for the job. Should be a valid ObjectId as a string.
        - jobId (str): The ID of the job being applied for. Should be a valid ObjectId as a string.
        - newStatus (str): The new status for the application. Must be "apply", "reject", "accept", or "decline".
        - oldStatus (str): The old status for the application. Must be "apply", "reject", "accept", or "decline".

        Example:
          {
            "userId": "648c75e9f9a32458f53a96b7",
            "jobId": "648c75e9f9a32458f53a96b8",
            "newStatus": "apply",
            "oldStatus": "reject"
          }

    Returns:
      Job: The updated job document, or None if an error occurred.

    Raises:
      Exception: Any exception that occurs during the update process is caught,
                 logged, and results in returning None.
    """
    try:
      jobFilter = {"_id": ObjectId(appdict.jobId)}

      operation = {}

      if appdict.oldStatus == "apply":
        operation["$pull"] = {"status.applied": ObjectId(appdict.userId)}
      elif appdict.oldStatus == "reject":
        operation["$pull"] = {"status.rejected": ObjectId(appdict.userId)}
      elif appdict.oldStatus == "accept":
        operation["$pull"] = {"status.accepted": ObjectId(appdict.userId)}
      elif appdict.oldStatus == "decline":
        operation["$pull"] = {"status.declined": ObjectId(appdict.userId)}

      if appdict.newStatus == "apply":
        operation["$addToSet"] = {"status.applied": ObjectId(appdict.userId)}
      elif appdict.newStatus == "reject":
        operation["$addToSet"] = {"status.rejected": ObjectId(appdict.userId)}
      elif appdict.newStatus == "accept":
        operation["$addToSet"] = {"status.accepted": ObjectId(appdict.userId)}
      elif appdict.newStatus == "decline":
        operation["$addToSet"] = {"status.declined": ObjectId(appdict.userId)}

      updateResult = getNoSqlConn().documentOperation(noSql.JOBS_COLLECTION,
                                                   jobFilter, operation)

      return Job.model_validate(updateResult)
    except Exception as e:
      logger.error(f"Error - Not able to update job status: {e}")
      return None

  # 2. ----- seeker operation
  @staticmethod
  async def seekerOperation(appdict: ApplicationSchema) -> Seeker:
    """
    Update the seeker document with the application details.

    This method takes a dictionary containing the application details and updates the seeker document
    with the user's application status.

    Args:
      appdict (ApplicationSchema): A dictionary containing the application details.
        - userId (str): The ID of the user applying for the job. Should be a valid ObjectId as a string.
        - jobId (str): The ID of the job being applied for. Should be a valid ObjectId as a string.
        - newStatus (str): The new status for the application. Must be "apply", "reject", "accept", or "decline".
        - oldStatus (str): The old status for the application. Must be "apply", "reject", "accept", or "decline".

        Example:
          {
            "userId": "648c75e9f9a32458f53a96b7",
            "jobId": "648c75e9f9a32458f53a96b8"
            "newStatus": "apply",
            "oldStatus": "reject"
          }

    Returns:
      Seeker: The updated seeker document, or None if an error occurred.

    Raises:
      Exception: Any exception that occurs during the update process is caught,
                 logged, and results in returning None.
    """
    try:
      seekerFilter = {"userId": ObjectId(appdict.userId)}
      operation = {}

      if appdict.oldStatus == "apply":
        operation["$pull"] = {"status.applied": ObjectId(appdict.jobId)}
      elif appdict.oldStatus == "reject":
        operation["$pull"] = {"status.rejected": ObjectId(appdict.jobId)}
      elif appdict.oldStatus == "accept":
        operation["$pull"] = {"status.accepted": ObjectId(appdict.jobId)}
      elif appdict.oldStatus == "decline":
        operation["$pull"] = {"status.declined": ObjectId(appdict.jobId)}

      if appdict.newStatus == "apply":
        operation["$addToSet"] = {"status.applied": ObjectId(appdict.jobId)}
      elif appdict.newStatus == "reject":
        operation["$addToSet"] = {"status.rejected": ObjectId(appdict.jobId)}
      elif appdict.newStatus == "accept":
        operation["$addToSet"] = {"status.accepted": ObjectId(appdict.jobId)}
      elif appdict.newStatus == "decline":
        operation["$addToSet"] = {"status.declined": ObjectId(appdict.jobId)}

      updateResult = getNoSqlConn().documentOperation(noSql.SEEKERS_COLLECTION,
                                                   seekerFilter, operation)


      return Seeker.model_validate(updateResult)
    except Exception as e:
      logger.error(f"Error - not able to update seeker status: {e}")
      return None

