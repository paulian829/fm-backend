import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
# STUDENTS_ENDPOINT = os.getenv('STUDENTS_ENDPOINT', 'https://facemask.algebrary.tech/')
STUDENTS_ENDPOINT = os.getenv('STUDENTS_ENDPOINT', 'http://localhost:5000/')
VIOLATIONS_DIRECTORY_PATH = os.getenv('DIRECTORY_PATH', './cubaapp/static/assets/violations/')
# debug = os.getenv('DEBUG')

