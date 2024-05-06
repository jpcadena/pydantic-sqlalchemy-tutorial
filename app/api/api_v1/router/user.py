"""
User API Router
This module provides CRUD (Create, Retrieve, Update, Delete) operations
 for users.
"""

from fastapi import APIRouter

router: APIRouter = APIRouter(prefix="/user", tags=["user"])
