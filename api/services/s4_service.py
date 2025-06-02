from fastapi import APIRouter, HTTPException, Depends
from fastapi import File
from api.db import get_db
from api.utils.logging import logger

def get_file():
    pass

def create_file(file_name, file, file_type):