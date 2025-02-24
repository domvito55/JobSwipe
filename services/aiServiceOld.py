# Import necessary libraries
import subprocess
import sys

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from spacy.matcher import PhraseMatcher
# Load default skills database
from skillNer.general_params import SKILL_DB
# Import skill extractor
from skillNer.skill_extractor_class import SkillExtractor
from sklearn.metrics.pairwise import cosine_similarity
import json


class AIService:
  """
  Class to provide AI services for the job matching system
  """

  _instance: 'AIService | None' = None

  def __init__(self):
    # Install spaCy model
    AIService.install_spacy_model("en_core_web_lg")
    # Initialize parameters of skill extractor
    nlp = spacy.load("en_core_web_lg")
    # Initialize skill extractor
    self.skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

  @classmethod
  def getInstance(cls) -> 'AIService':
    """
    Get the singleton instance of AIService.

    Returns:
      NoSqlConnection: The singleton instance of AIservice.
    """
    if cls._instance is None:
      cls._instance = cls()
    return cls._instance


  def json_to_tfidf(self, job_list, max_features=50000):
    """
      Function to convert a list of job descriptions in JSON format to a TF-IDF matrix
      Parameters:
          job_list: list, the list of job descriptions in JSON format
          max_features: int, the maximum number of features to consider in the TF-IDF vectorizer
      Returns:
          tfidf_df: DataFrame, the TF-IDF matrix in DataFrame format
          vectorizer: TfidfVectorizer, the fitted TfidfVectorizer object
      """
    # Initialize the TfidfVectorizer
    vectorizer = TfidfVectorizer(max_features=max_features)
    # Extract the 'skills_extracted' field from each JSON object
    skills_list = [item['skills_extracted'] for item in job_list]

    # Fit and transform the skills_list
    tfidf_matrix = vectorizer.fit_transform(skills_list)

    # Convert the TF-IDF matrix to a DataFrame for better readability
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

    return tfidf_df, vectorizer

  def get_top_jobs_for_candidate(self, seeker_skills: str, jobs_json: list, top_jobs=10) -> list:
    """
      Function to get the top 10 job IDs for a given candidate skills
      Parameters:
          seeker_skills: str, the skills of the candidate
          jobs_json: list, the list of job descriptions in JSON format
          top_jobs: int, the number of top jobs to return
      Returns:
          top10_jobs_ids: list, the list of top 10 job IDs

      """
    extracted_seeker_skills = self.extract_skills(seeker_skills)

    job_tfidf_df, vectorizer = self.json_to_tfidf(jobs_json)
    seeker_skills_tfidf = vectorizer.transform([extracted_seeker_skills])
    # Compute cosine similarity between the seeker skills and job descriptions
    cosine_similarities = cosine_similarity(seeker_skills_tfidf, job_tfidf_df).flatten()

    # Get the indices of the top most similar job descriptions
    top10_jobs_indices = cosine_similarities.argsort()[-top_jobs:][::-1]

    # Get the corresponding job IDs
    top10_jobs_ids = [jobs_json[i]['jobId'] for i in top10_jobs_indices]

    return top10_jobs_ids
  
  def get_top_candidates_for_job(self, job_skills: str, candidates_json: list, top_candidates=10) -> list:
    """
    Function to get the top 10 candidate IDs for a given job skills
    Parameters:
        job_skills: str, the skills of the job
        candidates_json: list, the list of candidate profiles in JSON format
        top_candidates: int, the number of top candidates to return
    Returns:
        top10_candidates_ids: list, the list of top 10 candidate IDs
    """
    extracted_job_skills = self.extract_skills(job_skills)

    candidate_tfidf_df, vectorizer = self.json_to_tfidf(candidates_json)
    job_skills_tfidf = vectorizer.transform([extracted_job_skills])
    # Compute cosine similarity between the job skills and candidate profiles
    cosine_similarities = cosine_similarity(job_skills_tfidf, candidate_tfidf_df).flatten()

    # Get the indices of the top most similar candidate profiles
    top10_candidates_indices = cosine_similarities.argsort()[-top_candidates:][::-1]


    # Get the corresponding candidate IDs
    top10_candidates_ids = [candidates_json[i]['userId'] for i in top10_candidates_indices]
    

    return top10_candidates_ids


  # --------------------------- Auxiliary Methods
  @staticmethod
  def install_spacy_model(model_name):
    """
    Function to install a spaCy model if not already installed
    Parameters:
        model_name: str, the name of the spaCy model to install
    """
    try:
      spacy.load(model_name)
    except OSError:
      subprocess.check_call(
          [sys.executable, "-m", "spacy", "download", model_name])

  def preprocess_text(self, text: str) -> str:
    # Remove any unwanted characters or extra spaces
    text = text.replace('(', '').replace(')', '').replace(',', ' ')
    text = ' '.join(text.split())
    return text

  def extract_skills(self, text):
    """
    Function to extract skills from a given text
    Parameters:
        text: str, the text from which to extract skills
    Returns:
        skills_list: list, the list of extracted skills
    """
    try:
      text = self.preprocess_text(text)
      annotations = self.skill_extractor.annotate(text)
      skills_list = []

      # Check for full_matches
      if 'results' in annotations and 'full_matches' in annotations['results']:
        skills_list.extend([
            skill['doc_node_value']
            for skill in annotations['results']['full_matches']
        ])

      # Check for ngram_scored
      if 'results' in annotations and 'ngram_scored' in annotations['results']:
        skills_list.extend([
            skill['doc_node_value']
            for skill in annotations['results']['ngram_scored']
        ])

      # Remove duplicates and limit to first 6 skills
      skills_list = list(dict.fromkeys(skills_list))[:20]

      return ' '.join(skills_list)
    except Exception as e:
      print(f"Error processing text: {text}\nError: {e}")
      return ''

# Alias for NoSqlConnection.getInstance
# This alias allows for easier access to the NoSqlDatabase singleton instance.
getAIService = AIService.getInstance


# print("start testing")
# test = AIService()
# seeker_skills = "instagram content content creation social medium social medium analytic social advertising social media"
# import json
# file_path = 'opus55.jobs.json'
# with open(file_path, 'r') as file:
#     data = json.load(file)

# a = test.get_top_jobs_for_candidate(seeker_skills, data)
# print("testing")

# print(a)
