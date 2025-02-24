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
import json
from core.config import noSql

# Define the collection name
collectionName = noSql.JOBS_COLLECTION

# ------------- Test the createJob endpoint -------------
def testCreateJob(client):
  """
  Test the getTopJobs endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """

  # Load the sample data
  with open("./test/integration/sampleData/oneJob.json") as file:
    job = json.load(file)

  # Test the createJob endpoint
  response = client.post(f"/api/job/{collectionName}", json=job)
  assert response.status_code == 201

# ------------- Test the getJobs endpoint -------------
def testGetJob(client):
  """
  Test the getJobs endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """
  # Test the getJobs endpoint
  response = client.get(f"/api/job/{collectionName}")
  assert response.status_code == 200

# ------------- Test the getJobByFilters endpoint -------------
def testGetJobByFilters(client):
  """
  Test the getJobByFilters endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """
  filters = "%7B%22userId%22%3A%20%2267362770d263ab83366f58aa%22%7D"

  # Test the getJobByFilters endpoint
  response = client.get(f"/api/job/{collectionName}/{filters}")
  assert response.status_code == 200

# ------------- Test the patchJob endpoint -------------
def testPatchJob(client):
  """
  Test the patchJob endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """
  # Load the sample data
  jobUpdate = {
    "userId": "67362770d263ab83366f58aa",
    "jobTitle":
        "Software Engineer2"
  }

  filters = "%7B%22userId%22%3A%20%2267362770d263ab83366f58aa%22%7D"

  # # Test the patchJob endpoint
  response = client.patch(f"/api/job/{collectionName}/{filters}", json=jobUpdate)
  assert response.status_code == 200
  assert  "Software Engineer2" in response.json()["message"]

# # ------------- Test the deleteJob endpoint -------------
def testDeleteJob(client):
  """
  Test the deleteJob endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """
  filters = "%7B%22userId%22%3A%20%2267362770d263ab83366f58aa%22%7D"

  # Test the deleteJob endpoint
  response = client.delete(f"/api/job/{collectionName}/{filters}")
  assert response.status_code == 200
  assert response.json()["message"] == "Job deleted successfully."