# -*- coding: utf-8 -*-
"""
Package Name: routers
Description: This package contains the API routers for the Opus application.
Author: MathTeixeira
Date: September 23, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55

This package includes routers for different functionalities of the application:
  - SeekerRouter: This router handles the API endpoints related to Seekers.
"""

from .seekerRouter import seekerRouter
from .jobRouter import jobRouter
from .aiRouter import aiRouter
from .authRouter import authRouter
from .applicationRouter import applicationRouter

__all__ = ['seekerRouter', 'jobRouter', 'aiRouter', 'authRouter', 'applicationRouter']
