# -*- coding: utf-8 -*-
"""
File Name: jobRouter.py
Description: This module defines the API routes for managing job.
Author: MathTeixeira
Date: December 3, 2024
Version: 3.0.1
License: MIT License
Contact Information: mathteixeira55
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from schemas import ResponseSchema, ApplicationSchema
from services import ApplicationService

applicationRouter = APIRouter()

# ---------------------------------- Update
@applicationRouter.patch("/updateApplication",
                       summary="Update Aplication",
                       response_model=ResponseSchema)
async def updateJob(appdict: ApplicationSchema):
  """
  Update the application status for a job.

  Args:
    appdict (ApplicationSchema): The application information to update.

  Returns:
    ResponseSchema: The response message and status code.
  """
  try:
    updatedJob = await ApplicationService.jobOperation(appdict)
    updatedSeeker = await ApplicationService.seekerOperation(appdict)

    if updatedJob and updatedSeeker:
      return ResponseSchema(message=f"{appdict.newStatus} for user {appdict.userId} to job {appdict.jobId} successfully",
                            code=status.HTTP_200_OK)
    else:
      responseContent = {
        "message": f"Error - Not able to {appdict.newStatus} for user {appdict.userId} to job {appdict.jobId}",
        "code": status.HTTP_404_NOT_FOUND
      }
      return JSONResponse(content=responseContent, status_code=status.HTTP_404_NOT_FOUND)
  except Exception as e:
    responseContent = {
      "message": f"Error -  - Not able to {appdict.newStatus} for user {appdict.userId} to job {appdict.jobId} successfully: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
