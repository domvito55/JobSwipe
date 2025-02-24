# -*- coding: utf-8 -*-
"""
File Name: noSqlConfig.py
Description: This module handles the configuration of the NoSQL database connection.
Author: MathTeixeira
Date: September 23, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55
"""

### Imports ###
from dotenv import load_dotenv
import os


class NoSqlConfig:
  """
  Config class to load environment variables and provide configuration values for NoSQL database connection.

  This class implements a singleton pattern with lazy loading to ensure
  only one instance is created and only when it's first needed.

  Attributes:
    USERNAME (str): The username for NoSQL database connection.
    PASSWORD (str): The password for NoSQL database connection.
    NAME (str): The name of the NoSQL database.
    URL (str): The complete NoSQL database connection URL.

  Raises:
    ValueError: If required environment variables are not set.
  """

  instance: 'NoSqlConfig | None' = None

  def __init__(self) -> None:
    """
    Initialize the NoSqlConfig instance.

    Loads environment variables and sets NoSQL database connection details.

    Raises:
      ValueError: If required environment variables are not set.
    """
    load_dotenv()
    self.USERNAME: str = self.getEnv("NO_SQL_USERNAME")
    self.PASSWORD: str = self.getEnv("NO_SQL_PASSWORD")
    self.NAME: str = self.getEnv("NO_SQL_NAME")

    self.SEEKERS_COLLECTION: str = self.getEnv("SEEKERS_COLLECTION")
    self.JOBS_COLLECTION: str = self.getEnv("JOBS_COLLECTION")
    self.USERS_COLLECTION: str = self.getEnv("USERS_COLLECTION")

    self.URL: str = f"mongodb+srv://{self.USERNAME}:{self.PASSWORD}@opuscluster.kptre.mongodb.net/?retryWrites=true&w=majority&appName=opusCluster"

  @classmethod
  def getInstance(cls) -> 'NoSqlConfig':
    """
    Get the singleton instance of NoSqlConfig.

    Returns:
      NoSqlConfig: The singleton instance of NoSqlConfig.

    This method ensures that only one instance of NoSqlConfig is created.
    """
    if cls.instance is None:
      cls.instance = cls()
    return cls.instance

  def getEnv(self, key: str) -> str:
    """
    Get an environment variable or raise an exception if it's not set.

    Args:
      key (str): The name of the environment variable.

    Returns:
      str: The value of the environment variable.

    Raises:
      ValueError: If the environment variable is not set.
    """
    value = os.getenv(key)
    if value is None:
      raise ValueError(f"Environment variable '{key}' is not set")
    return value


# Global instance of NoSqlConfig
# This will create the instance when the module is imported
noSql = NoSqlConfig.getInstance()
