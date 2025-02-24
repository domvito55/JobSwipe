# -*- config: utf-8 -*-
"""
File Name: test_getTopJobs.py
Description: This script tests the getTopJobs endpoint of the JobSwipe API.
Author: MathTeixeira
Date: November 12, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""
from core.config import noSql

# client is a fixture coming from conftest.py
def testGetTopJobs(client):
  """
  Test the getTopJobs endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """
  # Get the first seeker from the database
  collectionName = noSql.SEEKERS_COLLECTION
  response = client.get(f"/api/seeker/{collectionName}")
  responseJson = response.json()
  userId = responseJson["message"][0]["userId"]

  # Get the jobs for the selected seeker
  response = client.get(f"/api/ai/jobs/{userId}")

  # Check if the response status code is 200
  assert response.status_code == 200

  # Check if the response contains the expected fields
  responseJson = response.json()
  jobList = responseJson["message"]
  assert all(["userId" in job for job in jobList])
