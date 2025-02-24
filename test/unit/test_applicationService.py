import json
import pytest
from unittest.mock import Mock, patch
from bson import ObjectId
from services.applicationService import ApplicationService
from schemas import ApplicationSchema

# Load test data
with open("./test/unit/sampleData/twoJobs.json") as file:
    sample_jobs_json = json.load(file)

with open("./test/unit/sampleData/twoCandidates.json") as file:
    sample_candidates_json = json.load(file)

pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_db():
    """Mock database connection to capture operations"""
    with patch('services.applicationService.getNoSqlConn') as mock:
        db = Mock()
        mock.return_value = db
        yield db

@pytest.fixture
async def sample_application():
    """Fixture to provide a sample application schema."""
    return ApplicationSchema(
        userId=sample_candidates_json[0]["id"],
        jobId=sample_jobs_json[0]["id"],
        newStatus="apply",
        oldStatus="reject"
    )

class TestApplicationService:
    """Test suite for ApplicationService class."""

    @pytest.mark.asyncio
    async def test_job_operation_construction(self, sample_application, mock_db):
        """Test if the job operation is constructed correctly"""
        # Execute the operation
        await ApplicationService.jobOperation(sample_application)
        
        # Get the last call made to documentOperation
        operation_call = mock_db.documentOperation.call_args
        
        # Extract the arguments
        collection_name = operation_call.args[0]  # First arg: collection name
        filters = operation_call.args[1]          # Second arg: filters
        actual_operation = operation_call.args[2]  # Third arg: operation
        
        # Expected MongoDB operation
        expected_operation = {
            "$pull": {"status.rejected": ObjectId(sample_application.userId)},
            "$addToSet": {"status.applied": ObjectId(sample_application.userId)}
        }
        
        # Verify operation matches expected
        assert actual_operation == expected_operation
        assert collection_name == "jobs"
        assert filters == {"_id": ObjectId(sample_application.jobId)}

    @pytest.mark.asyncio
    async def test_seeker_operation_construction(self, sample_application, mock_db):
        """Test if the seeker operation is constructed correctly"""
        # Execute the operation
        await ApplicationService.seekerOperation(sample_application)
        
        # Get the last call made to documentOperation
        operation_call = mock_db.documentOperation.call_args
        
        # Extract the arguments
        collection_name = operation_call.args[0]  # First arg: collection name
        filters = operation_call.args[1]          # Second arg: filters
        actual_operation = operation_call.args[2]  # Third arg: operation
        
        # Expected MongoDB operation
        expected_operation = {
            "$pull": {"status.rejected": ObjectId(sample_application.jobId)},
            "$addToSet": {"status.applied": ObjectId(sample_application.jobId)}
        }
        
        # Verify operation matches expected
        assert actual_operation == expected_operation
        assert collection_name == "seekers"
        assert filters == {"userId": ObjectId(sample_application.userId)}

    @pytest.mark.asyncio
    async def test_status_transition_operation_construction(self, mock_db):
        """Test if the status transition operations are constructed correctly"""
        # Create application schema for accept to decline transition
        transition_app = ApplicationSchema(
            userId=sample_candidates_json[0]["id"],
            jobId=sample_jobs_json[0]["id"],
            newStatus="decline",
            oldStatus="accept"
        )
        
        # Execute the operation
        await ApplicationService.jobOperation(transition_app)
        
        # Get the last call made to documentOperation
        operation_call = mock_db.documentOperation.call_args
        
        # Extract the arguments
        collection_name = operation_call.args[0]  # First arg: collection name
        filters = operation_call.args[1]          # Second arg: filters
        actual_operation = operation_call.args[2]  # Third arg: operation
        
        # Expected MongoDB operation
        expected_operation = {
            "$pull": {"status.accepted": ObjectId(transition_app.userId)},
            "$addToSet": {"status.declined": ObjectId(transition_app.userId)}
        }
        
        # Verify operation matches expected
        assert actual_operation == expected_operation
        assert collection_name == "jobs"
        assert filters == {"_id": ObjectId(transition_app.jobId)}