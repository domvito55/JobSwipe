# -*- coding: utf-8 -*-
"""
File Name: jobRouter.py
Description: This module defines the API routes for managing job.
Author: MathTeixeira
Date: October 10, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

import json
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError

from models import Job, JobUpdate
from schemas import ResponseSchema
from services import JobService
from utils import jobCollectionPath, jobFiltersPath, jobQueryPath

jobRouter = APIRouter()

# -------------------------------- Create
@jobRouter.post("/{collectionName}",
                        summary="Create new job post",
                        status_code=status.HTTP_201_CREATED,
                        response_model=ResponseSchema)
async def createJob(*,
                        collectionName: str = jobCollectionPath,
                        job: Job):
  """
  Create a new job entry.

  This endpoint accepts a Job object and stores it in the database.

  Args:
      collectionName (str): The name of the collection to insert the document into.
      job (Job): The job to be created.

  Returns:
      ResponseSchema: A response containing the created job and a status code.

  Raises:
      HTTPException: If there's an error creating the job.
  """
  try:
    createdJob = await JobService.createJob(
        collectionName, job)
    responseContent = {
      "message": jsonable_encoder(createdJob),
      "code": status.HTTP_201_CREATED
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_201_CREATED)
  except Exception as e:
    responseContent = {
      "message": f"Error - Not able to create job: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# -------------------------------- Retrieve
# 1. ----- get all jobs
@jobRouter.get("/{collectionName}",
                  summary="Get all jobs",
                  response_model=ResponseSchema)
async def getJobs(collectionName: str = jobCollectionPath):
  """
  Retrieve all job documents from a specified collection.

  Args:
      collectionName (str): The name of the collection to retrieve the documents from.

  Returns:
      ResponseSchema: A response containing all jobs and a status code.

  Raises:
      HTTPException: If there's an error retrieving the jobs.
  """
  try:
    jobs = await JobService.getJobs(collectionName)
    return ResponseSchema(message=jobs, code=status.HTTP_200_OK)
  except Exception as e:
    responseContent = {
      "message": f"Error - Not able to retrieve jobs: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 2. ----- get one job by filters
@jobRouter.get("/{collectionName}/{filters}",
                       summary="Get one job based on filter dictionary",
                       response_model=ResponseSchema)
async def getJobByFilters(collectionName: str = jobCollectionPath,
                                filters: str = jobFiltersPath):
  """
  Retrieve a job document by a specified filter dictionary.

  Args:
    collectionName (str): The name of the collection to retrieve the document from.
    filters (str): The filters to apply to the database query.

  Returns:
    ResponseSchema: A response containing the job document and a status code.
  """
  try:
    filters = json.loads(filters)
    job = await JobService.getJobByFilters(
        collectionName, filters)
    if job:
      return ResponseSchema(message=job, code=status.HTTP_200_OK)
    else: # send a 404 response if the job is not found
      responseContent = {
        "message": "Job not found",
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

# 3. ----- get jobs by filters
@jobRouter.get("/{collectionName}/list/{query}",
                       summary="Get list of jobs based on a query dictionary",
                       response_model=ResponseSchema)
async def getJobByQuery(collectionName: str = jobCollectionPath,
                                query: str = jobQueryPath):
  """
  Retrieve a job document by a specified filter dictionary.

  Args:
    collectionName (str): The name of the collection to retrieve the document from.
    query (str): The query to apply to the database.

  Returns:
    ResponseSchema: A response containing a list of jobs and a status code.
  """
  try:
    query = json.loads(query)
    jobList = await JobService.getListJobByQuery(
        collectionName, query)
    if jobList:
      return ResponseSchema(message=jobList, code=status.HTTP_200_OK)
    else: # send a 404 response if the job is not found
      responseContent = {
        "message": "No job found",
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
      "message": f"Error - Not able to retrieve any job: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------------------------- Update
@jobRouter.patch("/{collectionName}/{filters}",
                       summary="Update Job",
                       response_model=ResponseSchema)
async def updateJob(collectionName: str = jobCollectionPath, filters: str = jobFiltersPath, *,
                            job: JobUpdate):
  """
  Update an existing job document by a specified filters

  Args:
    collectionName (str): The name of the collection to update the document in.
    filters (str): The filters to search by.
    job (Job): The updated

  Returns:
    ResponseSchema: A response containing a success message and a status code.

  Raises:
    HTTPException: If there's an error updating the job.
  """
  try:
    filters = json.loads(filters)
    updateResult = await JobService.patchJob(
        collectionName, filters, job)
    if updateResult:
      return ResponseSchema(message=f"Job updated successfully! {updateResult}",
                            code=status.HTTP_200_OK)
    else: # send a 404 response if the job is not found
      responseContent = {
        "message": f"Error - Either job do not exist or not updated {filters}",
        "code": status.HTTP_404_NOT_FOUND
      }
      return JSONResponse(content=responseContent, status_code=status.HTTP_404_NOT_FOUND)
  except Exception as e:
    responseContent = {
      "message": f"Error - Not able to update job: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ----------------------------------- Delete
@jobRouter.delete("/{collectionName}/{filters}",
                          summary="Delete Job",
                          response_model=ResponseSchema)
async def deleteJob(collectionName: str = jobCollectionPath, filters: str = jobFiltersPath):
  """
  Delete a job by filters.

  Args:
    collectionName (str): The name of the collection to delete the job from.
    filters (str): The filters to search by.

  Returns:
    ResponseSchema: A response containing a confirmation message and a status code.

  Raises:
    HTTPException: If there's an error deleting the job.
  """
  try:
    filters = json.loads(filters)
    deleteResult = await JobService.deleteJob(
        collectionName, filters)
    if deleteResult:
      return ResponseSchema(message="Job deleted successfully.",
                            code=status.HTTP_200_OK)
    else:
      responseContent = {
        "message": f"Error - Either job was not found or not deleted {filters}",
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR
      }
      return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  except Exception as e:
    responseContent = {
      "message": f"Error - Unable to delete job: {str(e)}",
      "code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
    return JSONResponse(content=responseContent, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
