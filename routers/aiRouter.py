# -*- coding: utf-8 -*-
"""
File Name: aiRouter.py
Description: This script defines the AI router for the JobSwipe API.
Author: MathTeixeira
Date: October 10, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

import json
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from models import Job, Seeker
from schemas import ResponseSchema
from services import JobService, getAIService, SeekerService
from utils import userIdPath, jobIdPath

aiRouter = APIRouter()


@aiRouter.get("/jobs/{userId}",
              summary="Get the list of jobs for a given seeker",
              response_model=ResponseSchema)
async def getTopJobs(userId: str = userIdPath):
  """
  """
  try:
    aiService = getAIService()

    # Get the seeker by userId
    seeker = await SeekerService.getSeekerByFilters('seekers',
                                                    {'userId': ObjectId(userId)})
    # Convert seeker to JSON (dict)
    seeker = Seeker.model_dump(seeker)
    
    # Get all jobs
    jobs = await JobService.getJobs('jobs')
    # Convert jobs to JSON (dict)
    jobs = [Job.model_dump(job) for job in jobs]

    rankedJobsIDs = aiService.get_top_jobs_for_candidate(seeker, jobs)

    query = {"id": {"$in": rankedJobsIDs}}
    listJob = await JobService.getListJobByQuery('jobs', query)
    if listJob:
      job_dict = {str(job.id): job for job in listJob}
      ordered_jobs = [job_dict[job_id] for job_id in rankedJobsIDs if job_id in job_dict]
      return ResponseSchema(message=ordered_jobs, code=status.HTTP_200_OK)
    else:
      return ResponseSchema(message="Jobs not found",
                            code=status.HTTP_404_NOT_FOUND)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=str(e))


@aiRouter.get("/seekers/{jobId}",
              summary="Get the list of seekers for a given job",
              response_model=ResponseSchema)
async def getTopSeekers(jobId: str = jobIdPath):
  """
  """
  try:
    aiService = getAIService()
    # Get the job by jobId
    job = await JobService.getJobByFilters('jobs', {'id': jobId})

    # Convert job to JSON (dict)
    job = Job.model_dump(job)

    # Get all seekers
    seekers = await SeekerService.getSeekers('seekers')

    # Convert seekers to JSON (dict)
    seekers = [Seeker.model_dump(seeker) for seeker in seekers]

    rankedIds = aiService.get_top_candidates_for_job(job, seekers)

    query = {"userId": {"$in": rankedIds}}

    listSeekers = await SeekerService.getListSeekerByQuery('seekers', query)
    if listSeekers:
      seeker_dict = {str(seeker.userId): seeker for seeker in listSeekers}
      ordered_seekers = [seeker_dict[seeker_id] for seeker_id in rankedIds if seeker_id in seeker_dict]
      return ResponseSchema(message=ordered_seekers, code=status.HTTP_200_OK)
    else:
      return ResponseSchema(message="Seekers not found",
                            code=status.HTTP_404_NOT_FOUND)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=str(e))

""" tejinder """
from typing import List
from fastapi import Query

@aiRouter.get(
    "/appliedSeekers/{jobId}",
    summary="Get the list of seekers who applied for a given job",
    response_model=ResponseSchema
)
async def getTopAppliedSeekers(
    jobId: str = jobIdPath,
    userIds: List[str] = Query(..., description="List of seeker user IDs to consider")
):
    """
    Get the list of top seekers for a given job using AI ranking,
    considering only the provided seeker user IDs.
    """
    try:
        aiService = getAIService()
        # Get the job by jobId
        job = await JobService.getJobByFilters('jobs', {'id': jobId})

        # Convert job to JSON (dict)
        job = Job.model_dump(job)

        # Filter seekers by provided IDs
        query = {"userId": {"$in": userIds}}
        seekers = await SeekerService.getListSeekerByQuery('seekers', query)

        if not seekers:
            return ResponseSchema(message="No seekers found for the provided IDs",
                                  code=status.HTTP_404_NOT_FOUND)

        # Convert seekers to JSON (dict)
        seekers = [Seeker.model_dump(seeker) for seeker in seekers]

        # Use AI service to rank the filtered seekers for the job
        rankedIds = aiService.get_top_candidates_for_job(job, seekers)

        # Get detailed seeker information for the ranked IDs
        query = {"userId": {"$in": rankedIds}}
        listSeekers = await SeekerService.getListSeekerByQuery('seekers', query)

        if listSeekers:
          seeker_dict = {str(seeker.userId): seeker for seeker in listSeekers}
          ordered_seekers = [seeker_dict[seeker_id] for seeker_id in rankedIds if seeker_id in seeker_dict]
          return ResponseSchema(message=ordered_seekers, code=status.HTTP_200_OK)
        else:
            return ResponseSchema(message="No ranked seekers found",
                                  code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))