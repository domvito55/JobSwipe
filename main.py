# -*- coding: utf-8 -*-
"""
File Name: main.py
Description: This is the main entry point for the Opus API. It sets up
 the FastAPI  application, includes routers, and defines the base endpoints.
Author: MathTeixeira
Date: Setember 23, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

### Imports ###
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from schemas import ResponseSchema
from routers import applicationRouter, seekerRouter, jobRouter, aiRouter, authRouter
from core.database import getNoSqlConn
from services import getAIService
from pymongo import ASCENDING

import logging

logger = logging.getLogger("uvicorn")

### Lifespan Events ###
@asynccontextmanager
async def lifespan(app: FastAPI):
  logger.info("Starting up...")
  app.noSqlConn = getNoSqlConn()
  app.aiService = getAIService()
  # Create the index if it doesn't already exist, in the background
  app.collection = app.noSqlConn.database["seekers"]
  logger.info("Ensuring index on 'userId' field for seekers")
  app.collection.create_index([("userId", ASCENDING)],
                              unique=True,
                              background=True)
  app.collection = app.noSqlConn.database["users"]
  logger.info("Ensuring index on 'username' field")
  app.collection.create_index([("username", ASCENDING)],
                              unique=True,
                              background=True)
  yield
  logger.info("Shutting down...")
  app.noSqlConn.shutdownDbClient()


### Initialize FastAPI App ###
app = FastAPI(
    title="Opus API",
    version="1.0.0",
    lifespan=lifespan,
    description=
    "API for the Jobswipe application."
)

# custom exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    response_content = {
        "message": f"Error - Validation failed: {exc.errors()}",
        "code": status.HTTP_422_UNPROCESSABLE_ENTITY
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

### Include Routers ###
# Uncomment and modify these lines if you add authentication and user management in the future
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(users.router, prefix="/api/users", tags=["Users"])

# app.include_router(ideationRouter, prefix="/api/ideation", tags=["Ideation"])
app.include_router(authRouter, prefix="/api/auth", tags=["Auth"])
app.include_router(aiRouter, prefix="/api/ai", tags=["AI"])
app.include_router(applicationRouter, prefix="/api/application", tags=["Application"])
app.include_router(jobRouter, prefix="/api/job", tags=["Jobs"])
app.include_router(seekerRouter, prefix="/api/seeker", tags=["Seeker"])#

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


### API Endpoints ###
@app.get("/check",
         tags=["Health Check"],
         summary="Health Check",
         response_model=ResponseSchema)
def health_check() -> ResponseSchema:
  """
    Health check endpoint for the 

    Returns:
        ResponseSchema: A dictionary containing a welcome message and a status code.
    """
  return ResponseSchema(message="Welcome to the Opus API!", code=200)


### Main ###
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(
      "main:app",
      host="0.0.0.0",
      port=8000,
      reload=True,
      reload_delay=1,  # Add a slight delay
      workers=1  # Ensure single worker for development
  )
