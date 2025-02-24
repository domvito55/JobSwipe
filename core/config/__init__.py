# -*- coding: utf-8 -*-
"""
File Name: __init__.py
Description: This module initializes and exports configuration instances for various components.
Author: MathTeixeira
Date: September 23, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55

This file imports and exports configuration instances for AWS and NoSQL components.
These instances are created using the singleton pattern implemented in their respective modules.
"""

from .noSqlConfig import noSql

__all__ = ['noSql']
