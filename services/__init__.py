# -*- coding: utf-8 -*-
"""
Package Name: services
Description: This package contains service classes for the chat application.
Author: MathTeixeira
Date: July 11, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55

This package includes the following service:
- IdeationService: Manages chat-based ideation sessions using AWS Bedrock and LangChain.
- ChatHistoryService: Manages chat history data storage and retrieval.
- MessageListService: Manages messages in a FILO (stack) style.


These services provide the core functionality for the chat application,
handling interactions with external APIs and processing chat messages.
"""

from .seekerService import SeekerService
from .jobService import JobService
from .aiService import AIService, getAIService
from .authService import AuthService
from .applicationService import ApplicationService

__all__ = [
    'SeekerService',
    'JobService',
    'AIService',
    'getAIService',
    'AuthService',
    'ApplicationService'
]
