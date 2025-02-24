# test_ai_service.py

import json
import pytest
from unittest.mock import patch
from services.aiService import AIService

# Sample data for testing
with open("./test/unit/sampleData/twoJobs.json") as file:
  sample_jobs_json = json.load(file)

with open("./test/unit/sampleData/twoCandidates.json") as file:
  sample_candidates_json = json.load(file)

@pytest.fixture
def ai_service():
  """Fixture to provide an instance of AIService."""
  # Mock the SkillExtractor initialization to avoid loading spacy during testing
  with patch("services.aiService.SkillExtractor"):
    return AIService.getInstance()

def test_json_to_tfidf(ai_service):
  """Test json_to_tfidf method"""
  tfidf_df, vectorizer = ai_service.json_to_tfidf(sample_jobs_json)
  assert tfidf_df.shape[0] == 2  # Ensure 2 rows in the dataframe
  assert "web_developers" in vectorizer.get_feature_names_out()  # Ensure features are generated

def test_get_top_jobs_for_candidate(ai_service):
  """Test get_top_jobs_for_candidate method"""
  top_jobs = ai_service.get_top_jobs_for_candidate(sample_candidates_json[0], sample_jobs_json)
  assert len(top_jobs) == 2  # Ensure we get 2 results since there are 2 jobs
  assert "6735a696d6cff11d57b1d95c" in top_jobs  # Ensure job_1 is in the top results

def test_get_top_candidates_for_job(ai_service):
  """Test get_top_candidates_for_job method"""
  top_candidates = ai_service.get_top_candidates_for_job(sample_jobs_json[0], sample_candidates_json)
  assert len(top_candidates) == 2  # Ensure we get 2 results since there are 2 candidates
  assert '6733aec175eb0fba49f14363' in top_candidates  # Ensure user_1 is in the top results
