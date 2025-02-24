# Import necessary libraries
import subprocess
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

import spacy
from spacy.matcher import PhraseMatcher

# Load default skills database
from skillNer.general_params import SKILL_DB

# Import skill extractor
from skillNer.skill_extractor_class import SkillExtractor


class AIService:
    """
    Class to provide AI services for the job matching system

    atributtes:
        _instance: 'AIService | None' = None
        skill_extractor: SkillExtractor = None

    methods:
        __init__(self) -> None
        getInstance(cls) -> 'AIService'
        install_spacy_model(model_name) -> None
        preprocess_text(text: str) -> str
        extract_skills(data) -> Tuple[list, list, list, list]
        clone_and_concatenate_skills(primary_hard_skills, primary_soft_skills, secondary_hard_skills, secondary_soft_skills, primary_multiplier=3, secondary_multiplier=1, hard_multiplier=2, soft_multiplier=1) -> str
        extract_and_concatenate_skills_without_weights(data: dict, primary_multiplier: int=3, secondary_multiplier: int=1, hard_multiplier: int=2, soft_multiplier: int=1) -> str
        json_to_tfidf(self, job_list, max_features=50000) -> Tuple[pd.DataFrame, TfidfVectorizer]
        get_top_jobs_for_candidate(seeker: dict, listJobs: list[dict], top_jobs: int=10) -> list[dict]
        get_top_candidates_for_job(job: dict, candidates_json: list, top_candidates=10) -> list
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
        skills_list = []
        for item in job_list:
            if 'skills_extracted' in item:
                skills_list.append(item['skills_extracted'])
            else:
                # print(f"Extracting skills for job {item['id']}")
                skills_list.append(self.extract_and_concatenate_skills_without_weights(item))

        # Fit and transform the skills_list
        tfidf_matrix = vectorizer.fit_transform(skills_list)

        # Convert the TF-IDF matrix to a DataFrame for better readability
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

        return tfidf_df, vectorizer

    def get_top_jobs_for_candidate(self,
                                   seeker: dict,
                                   listJobs: list[dict],
                                   top_jobs: int=10) -> list[dict]:
        """
        Function to get the top 10 job IDs for a given candidate skills
        Parameters:
            seekers: dict, the skills of the candidate
            listJobs: list, the list of job descriptions in JSON format
            top_jobs: int, the number of top jobs to return
        Returns:
            top10_jobs_ids: list, the list of top 10 job IDs
        """
        extracted_seeker_skills = self.extract_and_concatenate_skills_without_weights(seeker)
        job_tfidf_df, vectorizer = self.json_to_tfidf(listJobs)
        seeker_skills_tfidf = vectorizer.transform([extracted_seeker_skills])
        # Compute cosine similarity between the seeker skills and job descriptions
        cosine_similarities = cosine_similarity(seeker_skills_tfidf, job_tfidf_df).flatten()
        # Get the indices of the top most similar job descriptions
        top10_jobs_indices = cosine_similarities.argsort()[-top_jobs:][::-1]
        # Get the corresponding job IDs
        top10_jobs_ids = [listJobs[i]['id'] for i in top10_jobs_indices]

        return top10_jobs_ids

    def get_top_candidates_for_job(self, job: dict,
                                   candidates_json: list,
                                   top_candidates=10) -> list:
        """
        Function to get the top 10 candidate IDs for a given job skills
        Parameters:
            job_skills: dict, the skills of the job
            candidates_json: list, the list of candidate profiles in JSON format
            top_candidates: int, the number of top candidates to return
        Returns:
            top10_candidates_ids: list, the list of top 10 candidate IDs
        """
        extracted_job_skills = self.extract_and_concatenate_skills_without_weights(job)
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
        text = text.replace('(', '').replace(')', '').replace(',', ' ').replace('/', ' ').replace('-', ' ').replace('.', ' ')
        text = ' '.join(text.split())
        # Lowercase
        text = text.lower()
        # Replace space with underscore
        text = text.replace(' ', '_')
        return text

    def extract_skills(self, data):
        """
        Function to extract skills from the given data model.
        Parameters:
            data: dict, the data model containing job information and skills
        Returns:
            primary_hard_skills: list, a list of primary hard skills
            primary_soft_skills: list, a list of primary soft skills
            secondary_hard_skills: list, a list of secondary hard skills
            secondary_soft_skills: list, a list of secondary soft skills
        """
        primary_hard_skills = []
        primary_soft_skills = []
        secondary_hard_skills = []
        secondary_soft_skills = []

        # Extract primary hard skills
        if 'primarySkills' in data and 'technicalSkills' in data['primarySkills']:
            for skill in data['primarySkills']['technicalSkills']:
                skill['skillName'] = self.preprocess_text(skill['skillName'])
                primary_hard_skills.append(skill['skillName'])

        # Extract primary soft skills
        if 'primarySkills' in data and 'transferableSkills' in data['primarySkills']:
            for skill in data['primarySkills']['transferableSkills']:
                skill['skillName'] = self.preprocess_text(skill['skillName'])
                primary_soft_skills.append(skill['skillName'])

        # Extract secondary hard skills
        if 'secondarySkills' in data and 'technicalSkills' in data['secondarySkills']:
            for skill in data['secondarySkills']['technicalSkills']:
                skill['skillName'] = self.preprocess_text(skill['skillName'])
                secondary_hard_skills.append(skill['skillName'])

        # Extract secondary soft skills
        if 'secondarySkills' in data and 'transferableSkills' in data['secondarySkills']:
            for skill in data['secondarySkills']['transferableSkills']:
                skill['skillName'] = self.preprocess_text(skill['skillName'])
                secondary_soft_skills.append(skill['skillName'])

        return primary_hard_skills, primary_soft_skills, secondary_hard_skills, secondary_soft_skills

    def clone_and_concatenate_skills(self,
                                     primary_hard_skills,
                                     primary_soft_skills,
                                     secondary_hard_skills,
                                     secondary_soft_skills,
                                     primary_multiplier=3,
                                     secondary_multiplier=1,
                                     hard_multiplier=2,
                                     soft_multiplier=1):
        """
        Function to clone and concatenate skills.
        Parameters:
            primary_hard_skills: list, a list of primary hard skills
            primary_soft_skills: list, a list of primary soft skills
            secondary_hard_skills: list, a list of secondary hard skills
            secondary_soft_skills: list, a list of secondary soft skills
            primary_multiplier: int, the number of times to clone primary skills
            secondary_multiplier: int, the number of times to clone secondary skills
            hard_multiplier: int, the number of times to clone hard skills
            soft_multiplier: int, the number of times to clone soft skills
        Returns:
            concatenated_skills: str, a concatenated string of all skills with primary skills cloned
        """
        skills_list = []

        # Clone primary hard skills
        primary_hard_skills_cloned = primary_hard_skills * primary_multiplier * hard_multiplier

        # Clone primary soft skills
        primary_soft_skills_cloned = primary_soft_skills * primary_multiplier * soft_multiplier

        # Clone secondary hard skills
        secondary_hard_skills_cloned = secondary_hard_skills * secondary_multiplier * hard_multiplier

        # Clone secondary soft skills
        secondary_soft_skills_cloned = secondary_soft_skills * secondary_multiplier * soft_multiplier

        # Combine all skills
        skills_list.extend(primary_hard_skills_cloned)
        skills_list.extend(primary_soft_skills_cloned)
        skills_list.extend(secondary_hard_skills_cloned)
        skills_list.extend(secondary_soft_skills_cloned)

        # Concatenate skills into a single string
        concatenated_skills = ' '.join(skills_list)

        if not concatenated_skills:
            raise ValueError("No skills found in the data model")

        return concatenated_skills

    def extract_and_concatenate_skills_without_weights(self,
                                                       data: dict,
                                                       primary_multiplier: int=3,
                                                       secondary_multiplier: int=1,
                                                       hard_multiplier: int=2,
                                                       soft_multiplier: int=1) -> str:
        """
        Function to extract skills from the given data model, clone primary skills three times,
        and concatenate them into a single string.
        Parameters:
            data: dict, the data model containing job information and skills
            primary_multiplier: int, the number of times to clone primary skills
            secondary_multiplier: int, the number of times to clone secondary skills
            hard_multiplier: int, the number of times to clone hard skills
            soft_multiplier: int, the number of times to clone soft skills
        Returns:
            concatenated_skills: str, a concatenated string of all skills with primary skills cloned
        """
        try:
            primary_hard_skills, primary_soft_skills, secondary_hard_skills, secondary_soft_skills = self.extract_skills(data)
            concatenated_skills = self.clone_and_concatenate_skills(primary_hard_skills, primary_soft_skills, secondary_hard_skills, secondary_soft_skills, primary_multiplier, secondary_multiplier, hard_multiplier, soft_multiplier)
            return concatenated_skills
        except Exception as e:
            raise e

# Alias for NoSqlConnection.getInstance
# This alias allows for easier access to the NoSqlDatabase singleton instance.
getAIService = AIService.getInstance
