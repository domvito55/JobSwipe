# -*- coding: utf-8 -*-
"""
File Name: conftest.py
Description: This file contains pytest fixtures for the Car Sharing API project.
Author: MathTeixeira
Date: July 8, 2024
Version: 5.0.0
License: MIT License
Contact Information: mathteixeira55
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# One can add fixtures as arguments to the test functions to use them.


@pytest.fixture(scope="module")
def client():
  """
    Fixture that creates a FastAPI TestClient.

    Returns:
      TestClient: A FastAPI TestClient instance for testing API endpoints.
    """
  return TestClient(app)


# @pytest.fixture(scope="module")
# def auth_token(client):
#   """
#     Fixture that obtains an authentication token for testing protected routes.

#     Args:
#       client (TestClient): The FastAPI TestClient instance.

#     Returns:
#       str: The authentication token.

#     Raises:
#       AssertionError: If the login request fails.
#     """
#   response = client.post("/auth/token",
#                          data={
#                              "username": "johndoe22",
#                              "password": "1"
#                          })
#   assert response.status_code == 200
#   return response.json()["access_token"]
