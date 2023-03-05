import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
# STUDENTS_ENDPOINT = os.getenv('STUDENTS_ENDPOINT', 'https://facemask.algebrary.tech/')
VIOLATIONS_DIRECTORY_PATH = os.getenv('DIRECTORY_PATH', './cubaapp/static/assets/violations/')
STUDENTS_FOLDER = os.getenv('STUDENTS_FOLDER', './cubaapp/static/students/')
URL = os.getenv('URL', 'http://localhost:8000/')
HAARCASCADES_FOLDER = os.getenv('HAARCASCADE_FOLDER', './cubaapp/recognition/Haarcascades/haarcascade_frontalface_default.xml')
TRAINING_IMAGES_FOLDER = os.getenv('TRAINING_IMAGES_FOLDER', './cubaapp/static/training_images/')
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', './cubaapp/static/output/')
BASE_PATH = os.getenv('BASE_PATH', './cubaapp/')

# VIOLATIONS_DIRECTORY_PATH = os.getenv('DIRECTORY_PATH', '/home/fmthesis/fm-backend/cubaapp/static/assets/violations/')
# STUDENTS_FOLDER = os.getenv('STUDENTS_FOLDER', '/home/fmthesis/fm-backend/cubaapp/static/students')
# URL = os.getenv('URL', 'https://fmthesis.pythonanywhere.com/')
# HAARCASCADES_FOLDER = os.getenv('HAARCASCADE_FOLDER', '/home/fmthesis/fm-backend/cubaapp/recognition/Haarcascades/haarcascade_frontalface_default.xml')
# TRAINING_IMAGES_FOLDER = os.getenv('TRAINING_IMAGES_FOLDER', '/home/fmthesis/fm-backend/cubaapp/static/training_images/')
# OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', '/home/fmthesis/fm-backend/cubaapp/static/output/')
# BASE_PATH = os.getenv('BASE_PATH', '/home/fmthesis/fm-backend/cubaapp')