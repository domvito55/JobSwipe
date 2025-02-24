import json
import random
from bson import ObjectId

# Load the JSON data
with open("job_data.json", "r") as file:
    jobs = json.load(file)

# Define the user IDs (simulated ObjectIds)
user_ids = [
    ObjectId("6735034250b60baaa4401c0f"),
    ObjectId("673503f150b60baaa4401c11"),
    ObjectId("6735309c4d502b9d54e50d8a"),
    ObjectId("673530af4d502b9d54e50d8b"),
    ObjectId("673530c64d502b9d54e50d8c")
]

# Function to clean data, generate emails based on job title, and add updatedDate
def clean_data(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if key == "$numberLong":
                # Replace with a random 10-digit integer for phone numbers
                new_data = random.randint(1000000000, 9999999999)
            elif key == "jobInfo":
                # Move jobTitle to main level if present
                if "jobTitle" in value:
                    new_data["jobTitle"] = value.pop("jobTitle")  # Move jobTitle to main object and remove from jobInfo
                    # Generate a unique email based on job title inside jobInfo
                    job_title = new_data["jobTitle"].replace(" ", "").lower()
                    value["email"] = f"{job_title}@example.com"
                # Clean other data in jobInfo
                new_data[key] = clean_data(value)
            elif key == "createdDate":
                # Copy createdDate to updatedDate
                new_data["updatedDate"] = value
                new_data[key] = value
            elif key == "_id":
                # Ensure _id remains the same type (ObjectId)
                new_data[key] = {"$oid": value["$oid"]}
            elif key == "jobId":
                # Skip jobId field
                pass
            else:
                new_data[key] = clean_data(value)
        return new_data
    elif isinstance(data, list):
        # Process each item in lists
        return [clean_data(item) for item in data]
    else:
        return data

# Clean the data by replacing $numberLong, generating emails, and setting updated dates
cleaned_jobs = clean_data(jobs)

# Filter out jobs that do not have primarySkills or have empty primarySkills
filtered_jobs = [
    job for job in cleaned_jobs 
    if "primarySkills" in job and (job["primarySkills"].get("technicalSkills") or job["primarySkills"].get("transferableSkills"))
]

# Calculate the number of jobs per user for even distribution
num_jobs = len(filtered_jobs)
jobs_per_user = num_jobs // len(user_ids)
extra_jobs = num_jobs % len(user_ids)  # Handle any remainder

# Assign userIds to jobs
job_index = 0
for i, user_id in enumerate(user_ids):
    # Determine how many jobs this user should receive
    jobs_for_this_user = jobs_per_user + (1 if i < extra_jobs else 0)
    
    # Assign userId to the specified number of jobs
    for _ in range(jobs_for_this_user):
        filtered_jobs[job_index]["userId"] = {"$oid": str(user_id)}
        job_index += 1

# Save the cleaned and updated data back to a JSON file
with open("job_data_cleaned_and_assigned.json", "w") as file:
    json.dump(filtered_jobs, file, indent=4)

print("Cleaned JSON with unique emails, random phone numbers, userId assignments, and updated dates saved as job_data_cleaned_and_assigned.json.")
