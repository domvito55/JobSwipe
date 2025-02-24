# -*- config: utf-8 -*-
"""
File Name: test_getTopJobs.py
Description: This script tests the getTopJobs endpoint of the JobSwipe API.
Author: MathTeixeira
Date: December 3, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""
from core.config import noSql

# client is a fixture coming from conftest.py
def testApplyForJob(client):
  """
  Test the getTopJobs endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """

  # Load the sample data
  statusUpdate = {
    "userId": "6733aec175eb0fba49f14363",
    "jobId": "6735a696d6cff11d57b1d9b1",
    "newStatus": "accept",
    "oldStatus": "apply"
  }

  # Test the patchJob endpoint
  response = client.patch(f"/api/application/updateApplication", json=statusUpdate)
  assert response.status_code == 200
  assert  "6733aec175eb0fba49f14363" in response.json()["message"]
  assert  "6735a696d6cff11d57b1d9b1" in response.json()["message"]
  assert  "accept" in response.json()["message"]
  assert  "successfully" in response.json()["message"]
