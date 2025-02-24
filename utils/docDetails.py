# -*- coding: utf-8 -*-
"""
File Name: docDetails.py
Description: This module contains query and path parameters for API documentation.
Author: MathTeixeira
Date: July 12, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

from fastapi import Query, Path

### Query Parameters ###
# Query is used to define query parameters for the API endpoints.
# These definitions also provide Swagger documentation for the query parameters.
# sizeQuery: str | None = Query(
#     None,
#     description="Filter cars by size (s, m, l)",
#     openapi_examples={"small": {
#         "summary": "Small car",
#         "value": "s"
#     }})

### Path Parameters ###
# Path is used to define path parameters for the API endpoints.
seekerCollectionPath: str = Path(
    ...,
    description="Collection name for the database",
    openapi_examples={
        "Seeker": {
            "summary": "Seeker Collection",
            "value": "seekers"
        }
    })

jobCollectionPath: str = Path(
    ...,
    description="Collection name for the database",
    openapi_examples={"Jobs": {
        "summary": "Job Collection",
        "value": "jobs"
    }})

userCollectionPath: str = Path(
    ...,
    description="Collection name for the database",
    openapi_examples={"User": {
        "summary": "User Collection",
        "value": "users"
    }})

userIdFilterPath: str = Path(
    ...,
    description="Filters to be applied to the database",
    openapi_examples={
        "filters": {
            "summary": "Dict of filters to be applied to the database",
            "value": '{"userId": "6733aec175eb0fba49f14363"}'
        }
    })

userIdPath: str = Path(
    ...,
    description="UserId to be searched in the database",
    openapi_examples={
        "fieldName": {
            "summary": "UserId to search for",
            "value": "6733aec175eb0fba49f14363"
        }
    })

userIdPath: str = Path(
    ...,
    description="UserId to be searched in the database",
    openapi_examples={
        "fieldName": {
            "summary": "UserId to search for",
            "value": "6733aec175eb0fba49f14363"
        }
    })

jobIdPath: str = Path(
    ...,
    description="JobID to be searched in the database",
    openapi_examples={
        "fieldName": {
            "summary": "JobID to search for",
            "value": "6735a696d6cff11d57b1d95c"
        }
    })

jobFiltersPath: str = Path(
    ...,
    description="Filters to be applied to the database",
    openapi_examples={
        "filters": {
            "summary": "Dict of filters to be applied to the database",
            "value": '{"userId": "6733aec175eb0fba49f14363"}'
        }
    })

jobQueryPath: str = Path(
    ...,
    description="Query to database",
    openapi_examples={
        "query": {
            "summary": "Dict query to be applied to the database",
            "value": '{"userId": "6733aec175eb0fba49f14363"}'
        }
    })

seekerQueryPath: str = Path(
    ...,
    description="Query to database",
    openapi_examples={
        "query": {
            "summary": "Dict query to be applied to the database",
            "value": '{"primarySkills.technicalSkills": {"$elemMatch": {"skillName": "Engineering"} } }'
        }
    })

userFiltersPath: str = Path(
    ...,
    description="Filters to be applied to the database",
    openapi_examples={
        "filters": {
            "summary": "Dict of filters to be applied to the database",
            "value": '{"username": "tonystark"}'
        }
    })

fieldPath: str = Path(
    ...,
    description="Field to be searched in the database",
    openapi_examples={
        "fieldName": {
            "summary": "The name of the field",
            "value": "username"
        }
    })

valuePath: str = Path(
    ...,
    description="Value to be searched in the database",
    openapi_examples={
        "fieldValue": {
            "summary": "The value to search for",
            "value": "tonystark"
        }
    })

sessionPath: str = Path(
    ...,
    description="Session ID for the chat history",
    openapi_examples={
        "Test": {
            "summary": "The ID of the session",
            "value": "be46af78-63da-42d8-9145-ea99419689c4"
        }
    })
