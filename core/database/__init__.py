# -*- coding: utf-8 -*-
"""
File Name: __init__.py
Description: This module initializes and exports database instances for
 NoSQL databases.
Author: MathTeixeira
Date: September 23, 2024
Version: 3.0.0
License: MIT License
Contact Information: mathteixeira55

This file imports and exports database instances for NoSQL databases.
The NoSQL database class is exported for on-demand instantiation.
"""

from .noSqlDatabase import NoSqlConnection, getNoSqlConn

__all__ = ['NoSqlConnection', 'getNoSqlConn']
