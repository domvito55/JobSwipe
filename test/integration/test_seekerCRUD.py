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
collectionName = noSql.SEEKERS_COLLECTION

# ------------- Test the createSeeker endpoint -------------
def testCreateSeeker(client):
  """
  Test the getTopJobs endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """

  # Load the sample data
  with open("./test/integration/sampleData/oneSeeker.json") as file:
    seeker = json.load(file)

  # Test the createSeeker endpoint
  response = client.post(f"/api/seeker/{collectionName}", json=seeker)
  assert response.status_code == 201

# ------------- Test the getSeekers endpoint -------------
def testGetSeekers(client):
  """
  Test the getSeekers endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """
  # Test the getSeekers endpoint
  response = client.get(f"/api/seeker/{collectionName}")
  assert response.status_code == 200

# ------------- Test the getSeekerByFilters endpoint -------------
def testGetSeekerByFilters(client):
  """
  Test the getSeekerByFilters endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """
  filters = "%7B%22userId%22%3A%20%2267362770d263ab83366f58aa%22%7D"

  # Test the getSeekerByFilters endpoint
  response = client.get(f"/api/seeker/{collectionName}/{filters}")
  assert response.status_code == 200

# ------------- Test the patchSeeker endpoint -------------
def testPatchSeeker(client):
  """
  Test the patchSeeker endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """
  # Load the sample data
  seekerUpdate = {
    "userId": "67362770d263ab83366f58aa",
    "areaOfInterest": "Artificial Intelligence2"
  }
  filters = "%7B%22userId%22%3A%20%2267362770d263ab83366f58aa%22%7D"

  # # Test the patchSeeker endpoint
  response = client.patch(f"/api/seeker/{collectionName}/{filters}", json=seekerUpdate)
  assert response.status_code == 200
  assert  "Artificial Intelligence2" in response.json()["message"]

# ------------- Test the deleteSeeker endpoint -------------
def testDeleteSeeker(client):
  """
  Test the deleteSeeker endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """
  filters = "%7B%22userId%22%3A%20%2267362770d263ab83366f58aa%22%7D"

  # Test the deleteSeeker endpoint
  response = client.delete(f"/api/seeker/{collectionName}/{filters}")
  assert response.status_code == 200
  assert response.json()["message"] == "Seeker deleted successfully."