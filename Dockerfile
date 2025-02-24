# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only necessary files, excluding .env and other unnecessary files
COPY core core/
COPY enums enums/
COPY models models/
COPY routers routers/
COPY schemas schemas/
COPY security security/
COPY services services/
COPY utils utils/
COPY main.py .
COPY requirements.txt .

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies with limited concurrency and disabled progress bar
RUN pip install --no-cache-dir --no-compile --disable-pip-version-check --progress-bar off -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
