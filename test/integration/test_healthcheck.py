# -*- config: utf-8 -*-
"""
File Name: test_healthcheck.py
Description: This script tests the healthcheck endpoint of the opus API.
Author: MathTeixeira
Date: November 12, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""


def testHome(client):
  """
  Test the healthcheck endpoint of the API.

  Args:
    client (TestClient): The FastAPI TestClient instance.

  Returns:
    None
  """
  response = client.get("/check")
  assert response.status_code == 200
  assert "Welcome to the Opus API!" in response.text
