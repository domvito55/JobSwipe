# Opus API

## Overview

Opus API is a FastAPI-based backend service designed to manage job seekers,
job postings, and user authentication. This API provides endpoints for
creating, retrieving, updating, and deleting job seekers and job postings,
as well as user authentication and AI services.

There is a live running version of this code running on aws, that you can try
using swagger at this address:

https://d3tughb5ymsff6.cloudfront.net/docs


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [License](#license)
- [Contact](#contact)

## Features

- **User Authentication**: Manage user authentication with endpoints for
 creating and retrieving users.
- **Job Seekers**: Endpoints for managing job seekers, including creating,
 retrieving, updating, and deleting seeker profiles.
- **Job Postings**: Endpoints for managing job postings, including creating,
 retrieving, updating, and deleting job postings.
- **AI Services**: Integration with AI services that will match and rank the
the best candidates for each postion. And also the best positions for each
candidate
- **Health Check**: Endpoint to check the health status of the API.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/domvito55/opusBackend_dom
    cd opusBackend_dom
    ```

2. **Set up the environment**:
    - Create a `.env` file and add necessary environment variables.
    NO_SQL_USERNAME=<yourcredential>
    NO_SQL_PASSWORD=<yourcredential>
    NO_SQL_NAME=<databaseName>

    - Install dependencies:
      ```sh
      pip install -r requirements.txt
      ```

3. **Run the application**:
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

4. **Note**:
    A .circleci folder is provided, you can use this template to build a
     pipeline in your own circleci account and have cicd set to automatically
     deploy the code using DOCKER and AWC ECS.

    the Dockerfile is also provided

## Usage

### Docker

To run the application using Docker:

1. **Build the Docker image**:
    ```sh
    docker build -t opus-api .
    ```

2. **Run the Docker container**:
    ```sh
    docker run -p 8000:8000 opus-api
    ```

## API Endpoints

### Authentication

- **Create User**: `POST /api/auth/{collectionName}`
- **Get User by Filters**: `GET /api/auth/{collectionName}/{filters}`

### Job Seekers

- **Create Seeker**: `POST /api/seeker/{collectionName}`
- **Get All Seekers**: `GET /api/seeker/{collectionName}`
- **Get Seeker by Filters**: `GET /api/seeker/{collectionName}/{filters}`
- **Update Seeker**: `PUT /api/seeker/{collectionName}/{filters}`
- **Delete Seeker**: `DELETE /api/seeker/{collectionName}/{filters}`

### Jobs

- **Create Job**: `POST /api/job/{collectionName}`
- **Get All Jobs**: `GET /api/job/{collectionName}`
- **Get Job by Filters**: `GET /api/job/{collectionName}/{filters}`
- **Update Job**: `PUT /api/job/{collectionName}/{filters}`
- **Delete Job**: `DELETE /api/job/{collectionName}/{filters}`

### AI Services

- **Get Top Jobs for Seeker**: `GET /api/ai/jobs/{username}`
- **Get Top Seekers for Job**: `GET /api/ai/seekers/{jobId}`

### Health Check

- **Health Check**: `GET /check`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Author: MathTeixeira  
Contact Information: mathteixeira55