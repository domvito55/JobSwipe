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
def testGetTopSeekers(client):
  """
  Test the getTopJobs endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """
  # Get the first seeker from the database
  collectionName = noSql.JOBS_COLLECTION
  response = client.get(f"/api/job/{collectionName}")
  responseJson = response.json()
  jobId = responseJson["message"][0]["id"]

  # Get the jobs for the selected seeker
  response = client.get(f"/api/ai/seekers/{jobId}")

  # Check if the response status code is 200
  assert response.status_code == 200

  # Check if the response contains the expected fields
  responseJson = response.json()
  seekerList = responseJson["message"]
  assert all(["userId" in seeker for seeker in seekerList])
  assert all(["primarySkills" in seeker for seeker in seekerList])
