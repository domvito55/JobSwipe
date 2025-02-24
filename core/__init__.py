# -*- coding: utf-8 -*-
"""
Package Name: core
Description: This package contains the core modules for the application.
Author: MathTeixeira
Date: September 23, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55

This package includes configuration modules and database interfaces. It provides
 centralized access to configuration settings and database connections used
 throughout the application.
"""

from .config import noSql
from .database.noSqlDatabase import NoSqlConnection

__all__ = ['noSql', 'NoSqlConnection']
